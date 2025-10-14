"""
Configuration management for the honeypot system.
"""

import yaml
from pathlib import Path


class Config:
    """Configuration manager for the honeypot."""
    
    def __init__(self, config_file="config.yaml"):
        """Load configuration from YAML file."""
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file or use defaults."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self):
        """Return default configuration."""
        return {
            "general": {
                "log_dir": "logs",
                "bind_address": "0.0.0.0"
            },
            "services": {
                "ssh": {
                    "enabled": True,
                    "port": 2222,
                    "banner": "SSH-2.0-OpenSSH_7.4"
                },
                "http": {
                    "enabled": True,
                    "port": 8080,
                    "server_name": "Apache/2.4.41 (Ubuntu)"
                },
                "ftp": {
                    "enabled": True,
                    "port": 2121,
                    "banner": "220 FTP Server Ready"
                }
            }
        }
    
    def get(self, key, default=None):
        """Get configuration value by key."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def save(self):
        """Save current configuration to file."""
        with open(self.config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
