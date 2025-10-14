"""
SSH Honeypot Service
Simulates an SSH server to capture login attempts and commands.
"""

import paramiko
import socket
import threading
from io import StringIO


class SSHServer(paramiko.ServerInterface):
    """SSH Server Interface for the honeypot."""
    
    def __init__(self, logger):
        self.event = threading.Event()
        self.logger = logger
    
    def check_auth_password(self, username, password):
        """Log password authentication attempts."""
        self.logger.log_attack(
            "SSH",
            "unknown",  # Will be updated by parent
            0,
            {
                "type": "password_auth",
                "username": username,
                "password": password
            }
        )
        # Always fail authentication but log the attempt
        return paramiko.AUTH_FAILED
    
    def check_auth_publickey(self, username, key):
        """Log public key authentication attempts."""
        self.logger.log_attack(
            "SSH",
            "unknown",
            0,
            {
                "type": "publickey_auth",
                "username": username,
                "key_type": key.get_name()
            }
        )
        return paramiko.AUTH_FAILED
    
    def get_allowed_auths(self, username):
        """Return allowed authentication methods."""
        return "password,publickey"
    
    def check_channel_request(self, kind, chanid):
        """Handle channel requests."""
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


class SSHHoneypot:
    """SSH Honeypot Service."""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.port = config.get('services.ssh.port', 2222)
        self.bind_address = config.get('general.bind_address', '0.0.0.0')
        self.banner = config.get('services.ssh.banner', 'SSH-2.0-OpenSSH_7.4')
        
        # Generate server key
        self.host_key = paramiko.RSAKey.generate(2048)
    
    def handle_client(self, client_socket, addr):
        """Handle individual SSH client connection."""
        try:
            transport = paramiko.Transport(client_socket)
            transport.local_version = self.banner
            transport.add_server_key(self.host_key)
            
            server = SSHServer(self.logger)
            transport.start_server(server=server)
            
            # Wait for authentication
            channel = transport.accept(20)
            if channel is not None:
                channel.close()
            
        except Exception as e:
            self.logger.log_error(f"SSH error from {addr}: {str(e)}")
        finally:
            try:
                transport.close()
            except:
                pass
    
    def start(self):
        """Start the SSH honeypot service."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.bind_address, self.port))
        server_socket.listen(100)
        
        self.logger.log_info(f"SSH Honeypot listening on {self.bind_address}:{self.port}")
        
        while True:
            try:
                client, addr = server_socket.accept()
                self.logger.log_connection("SSH", addr[0], addr[1])
                
                # Handle client in separate thread
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.log_error(f"SSH service error: {str(e)}")
        
        server_socket.close()
