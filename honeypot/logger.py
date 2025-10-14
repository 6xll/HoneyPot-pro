"""
Logger module for the honeypot system.
Handles logging of all attack attempts and system events.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path


class HoneyPotLogger:
    """Logger for honeypot events and attacks."""
    
    def __init__(self, log_dir="logs"):
        """Initialize the logger with specified log directory."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup main logger
        self.logger = logging.getLogger("HoneyPot")
        self.logger.setLevel(logging.INFO)
        
        # File handler for general logs
        log_file = self.log_dir / f"honeypot_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Attack log file
        self.attack_log = self.log_dir / f"attacks_{datetime.now().strftime('%Y%m%d')}.json"
    
    def log_attack(self, service, source_ip, source_port, data):
        """Log an attack attempt with details."""
        attack_data = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "source_ip": source_ip,
            "source_port": source_port,
            "data": data
        }
        
        # Log to main logger
        self.logger.warning(
            f"Attack on {service} from {source_ip}:{source_port}"
        )
        
        # Append to attack log JSON file
        with open(self.attack_log, 'a') as f:
            f.write(json.dumps(attack_data) + '\n')
    
    def log_connection(self, service, source_ip, source_port):
        """Log a connection attempt."""
        self.logger.info(
            f"Connection to {service} from {source_ip}:{source_port}"
        )
    
    def log_info(self, message):
        """Log an info message."""
        self.logger.info(message)
    
    def log_error(self, message):
        """Log an error message."""
        self.logger.error(message)
