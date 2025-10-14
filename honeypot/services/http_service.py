"""
HTTP Honeypot Service
Simulates a web server to capture HTTP attacks and reconnaissance.
"""

import socket
import threading
from datetime import datetime


class HTTPHoneypot:
    """HTTP Honeypot Service."""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.port = config.get('services.http.port', 8080)
        self.bind_address = config.get('general.bind_address', '0.0.0.0')
        self.server_name = config.get('services.http.server_name', 'Apache/2.4.41 (Ubuntu)')
    
    def generate_response(self, request_data):
        """Generate HTTP response based on request."""
        # Simple HTML response
        body = """<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Server is Running</h1>
    <p>Welcome to the server.</p>
</body>
</html>"""
        
        headers = f"""HTTP/1.1 200 OK
Server: {self.server_name}
Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Content-Type: text/html
Content-Length: {len(body)}
Connection: close

"""
        return headers + body
    
    def handle_client(self, client_socket, addr):
        """Handle individual HTTP client connection."""
        try:
            request = client_socket.recv(4096).decode('utf-8', errors='ignore')
            
            if request:
                # Log the request
                request_lines = request.split('\n')
                if request_lines:
                    self.logger.log_attack(
                        "HTTP",
                        addr[0],
                        addr[1],
                        {
                            "request_line": request_lines[0],
                            "headers": request_lines[1:10],  # First 10 lines
                            "full_request": request[:500]  # First 500 chars
                        }
                    )
                
                # Send response
                response = self.generate_response(request)
                client_socket.send(response.encode())
        
        except Exception as e:
            self.logger.log_error(f"HTTP error from {addr}: {str(e)}")
        finally:
            client_socket.close()
    
    def start(self):
        """Start the HTTP honeypot service."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.bind_address, self.port))
        server_socket.listen(100)
        
        self.logger.log_info(f"HTTP Honeypot listening on {self.bind_address}:{self.port}")
        
        while True:
            try:
                client, addr = server_socket.accept()
                self.logger.log_connection("HTTP", addr[0], addr[1])
                
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
                self.logger.log_error(f"HTTP service error: {str(e)}")
        
        server_socket.close()
