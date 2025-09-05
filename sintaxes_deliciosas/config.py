"""
Configuration Manager Module

Handles configuration loading, validation, and management for the application.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import os

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager."""
        self.logger = logging.getLogger(__name__)
        self.config_path = self._resolve_config_path(config_path)
        self.config = self._load_config()
    
    def _resolve_config_path(self, config_path: Optional[str]) -> Optional[Path]:
        """Resolve configuration file path."""
        if config_path:
            return Path(config_path)
        
        # Check common configuration locations
        possible_paths = [
            Path.cwd() / 'sintaxes_config.json',
            Path.home() / '.sintaxes_deliciosas' / 'config.json',
            Path.home() / '.config' / 'sintaxes_deliciosas' / 'config.json'
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        return None
    
    def _load_config(self) -> Dict:
        """Load configuration from file or return defaults."""
        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded configuration from {self.config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load config from {self.config_path}: {e}")
        
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            "version": "1.0.0",
            "analyzer": {
                "deep_analysis": False,
                "include_hidden_files": False,
                "max_file_size_mb": 1000,
                "excluded_extensions": [".tmp", ".cache", ".log"],
                "duplicate_threshold_mb": 1
            },
            "organizer": {
                "create_backups": True,
                "backup_directory": "backups",
                "max_filename_length": 255,
                "naming_separator": "_",
                "preserve_timestamps": True,
                "safe_mode": True
            },
            "layout": {
                "default_theme": "professional",
                "auto_apply_icons": True,
                "create_templates": True,
                "enable_auto_organization": True,
                "folder_color_coding": True
            },
            "cloud": {
                "default_strategy": "smart",
                "cache_size_mb": 1024,
                "auto_sync": False,
                "bandwidth_limit_mbps": 0,  # 0 = unlimited
                "conflict_resolution": "prompt",
                "providers": {
                    "dropbox": {
                        "enabled": False,
                        "access_token": ""
                    },
                    "google_drive": {
                        "enabled": False,
                        "credentials_file": ""
                    },
                    "onedrive": {
                        "enabled": False,
                        "client_id": ""
                    },
                    "aws_s3": {
                        "enabled": False,
                        "access_key_id": "",
                        "secret_access_key": "",
                        "bucket": ""
                    }
                }
            },
            "logging": {
                "level": "INFO",
                "file": "",
                "max_size_mb": 10,
                "backup_count": 5
            },
            "ui": {
                "use_colors": True,
                "progress_bars": True,
                "confirm_destructive_actions": True,
                "auto_open_results": False
            },
            "performance": {
                "max_workers": 4,
                "chunk_size": 1000,
                "memory_limit_mb": 2048,
                "enable_caching": True
            }
        }
    
    def get_config(self) -> Dict:
        """Get current configuration."""
        return self.config.copy()
    
    def get_config_path(self) -> Optional[Path]:
        """Get configuration file path."""
        return self.config_path
    
    def save_config(self, config: Optional[Dict] = None) -> None:
        """Save configuration to file."""
        if config is not None:
            self.config = config
        
        if not self.config_path:
            # Create default config path
            config_dir = Path.home() / '.config' / 'sintaxes_deliciosas'
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_path = config_dir / 'config.json'
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            raise
    
    def create_default_config(self, path: Optional[str] = None) -> Path:
        """Create default configuration file."""
        if path:
            config_path = Path(path)
        else:
            config_dir = Path.home() / '.config' / 'sintaxes_deliciosas'
            config_dir.mkdir(parents=True, exist_ok=True)
            config_path = config_dir / 'config.json'
        
        default_config = self._get_default_config()
        
        # Add comments and documentation
        commented_config = self._add_config_comments(default_config)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(commented_config, f, indent=2, ensure_ascii=False)
            
            self.config_path = config_path
            self.config = default_config
            
            return config_path
        except Exception as e:
            self.logger.error(f"Failed to create default configuration: {e}")
            raise
    
    def _add_config_comments(self, config: Dict) -> Dict:
        """Add comments to configuration for better documentation."""
        # In a real implementation, this would add helpful comments
        # For JSON, we can add a "_comments" section
        commented = config.copy()
        commented["_comments"] = {
            "version": "Configuration version for compatibility checking",
            "analyzer": {
                "deep_analysis": "Enable comprehensive analysis (slower but more thorough)",
                "include_hidden_files": "Include hidden files in analysis",
                "max_file_size_mb": "Maximum file size to analyze in MB",
                "excluded_extensions": "File extensions to skip during analysis",
                "duplicate_threshold_mb": "Minimum file size for duplicate detection"
            },
            "organizer": {
                "create_backups": "Create backups before organizing files",
                "backup_directory": "Directory name for backups",
                "max_filename_length": "Maximum allowed filename length",
                "naming_separator": "Character to use for separating words in filenames",
                "preserve_timestamps": "Keep original file timestamps",
                "safe_mode": "Enable additional safety checks"
            },
            "layout": {
                "default_theme": "Default visual theme (professional, modern, minimal, colorful)",
                "auto_apply_icons": "Automatically apply folder icons",
                "create_templates": "Create layout templates",
                "enable_auto_organization": "Enable automatic file organization",
                "folder_color_coding": "Apply color coding to folders"
            },
            "cloud": {
                "default_strategy": "Default sync strategy (smart, mirror, backup, selective)",
                "cache_size_mb": "Virtual memory cache size in MB",
                "auto_sync": "Enable automatic synchronization",
                "bandwidth_limit_mbps": "Bandwidth limit in Mbps (0 = unlimited)",
                "conflict_resolution": "How to handle conflicts (prompt, latest_wins, keep_both)"
            }
        }
        return commented
    
    def validate_config(self) -> Tuple[bool, List[str]]:
        """Validate current configuration."""
        errors = []
        
        # Check required fields
        required_sections = ['analyzer', 'organizer', 'layout', 'cloud']
        for section in required_sections:
            if section not in self.config:
                errors.append(f"Missing required section: {section}")
        
        # Validate analyzer settings
        analyzer_config = self.config.get('analyzer', {})
        if 'max_file_size_mb' in analyzer_config:
            if not isinstance(analyzer_config['max_file_size_mb'], (int, float)) or analyzer_config['max_file_size_mb'] <= 0:
                errors.append("analyzer.max_file_size_mb must be a positive number")
        
        # Validate organizer settings
        organizer_config = self.config.get('organizer', {})
        if 'max_filename_length' in organizer_config:
            if not isinstance(organizer_config['max_filename_length'], int) or organizer_config['max_filename_length'] <= 0:
                errors.append("organizer.max_filename_length must be a positive integer")
        
        # Validate layout settings
        layout_config = self.config.get('layout', {})
        if 'default_theme' in layout_config:
            valid_themes = ['professional', 'modern', 'minimal', 'colorful']
            if layout_config['default_theme'] not in valid_themes:
                errors.append(f"layout.default_theme must be one of: {', '.join(valid_themes)}")
        
        # Validate cloud settings
        cloud_config = self.config.get('cloud', {})
        if 'default_strategy' in cloud_config:
            valid_strategies = ['smart', 'mirror', 'backup', 'selective']
            if cloud_config['default_strategy'] not in valid_strategies:
                errors.append(f"cloud.default_strategy must be one of: {', '.join(valid_strategies)}")
        
        if 'cache_size_mb' in cloud_config:
            if not isinstance(cloud_config['cache_size_mb'], int) or cloud_config['cache_size_mb'] <= 0:
                errors.append("cloud.cache_size_mb must be a positive integer")
        
        # Validate cloud provider configurations
        providers = cloud_config.get('providers', {})
        for provider_name, provider_config in providers.items():
            if not isinstance(provider_config, dict):
                errors.append(f"cloud.providers.{provider_name} must be an object")
                continue
            
            if 'enabled' not in provider_config:
                errors.append(f"cloud.providers.{provider_name} missing 'enabled' field")
        
        # Validate performance settings
        performance_config = self.config.get('performance', {})
        if 'max_workers' in performance_config:
            if not isinstance(performance_config['max_workers'], int) or performance_config['max_workers'] <= 0:
                errors.append("performance.max_workers must be a positive integer")
        
        if 'memory_limit_mb' in performance_config:
            if not isinstance(performance_config['memory_limit_mb'], int) or performance_config['memory_limit_mb'] <= 0:
                errors.append("performance.memory_limit_mb must be a positive integer")
        
        return len(errors) == 0, errors
    
    def update_config(self, updates: Dict) -> None:
        """Update configuration with new values."""
        def deep_update(original: Dict, updates: Dict) -> Dict:
            """Recursively update nested dictionaries."""
            for key, value in updates.items():
                if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                    deep_update(original[key], value)
                else:
                    original[key] = value
            return original
        
        deep_update(self.config, updates)
    
    def get_section(self, section_name: str) -> Dict:
        """Get a specific configuration section."""
        return self.config.get(section_name, {})
    
    def set_section(self, section_name: str, section_config: Dict) -> None:
        """Set a specific configuration section."""
        self.config[section_name] = section_config
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = self._get_default_config()
    
    def export_config(self, output_path: str, format_type: str = 'json') -> None:
        """Export configuration to file."""
        output_path = Path(output_path)
        
        if format_type == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        elif format_type == 'yaml':
            try:
                import yaml
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            except ImportError:
                raise ImportError("PyYAML is required for YAML export")
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def import_config(self, input_path: str, format_type: str = 'json') -> None:
        """Import configuration from file."""
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {input_path}")
        
        if format_type == 'json':
            with open(input_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
        
        elif format_type == 'yaml':
            try:
                import yaml
                with open(input_path, 'r', encoding='utf-8') as f:
                    imported_config = yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML is required for YAML import")
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
        
        # Validate imported configuration
        old_config = self.config.copy()
        self.config = imported_config
        
        is_valid, errors = self.validate_config()
        if not is_valid:
            # Restore old configuration
            self.config = old_config
            raise ValueError(f"Invalid configuration: {'; '.join(errors)}")
    
    def get_cloud_provider_config(self, provider_name: str) -> Dict:
        """Get configuration for a specific cloud provider."""
        return self.config.get('cloud', {}).get('providers', {}).get(provider_name, {})
    
    def is_cloud_provider_enabled(self, provider_name: str) -> bool:
        """Check if a cloud provider is enabled."""
        provider_config = self.get_cloud_provider_config(provider_name)
        return provider_config.get('enabled', False)
    
    def enable_cloud_provider(self, provider_name: str, provider_config: Dict) -> None:
        """Enable and configure a cloud provider."""
        if 'cloud' not in self.config:
            self.config['cloud'] = {}
        if 'providers' not in self.config['cloud']:
            self.config['cloud']['providers'] = {}
        
        self.config['cloud']['providers'][provider_name] = {
            'enabled': True,
            **provider_config
        }
    
    def disable_cloud_provider(self, provider_name: str) -> None:
        """Disable a cloud provider."""
        if provider_name in self.config.get('cloud', {}).get('providers', {}):
            self.config['cloud']['providers'][provider_name]['enabled'] = False