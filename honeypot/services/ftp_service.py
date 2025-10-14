"""
FTP Honeypot Service
Simulates an FTP server to capture login attempts and file operations.
"""

import socket
import threading


class FTPHoneypot:
    """FTP Honeypot Service."""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.port = config.get('services.ftp.port', 2121)
        self.bind_address = config.get('general.bind_address', '0.0.0.0')
        self.banner = config.get('services.ftp.banner', '220 FTP Server Ready')
    
    def handle_client(self, client_socket, addr):
        """Handle individual FTP client connection."""
        username = None
        
        try:
            # Send banner
            client_socket.send(f"{self.banner}\r\n".encode())
            
            while True:
                data = client_socket.recv(1024).decode('utf-8', errors='ignore').strip()
                
                if not data:
                    break
                
                command = data.upper()
                
                if command.startswith('USER'):
                    username = data.split(' ', 1)[1] if ' ' in data else 'anonymous'
                    self.logger.log_attack(
                        "FTP",
                        addr[0],
                        addr[1],
                        {"type": "user", "username": username}
                    )
                    client_socket.send(b"331 Password required\r\n")
                
                elif command.startswith('PASS'):
                    password = data.split(' ', 1)[1] if ' ' in data else ''
                    self.logger.log_attack(
                        "FTP",
                        addr[0],
                        addr[1],
                        {
                            "type": "password",
                            "username": username or "unknown",
                            "password": password
                        }
                    )
                    client_socket.send(b"530 Login incorrect\r\n")
                
                elif command.startswith('QUIT'):
                    client_socket.send(b"221 Goodbye\r\n")
                    break
                
                elif command.startswith('SYST'):
                    client_socket.send(b"215 UNIX Type: L8\r\n")
                
                elif command.startswith('FEAT'):
                    client_socket.send(b"211-Features:\r\n SIZE\r\n MDTM\r\n211 End\r\n")
                
                else:
                    # Log other commands
                    self.logger.log_attack(
                        "FTP",
                        addr[0],
                        addr[1],
                        {"type": "command", "command": data}
                    )
                    client_socket.send(b"502 Command not implemented\r\n")
        
        except Exception as e:
            self.logger.log_error(f"FTP error from {addr}: {str(e)}")
        finally:
            client_socket.close()
    
    def start(self):
        """Start the FTP honeypot service."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.bind_address, self.port))
        server_socket.listen(100)
        
        self.logger.log_info(f"FTP Honeypot listening on {self.bind_address}:{self.port}")
        
        while True:
            try:
                client, addr = server_socket.accept()
                self.logger.log_connection("FTP", addr[0], addr[1])
                
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
                self.logger.log_error(f"FTP service error: {str(e)}")
        
        server_socket.close()
