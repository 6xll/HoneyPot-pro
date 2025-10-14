#!/usr/bin/env python3
"""
HoneyPot Main Entry Point
Starts all configured honeypot services.
"""

import sys
import threading
import signal
from honeypot.config import Config
from honeypot.logger import HoneyPotLogger
from honeypot.services.ssh_service import SSHHoneypot
from honeypot.services.http_service import HTTPHoneypot
from honeypot.services.ftp_service import FTPHoneypot


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\nShutting down honeypot...")
    sys.exit(0)


def main():
    """Main function to start the honeypot."""
    print("=" * 50)
    print("HoneyPot - Network Honeypot System")
    print("=" * 50)
    
    # Load configuration
    config = Config()
    
    # Initialize logger
    log_dir = config.get('general.log_dir', 'logs')
    logger = HoneyPotLogger(log_dir)
    
    logger.log_info("Starting HoneyPot system...")
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start services in separate threads
    services = []
    
    # SSH Service
    if config.get('services.ssh.enabled', True):
        ssh_service = SSHHoneypot(config, logger)
        ssh_thread = threading.Thread(target=ssh_service.start)
        ssh_thread.daemon = True
        ssh_thread.start()
        services.append('SSH')
    
    # HTTP Service
    if config.get('services.http.enabled', True):
        http_service = HTTPHoneypot(config, logger)
        http_thread = threading.Thread(target=http_service.start)
        http_thread.daemon = True
        http_thread.start()
        services.append('HTTP')
    
    # FTP Service
    if config.get('services.ftp.enabled', True):
        ftp_service = FTPHoneypot(config, logger)
        ftp_thread = threading.Thread(target=ftp_service.start)
        ftp_thread.daemon = True
        ftp_thread.start()
        services.append('FTP')
    
    logger.log_info(f"All services started: {', '.join(services)}")
    print(f"\nActive services: {', '.join(services)}")
    print("\nPress Ctrl+C to stop the honeypot\n")
    
    # Keep main thread alive
    while True:
        try:
            signal.pause()
        except AttributeError:
            # signal.pause() is not available on Windows
            import time
            time.sleep(1)


if __name__ == "__main__":
    main()
