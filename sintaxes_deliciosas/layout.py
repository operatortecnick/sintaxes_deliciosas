"""
Layout Manager Module

Creates and manages professional, clean, and dynamic layouts with:
- Theme-based visual organization
- Dynamic folder icons and colors
- Professional naming conventions
- Visual hierarchy optimization
- Cross-platform compatibility
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import platform
import subprocess

class LayoutManager:
    """Professional layout manager for creating clean and dynamic file structures."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the layout manager."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.current_theme = self.config.get('theme', 'professional')
        self.platform = platform.system().lower()
        
    def apply_professional_layout(self, target_path: str, theme: str = 'professional') -> Dict:
        """
        Apply professional layout styling to a directory structure.
        
        Args:
            target_path: Path to apply layout
            theme: Layout theme ('professional', 'modern', 'minimal', 'colorful')
            
        Returns:
            Dictionary with layout application results
        """
        target_path = Path(target_path)
        self.current_theme = theme
        
        self.logger.info(f"Applying {theme} layout to {target_path}")
        
        results = {
            'theme_applied': theme,
            'target_path': str(target_path),
            'icons_set': 0,
            'colors_applied': 0,
            'layouts_created': 0,
            'platform': self.platform,
            'features_applied': []
        }
        
        # Apply theme-specific configurations
        theme_config = self._get_theme_config(theme)
        
        # Set folder icons and colors
        if theme_config.get('folder_customization', True):
            self._apply_folder_customization(target_path, theme_config)
            results['features_applied'].append('folder_customization')
        
        # Create visual hierarchy
        if theme_config.get('visual_hierarchy', True):
            self._create_visual_hierarchy(target_path, theme_config)
            results['features_applied'].append('visual_hierarchy')
        
        # Apply naming conventions
        if theme_config.get('professional_naming', True):
            self._apply_professional_naming(target_path, theme_config)
            results['features_applied'].append('professional_naming')
        
        # Create layout templates
        if theme_config.get('layout_templates', True):
            self._create_layout_templates(target_path, theme_config)
            results['features_applied'].append('layout_templates')
        
        # Set up auto-organization rules
        if theme_config.get('auto_organization', True):
            self._setup_auto_organization(target_path, theme_config)
            results['features_applied'].append('auto_organization')
        
        # Platform-specific optimizations
        self._apply_platform_optimizations(target_path, theme_config)
        results['features_applied'].append('platform_optimizations')
        
        return results
    
    def _get_theme_config(self, theme: str) -> Dict:
        """Get configuration for specific theme."""
        themes = {
            'professional': {
                'folder_customization': True,
                'visual_hierarchy': True,
                'professional_naming': True,
                'layout_templates': True,
                'auto_organization': True,
                'color_scheme': {
                    'primary': '#2C3E50',      # Dark blue-gray
                    'secondary': '#3498DB',    # Blue
                    'accent': '#E74C3C',       # Red
                    'success': '#27AE60',      # Green
                    'warning': '#F39C12',      # Orange
                    'neutral': '#95A5A6'       # Gray
                },
                'folder_icons': {
                    'Work': '💼',
                    'Personal': '🏠',
                    'Projects': '📁',
                    'Documents': '📄',
                    'Archive': '📦',
                    'Temp': '🗂️',
                    'Media': '🎬',
                    'Software': '💻'
                },
                'priority_colors': {
                    1: '#E74C3C',  # High priority - Red
                    2: '#F39C12',  # Medium priority - Orange
                    3: '#3498DB',  # Normal priority - Blue
                    4: '#27AE60',  # Low priority - Green
                    5: '#95A5A6'   # Archive - Gray
                }
            },
            'modern': {
                'folder_customization': True,
                'visual_hierarchy': True,
                'professional_naming': True,
                'layout_templates': True,
                'auto_organization': True,
                'color_scheme': {
                    'primary': '#1A1A1A',      # Deep black
                    'secondary': '#007ACC',    # Modern blue
                    'accent': '#FF6B6B',       # Coral
                    'success': '#4ECDC4',      # Teal
                    'warning': '#FFE66D',      # Yellow
                    'neutral': '#A8A8A8'       # Light gray
                },
                'folder_icons': {
                    'Work': '🚀',
                    'Personal': '✨',
                    'Projects': '⚡',
                    'Documents': '📋',
                    'Archive': '🗄️',
                    'Temp': '⏳',
                    'Media': '🎨',
                    'Software': '⚙️'
                }
            },
            'minimal': {
                'folder_customization': False,
                'visual_hierarchy': True,
                'professional_naming': True,
                'layout_templates': False,
                'auto_organization': True,
                'color_scheme': {
                    'primary': '#FFFFFF',
                    'secondary': '#F8F9FA',
                    'accent': '#6C757D',
                    'neutral': '#E9ECEF'
                },
                'folder_icons': {}  # No icons for minimal theme
            },
            'colorful': {
                'folder_customization': True,
                'visual_hierarchy': True,
                'professional_naming': True,
                'layout_templates': True,
                'auto_organization': True,
                'color_scheme': {
                    'primary': '#FF5722',      # Deep orange
                    'secondary': '#4CAF50',    # Green
                    'accent': '#9C27B0',       # Purple
                    'success': '#00BCD4',      # Cyan
                    'warning': '#FF9800',      # Orange
                    'neutral': '#607D8B'       # Blue gray
                },
                'folder_icons': {
                    'Work': '🔥',
                    'Personal': '🌈',
                    'Projects': '🎯',
                    'Documents': '📊',
                    'Archive': '🎪',
                    'Temp': '🎨',
                    'Media': '🎭',
                    'Software': '🔧'
                }
            }
        }
        
        return themes.get(theme, themes['professional'])
    
    def _apply_folder_customization(self, target_path: Path, theme_config: Dict) -> None:
        """Apply folder icons and colors based on theme."""
        folder_icons = theme_config.get('folder_icons', {})
        
        for folder_path in target_path.rglob('*'):
            if folder_path.is_dir():
                folder_name = folder_path.name
                
                # Apply icon if available
                if folder_name in folder_icons:
                    self._set_folder_icon(folder_path, folder_icons[folder_name])
                
                # Apply color based on folder type
                self._set_folder_color(folder_path, theme_config)
    
    def _set_folder_icon(self, folder_path: Path, icon: str) -> None:
        """Set folder icon (platform-specific implementation)."""
        try:
            if self.platform == 'windows':
                # Windows: Create desktop.ini file
                desktop_ini_path = folder_path / 'desktop.ini'
                desktop_ini_content = f"""[.ShellClassInfo]
IconResource={icon}
[ViewState]
Mode=
Vid=
FolderType=Generic
"""
                with open(desktop_ini_path, 'w', encoding='utf-8') as f:
                    f.write(desktop_ini_content)
                
                # Hide the desktop.ini file
                if self.platform == 'windows':
                    subprocess.run(['attrib', '+h', str(desktop_ini_path)], 
                                 capture_output=True, text=True)
                
            elif self.platform == 'darwin':  # macOS
                # macOS: Use extended attributes
                try:
                    subprocess.run(['xattr', '-w', 'com.apple.FinderInfo', 
                                  icon.encode('utf-8').hex(), str(folder_path)],
                                 capture_output=True, text=True)
                except FileNotFoundError:
                    # xattr not available
                    pass
                
            elif self.platform == 'linux':
                # Linux: Create .directory file
                directory_file_path = folder_path / '.directory'
                directory_content = f"""[Desktop Entry]
Icon={icon}
"""
                with open(directory_file_path, 'w', encoding='utf-8') as f:
                    f.write(directory_content)
        
        except Exception as e:
            self.logger.debug(f"Could not set icon for {folder_path}: {e}")
    
    def _set_folder_color(self, folder_path: Path, theme_config: Dict) -> None:
        """Set folder color based on theme and folder type."""
        folder_name = folder_path.name.lower()
        color_scheme = theme_config.get('color_scheme', {})
        
        # Determine color based on folder type
        if 'work' in folder_name or 'project' in folder_name:
            color = color_scheme.get('primary')
        elif 'archive' in folder_name or 'backup' in folder_name:
            color = color_scheme.get('neutral')
        elif 'temp' in folder_name or 'cache' in folder_name:
            color = color_scheme.get('warning')
        elif 'personal' in folder_name:
            color = color_scheme.get('success')
        else:
            color = color_scheme.get('secondary')
        
        if color:
            self._apply_folder_color(folder_path, color)
    
    def _apply_folder_color(self, folder_path: Path, color: str) -> None:
        """Apply color to folder (platform-specific)."""
        try:
            if self.platform == 'darwin':  # macOS
                # macOS: Use tags
                subprocess.run(['tag', '-a', color, str(folder_path)],
                             capture_output=True, text=True)
            
            elif self.platform == 'linux':
                # Linux: Update .directory file with color
                directory_file_path = folder_path / '.directory'
                if directory_file_path.exists():
                    content = directory_file_path.read_text()
                    if 'Icon=' not in content:
                        content += f"\nIcon=folder\nColor={color}\n"
                    else:
                        content += f"\nColor={color}\n"
                    directory_file_path.write_text(content)
        
        except Exception as e:
            self.logger.debug(f"Could not set color for {folder_path}: {e}")
    
    def _create_visual_hierarchy(self, target_path: Path, theme_config: Dict) -> None:
        """Create visual hierarchy with numbered prefixes and organization."""
        priority_mapping = {
            'Work': 1,
            'Projects': 1,
            'Active': 1,
            'Personal': 2,
            'Documents': 2,
            'Media': 3,
            'Software': 3,
            'Archive': 4,
            'Temp': 5,
            'Cache': 5
        }
        
        # Apply priority prefixes to main directories
        for folder_path in target_path.iterdir():
            if folder_path.is_dir():
                folder_name = folder_path.name
                
                # Skip already numbered folders
                if folder_name[0].isdigit():
                    continue
                
                priority = priority_mapping.get(folder_name, 3)
                new_name = f"{priority:02d}_{folder_name}"
                new_path = folder_path.parent / new_name
                
                try:
                    folder_path.rename(new_path)
                    self.logger.debug(f"Renamed {folder_name} to {new_name}")
                except OSError as e:
                    self.logger.warning(f"Could not rename {folder_name}: {e}")
    
    def _apply_professional_naming(self, target_path: Path, theme_config: Dict) -> None:
        """Apply professional naming conventions."""
        naming_rules = {
            'replace_spaces': True,
            'lowercase_extensions': True,
            'remove_special_chars': True,
            'max_length': 50,
            'separator': '_'
        }
        
        for item_path in target_path.rglob('*'):
            if item_path.is_file() or item_path.is_dir():
                original_name = item_path.name
                clean_name = self._clean_name(original_name, naming_rules)
                
                if clean_name != original_name:
                    new_path = item_path.parent / clean_name
                    try:
                        if not new_path.exists():
                            item_path.rename(new_path)
                            self.logger.debug(f"Renamed {original_name} to {clean_name}")
                    except OSError as e:
                        self.logger.warning(f"Could not rename {original_name}: {e}")
    
    def _clean_name(self, name: str, rules: Dict) -> str:
        """Clean a file/folder name according to professional standards."""
        import re
        
        # Split name and extension
        path_obj = Path(name)
        stem = path_obj.stem
        suffix = path_obj.suffix
        
        # Replace spaces
        if rules.get('replace_spaces', True):
            stem = stem.replace(' ', rules.get('separator', '_'))
        
        # Remove special characters
        if rules.get('remove_special_chars', True):
            stem = re.sub(r'[^\w\-_.]', '', stem)
        
        # Lowercase extension
        if rules.get('lowercase_extensions', True):
            suffix = suffix.lower()
        
        # Limit length
        max_length = rules.get('max_length', 50)
        if len(stem) > max_length:
            stem = stem[:max_length].rstrip(rules.get('separator', '_'))
        
        # Remove multiple separators
        separator = rules.get('separator', '_')
        stem = re.sub(f'{separator}+', separator, stem)
        stem = stem.strip(separator)
        
        return f"{stem}{suffix}"
    
    def _create_layout_templates(self, target_path: Path, theme_config: Dict) -> None:
        """Create layout templates and documentation."""
        templates_dir = target_path / 'Templates'
        templates_dir.mkdir(exist_ok=True)
        
        # Create various templates
        templates = {
            'Project_Template': {
                'folders': ['01_Planning', '02_Development', '03_Testing', '04_Documentation', '05_Deployment'],
                'files': ['README.md', 'TODO.md', 'CHANGELOG.md']
            },
            'Document_Template': {
                'folders': ['Drafts', 'Final', 'Archive', 'References'],
                'files': ['template.docx', 'checklist.md']
            },
            'Media_Template': {
                'folders': ['Raw', 'Processed', 'Final', 'Archive'],
                'files': ['guidelines.md']
            }
        }
        
        for template_name, template_config in templates.items():
            template_dir = templates_dir / template_name
            template_dir.mkdir(exist_ok=True)
            
            # Create folders
            for folder in template_config.get('folders', []):
                (template_dir / folder).mkdir(exist_ok=True)
            
            # Create template files
            for filename in template_config.get('files', []):
                file_path = template_dir / filename
                if not file_path.exists():
                    content = self._get_template_content(filename, template_name)
                    file_path.write_text(content, encoding='utf-8')
    
    def _get_template_content(self, filename: str, template_type: str) -> str:
        """Get content for template files."""
        templates = {
            'README.md': f"""# {template_type.replace('_', ' ')}

## Overview
Brief description of this {template_type.lower()}.

## Structure
- Organized using professional layout standards
- Follow naming conventions
- Maintain clear hierarchy

## Usage
1. Copy this template to your project location
2. Rename folders and files as needed
3. Follow the established structure

Generated by Sintaxes Deliciosas Layout Manager
""",
            'TODO.md': """# TODO List

## High Priority
- [ ] Task 1
- [ ] Task 2

## Medium Priority
- [ ] Task 3
- [ ] Task 4

## Low Priority
- [ ] Task 5
- [ ] Task 6

## Completed
- [x] Example completed task
""",
            'CHANGELOG.md': """# Changelog

## [Unreleased]
### Added
### Changed
### Fixed

## [1.0.0] - 2024-01-01
### Added
- Initial version
""",
            'guidelines.md': """# Guidelines

## Organization Standards
- Use descriptive names
- Maintain consistent structure
- Archive old files regularly
- Keep documentation updated

## Best Practices
- Regular backups
- Version control for important files
- Clear folder hierarchy
- Professional naming conventions
"""
        }
        
        return templates.get(filename, f"# {filename}\n\nTemplate content for {template_type}")
    
    def _setup_auto_organization(self, target_path: Path, theme_config: Dict) -> None:
        """Set up automatic organization rules."""
        auto_org_config = {
            'watch_folders': ['Downloads', 'Desktop', 'Temp'],
            'rules': {
                'images': {
                    'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
                    'destination': 'Personal/Media/Photos'
                },
                'documents': {
                    'extensions': ['.pdf', '.doc', '.docx', '.txt'],
                    'destination': 'Personal/Documents'
                },
                'archives': {
                    'extensions': ['.zip', '.rar', '.7z'],
                    'destination': 'Software/Archive'
                }
            }
        }
        
        # Save auto-organization configuration
        config_file = target_path / '.organization_config.json'
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(auto_org_config, f, indent=2)
        
        # Hide configuration file on Windows
        if self.platform == 'windows':
            try:
                subprocess.run(['attrib', '+h', str(config_file)], 
                             capture_output=True, text=True)
            except Exception:
                pass
    
    def _apply_platform_optimizations(self, target_path: Path, theme_config: Dict) -> None:
        """Apply platform-specific optimizations."""
        if self.platform == 'windows':
            self._apply_windows_optimizations(target_path)
        elif self.platform == 'darwin':
            self._apply_macos_optimizations(target_path)
        elif self.platform == 'linux':
            self._apply_linux_optimizations(target_path)
    
    def _apply_windows_optimizations(self, target_path: Path) -> None:
        """Apply Windows-specific optimizations."""
        # Create thumbnail cache optimization
        thumbs_db_files = list(target_path.rglob('Thumbs.db'))
        for thumbs_file in thumbs_db_files:
            try:
                thumbs_file.unlink()
            except Exception:
                pass
        
        # Set folder attributes for better performance
        for folder in target_path.rglob('*'):
            if folder.is_dir() and 'Archive' in folder.name:
                try:
                    # Set archive attribute
                    subprocess.run(['attrib', '+a', str(folder)], 
                                 capture_output=True, text=True)
                except Exception:
                    pass
    
    def _apply_macos_optimizations(self, target_path: Path) -> None:
        """Apply macOS-specific optimizations."""
        # Remove .DS_Store files
        ds_store_files = list(target_path.rglob('.DS_Store'))
        for ds_file in ds_store_files:
            try:
                ds_file.unlink()
            except Exception:
                pass
        
        # Set Finder preferences
        for folder in target_path.iterdir():
            if folder.is_dir():
                try:
                    # Set view options
                    subprocess.run(['defaults', 'write', 'com.apple.finder', 
                                  f'FXPreferredViewStyle{folder.name}', 'clmv'],
                                 capture_output=True, text=True)
                except Exception:
                    pass
    
    def _apply_linux_optimizations(self, target_path: Path) -> None:
        """Apply Linux-specific optimizations."""
        # Set appropriate permissions
        for item in target_path.rglob('*'):
            try:
                if item.is_dir():
                    item.chmod(0o755)  # rwxr-xr-x for directories
                elif item.is_file():
                    if item.suffix in ['.sh', '.py', '.pl']:
                        item.chmod(0o755)  # rwxr-xr-x for executables
                    else:
                        item.chmod(0o644)  # rw-r--r-- for regular files
            except Exception:
                pass
    
    def create_dynamic_layout(self, target_path: str, layout_type: str = 'adaptive') -> Dict:
        """Create a dynamic layout that adapts to content."""
        target_path = Path(target_path)
        
        layout_configs = {
            'adaptive': {
                'auto_categorize': True,
                'dynamic_folders': True,
                'smart_naming': True,
                'content_aware': True
            },
            'project_based': {
                'project_structure': True,
                'milestone_tracking': True,
                'resource_management': True
            },
            'time_based': {
                'yearly_archives': True,
                'monthly_organization': True,
                'daily_folders': True
            }
        }
        
        config = layout_configs.get(layout_type, layout_configs['adaptive'])
        
        results = {
            'layout_type': layout_type,
            'target_path': str(target_path),
            'dynamic_features': [],
            'folders_created': 0
        }
        
        if config.get('auto_categorize', False):
            self._setup_auto_categorization(target_path)
            results['dynamic_features'].append('auto_categorization')
        
        if config.get('dynamic_folders', False):
            self._create_dynamic_folders(target_path)
            results['dynamic_features'].append('dynamic_folders')
        
        if config.get('smart_naming', False):
            self._setup_smart_naming(target_path)
            results['dynamic_features'].append('smart_naming')
        
        return results
    
    def _setup_auto_categorization(self, target_path: Path) -> None:
        """Set up automatic categorization based on file content and metadata."""
        # This would integrate with the organizer module for automatic file categorization
        pass
    
    def _create_dynamic_folders(self, target_path: Path) -> None:
        """Create folders that adapt based on content."""
        # Create date-based folders
        from datetime import datetime
        current_date = datetime.now()
        
        # Current year/month structure
        current_path = target_path / str(current_date.year) / f"{current_date.month:02d}_{current_date.strftime('%B')}"
        current_path.mkdir(parents=True, exist_ok=True)
        
        # Next month preparation
        next_month = current_date.replace(day=28) + Path('timedelta')(days=4)
        next_month = next_month.replace(day=1)
        next_path = target_path / str(next_month.year) / f"{next_month.month:02d}_{next_month.strftime('%B')}"
        next_path.mkdir(parents=True, exist_ok=True)
    
    def _setup_smart_naming(self, target_path: Path) -> None:
        """Set up intelligent naming conventions."""
        # Create naming convention documentation
        naming_doc = target_path / '_NAMING_CONVENTIONS.md'
        
        content = """# Smart Naming Conventions

## File Naming Standards
- Use descriptive names
- Include dates in YYYY-MM-DD format
- Use underscores instead of spaces
- Include version numbers: v1.0, v2.1, etc.
- Add status prefixes: DRAFT_, FINAL_, ARCHIVE_

## Folder Naming Standards
- Use numbered prefixes for priority: 01_, 02_, 03_
- Categories in UPPERCASE: PROJECTS, ARCHIVE, TEMP
- Subcategories in Title_Case: Current_Projects, Old_Projects

## Examples
- Documents: 2024-01-15_Meeting_Notes_v1.0.docx
- Projects: 01_ACTIVE_PROJECTS/Website_Redesign/
- Archive: 99_ARCHIVE/2023/Q4_Reports/

This system ensures consistency and easy navigation.
"""
        
        naming_doc.write_text(content, encoding='utf-8')
    
    def export_layout_config(self, target_path: str, output_file: str) -> None:
        """Export current layout configuration."""
        config = {
            'target_path': target_path,
            'theme': self.current_theme,
            'platform': self.platform,
            'created_at': datetime.now().isoformat(),
            'layout_features': self.config
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Layout configuration exported to {output_file}")