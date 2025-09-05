"""
File Organizer Module

Implements intelligent file organization and categorization system with:
- Smart file categorization by type and content
- Automated folder structure creation
- Safe file moving and organization
- Professional naming conventions
- Backup and rollback capabilities
"""

import os
import shutil
import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re
from send2trash import send2trash

class FileOrganizer:
    """Intelligent file organizer with categorization and professional layout."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the file organizer."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.organization_rules = self._load_default_rules()
        self.organized_files = []
        self.backup_info = {}
        
    def _load_default_rules(self) -> Dict:
        """Load default file organization rules."""
        return {
            'categories': {
                'Documents': {
                    'extensions': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.pages'],
                    'keywords': ['document', 'report', 'letter', 'resume', 'cv'],
                    'subdirectories': ['PDFs', 'Word_Documents', 'Text_Files', 'Reports']
                },
                'Images': {
                    'extensions': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
                    'keywords': ['photo', 'image', 'picture', 'screenshot'],
                    'subdirectories': ['Photos', 'Screenshots', 'Graphics', 'Icons']
                },
                'Videos': {
                    'extensions': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v'],
                    'keywords': ['video', 'movie', 'clip', 'recording'],
                    'subdirectories': ['Movies', 'Clips', 'Recordings', 'Tutorials']
                },
                'Audio': {
                    'extensions': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
                    'keywords': ['music', 'audio', 'sound', 'song', 'podcast'],
                    'subdirectories': ['Music', 'Podcasts', 'Sounds', 'Recordings']
                },
                'Archives': {
                    'extensions': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
                    'keywords': ['archive', 'compressed', 'backup'],
                    'subdirectories': ['Compressed', 'Backups', 'Installers']
                },
                'Code': {
                    'extensions': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.c', '.php', '.rb', '.go'],
                    'keywords': ['code', 'script', 'program', 'source'],
                    'subdirectories': ['Python', 'JavaScript', 'Web', 'Projects']
                },
                'Spreadsheets': {
                    'extensions': ['.xls', '.xlsx', '.csv', '.ods', '.numbers'],
                    'keywords': ['spreadsheet', 'data', 'table', 'calculation'],
                    'subdirectories': ['Excel', 'Data', 'Reports']
                },
                'Presentations': {
                    'extensions': ['.ppt', '.pptx', '.odp', '.key'],
                    'keywords': ['presentation', 'slides', 'meeting'],
                    'subdirectories': ['PowerPoint', 'Keynote', 'Meetings']
                },
                'Executables': {
                    'extensions': ['.exe', '.msi', '.dmg', '.app', '.deb', '.rpm'],
                    'keywords': ['installer', 'application', 'software'],
                    'subdirectories': ['Applications', 'Installers', 'Portable']
                }
            },
            'naming_patterns': {
                'date_format': '%Y-%m-%d',
                'separator': '_',
                'max_length': 255,
                'invalid_chars': r'[<>:"/\\|?*]'
            },
            'size_thresholds': {
                'large_file': 100 * 1024 * 1024,  # 100MB
                'huge_file': 1024 * 1024 * 1024   # 1GB
            }
        }
    
    def organize_directory(self, source_path: str, target_path: Optional[str] = None, 
                          dry_run: bool = False) -> Dict:
        """
        Organize files in a directory according to professional standards.
        
        Args:
            source_path: Path to directory to organize
            target_path: Optional target directory. If None, organizes in place
            dry_run: If True, only shows what would be done without actual changes
            
        Returns:
            Dictionary with organization results and statistics
        """
        source_path = Path(source_path)
        if target_path is None:
            target_path = source_path / "Organized"
        else:
            target_path = Path(target_path)
        
        self.logger.info(f"Starting organization of {source_path}")
        
        results = {
            'source_path': str(source_path),
            'target_path': str(target_path),
            'files_processed': 0,
            'files_organized': 0,
            'categories_created': [],
            'errors': [],
            'dry_run': dry_run,
            'organization_plan': [],
            'space_saved': 0
        }
        
        # Create backup info
        backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_info[backup_timestamp] = {
            'source': str(source_path),
            'target': str(target_path),
            'operations': []
        }
        
        # Analyze files first
        files_to_organize = self._scan_files(source_path)
        results['files_processed'] = len(files_to_organize)
        
        # Create organization plan
        organization_plan = self._create_organization_plan(files_to_organize, target_path)
        results['organization_plan'] = organization_plan
        
        if not dry_run:
            # Create target directory structure
            self._create_directory_structure(target_path, organization_plan)
            results['categories_created'] = list(organization_plan.keys())
            
            # Organize files
            for category, file_list in organization_plan.items():
                for file_info in file_list:
                    try:
                        self._organize_file(file_info, target_path, category, backup_timestamp)
                        results['files_organized'] += 1
                    except Exception as e:
                        error_msg = f"Error organizing {file_info['path']}: {str(e)}"
                        self.logger.error(error_msg)
                        results['errors'].append(error_msg)
        
        # Clean up empty directories
        if not dry_run:
            self._cleanup_empty_directories(source_path)
        
        self.logger.info(f"Organization complete. Processed {results['files_processed']} files, organized {results['files_organized']}")
        return results
    
    def _scan_files(self, path: Path) -> List[Dict]:
        """Scan directory and collect file information."""
        files = []
        
        try:
            for file_path in path.rglob('*'):
                if file_path.is_file():
                    try:
                        stat = file_path.stat()
                        file_info = {
                            'path': str(file_path),
                            'name': file_path.name,
                            'stem': file_path.stem,
                            'suffix': file_path.suffix.lower(),
                            'size': stat.st_size,
                            'modified': stat.st_mtime,
                            'relative_path': file_path.relative_to(path)
                        }
                        files.append(file_info)
                    except (OSError, PermissionError) as e:
                        self.logger.warning(f"Cannot access {file_path}: {e}")
                        continue
        except PermissionError as e:
            self.logger.error(f"Permission denied accessing {path}: {e}")
        
        return files
    
    def _create_organization_plan(self, files: List[Dict], target_path: Path) -> Dict:
        """Create organization plan by categorizing files."""
        plan = {}
        
        for file_info in files:
            category = self._categorize_file(file_info)
            
            if category not in plan:
                plan[category] = []
            
            # Add organized file path
            file_info['organized_path'] = self._generate_organized_path(
                file_info, target_path, category
            )
            
            plan[category].append(file_info)
        
        return plan
    
    def _categorize_file(self, file_info: Dict) -> str:
        """Categorize a file based on extension, name, and content."""
        extension = file_info['suffix']
        filename = file_info['name'].lower()
        
        # Check each category
        for category, rules in self.organization_rules['categories'].items():
            # Check extension
            if extension in rules['extensions']:
                return category
            
            # Check keywords in filename
            for keyword in rules.get('keywords', []):
                if keyword in filename:
                    return category
        
        # Special handling for specific cases
        if file_info['size'] > self.organization_rules['size_thresholds']['huge_file']:
            return 'Large_Files'
        
        # Check for system/hidden files
        if filename.startswith('.') or filename.startswith('~'):
            return 'System_Files'
        
        # Default category
        return 'Miscellaneous'
    
    def _generate_organized_path(self, file_info: Dict, target_path: Path, category: str) -> str:
        """Generate organized file path with professional naming."""
        # Create category subdirectory
        category_path = target_path / category
        
        # Determine subdirectory based on file characteristics
        subdirectory = self._get_subdirectory(file_info, category)
        if subdirectory:
            category_path = category_path / subdirectory
        
        # Generate clean filename
        clean_filename = self._generate_clean_filename(file_info)
        
        return str(category_path / clean_filename)
    
    def _get_subdirectory(self, file_info: Dict, category: str) -> Optional[str]:
        """Determine appropriate subdirectory for file."""
        if category in self.organization_rules['categories']:
            rules = self.organization_rules['categories'][category]
            subdirs = rules.get('subdirectories', [])
            
            if not subdirs:
                return None
            
            # File size based sorting
            if file_info['size'] > self.organization_rules['size_thresholds']['large_file']:
                return 'Large_Files'
            
            # Date-based sorting for certain categories
            if category in ['Images', 'Videos', 'Documents']:
                mod_time = datetime.fromtimestamp(file_info['modified'])
                return f"{mod_time.year}/{mod_time.month:02d}"
            
            # Extension-based sorting
            extension = file_info['suffix']
            if extension in ['.jpg', '.jpeg', '.png']:
                return 'Photos'
            elif extension in ['.pdf']:
                return 'PDFs'
            elif extension in ['.mp4', '.avi']:
                return 'Videos'
            
            # Default to first subdirectory
            return subdirs[0] if subdirs else None
        
        return None
    
    def _generate_clean_filename(self, file_info: Dict) -> str:
        """Generate a clean, professional filename."""
        name = file_info['stem']
        extension = file_info['suffix']
        
        # Remove invalid characters
        invalid_chars = self.organization_rules['naming_patterns']['invalid_chars']
        name = re.sub(invalid_chars, '', name)
        
        # Replace spaces and special characters with separator
        separator = self.organization_rules['naming_patterns']['separator']
        name = re.sub(r'[\s\-\.]+', separator, name)
        
        # Remove multiple separators
        name = re.sub(f'{separator}+', separator, name)
        
        # Trim separators from ends
        name = name.strip(separator)
        
        # Ensure reasonable length
        max_length = self.organization_rules['naming_patterns']['max_length'] - len(extension)
        if len(name) > max_length:
            name = name[:max_length].rstrip(separator)
        
        # Add timestamp if name is empty or too generic
        if not name or len(name) < 3 or name.lower() in ['file', 'document', 'image']:
            timestamp = datetime.fromtimestamp(file_info['modified'])
            date_str = timestamp.strftime(self.organization_rules['naming_patterns']['date_format'])
            name = f"{date_str}{separator}{name}" if name else date_str
        
        return f"{name}{extension}"
    
    def _create_directory_structure(self, target_path: Path, organization_plan: Dict) -> None:
        """Create the organized directory structure."""
        for category, files in organization_plan.items():
            category_path = target_path / category
            category_path.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            subdirs = set()
            for file_info in files:
                org_path = Path(file_info['organized_path'])
                subdir_path = org_path.parent
                if subdir_path != category_path:
                    subdirs.add(subdir_path)
            
            for subdir in subdirs:
                subdir.mkdir(parents=True, exist_ok=True)
    
    def _organize_file(self, file_info: Dict, target_path: Path, category: str, backup_id: str) -> None:
        """Move/copy file to organized location."""
        source_path = Path(file_info['path'])
        target_file_path = Path(file_info['organized_path'])
        
        # Ensure target directory exists
        target_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle file conflicts
        if target_file_path.exists():
            target_file_path = self._resolve_file_conflict(target_file_path)
        
        # Record operation for potential rollback
        operation = {
            'type': 'move',
            'source': str(source_path),
            'target': str(target_file_path),
            'category': category
        }
        self.backup_info[backup_id]['operations'].append(operation)
        
        # Move the file
        try:
            shutil.move(str(source_path), str(target_file_path))
            self.organized_files.append(str(target_file_path))
            self.logger.debug(f"Moved {source_path} to {target_file_path}")
        except Exception as e:
            self.logger.error(f"Failed to move {source_path} to {target_file_path}: {e}")
            raise
    
    def _resolve_file_conflict(self, target_path: Path) -> Path:
        """Resolve file naming conflicts."""
        counter = 1
        original_stem = target_path.stem
        suffix = target_path.suffix
        parent = target_path.parent
        
        while target_path.exists():
            new_name = f"{original_stem}_{counter:03d}{suffix}"
            target_path = parent / new_name
            counter += 1
            
            # Prevent infinite loop
            if counter > 999:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_name = f"{original_stem}_{timestamp}{suffix}"
                target_path = parent / new_name
                break
        
        return target_path
    
    def _cleanup_empty_directories(self, path: Path) -> None:
        """Remove empty directories after organization."""
        try:
            for dir_path in sorted(path.rglob('*'), key=lambda p: str(p), reverse=True):
                if dir_path.is_dir() and not any(dir_path.iterdir()):
                    try:
                        dir_path.rmdir()
                        self.logger.debug(f"Removed empty directory: {dir_path}")
                    except OSError:
                        # Directory might not be empty or permission issues
                        pass
        except Exception as e:
            self.logger.warning(f"Error during cleanup: {e}")
    
    def create_professional_layout(self, base_path: str) -> Dict:
        """Create a professional directory layout structure."""
        base_path = Path(base_path)
        
        layout = {
            'Work': {
                'Projects': ['Active', 'Completed', 'Archive'],
                'Documents': ['Contracts', 'Reports', 'Presentations'],
                'Resources': ['Templates', 'References', 'Tools']
            },
            'Personal': {
                'Documents': ['Financial', 'Medical', 'Legal', 'Personal'],
                'Media': ['Photos', 'Videos', 'Music'],
                'Archive': ['2024', '2023', '2022']
            },
            'Software': {
                'Development': ['Projects', 'Libraries', 'Tools'],
                'Applications': ['Installed', 'Portable', 'Installers'],
                'Backup': ['System', 'Projects', 'Documents']
            },
            'Temp': {
                'Downloads': [],
                'Processing': [],
                'Cache': []
            }
        }
        
        created_dirs = []
        
        for main_category, subcategories in layout.items():
            main_path = base_path / main_category
            main_path.mkdir(exist_ok=True)
            created_dirs.append(str(main_path))
            
            for subcategory, subdirs in subcategories.items():
                sub_path = main_path / subcategory
                sub_path.mkdir(exist_ok=True)
                created_dirs.append(str(sub_path))
                
                for subdir in subdirs:
                    subdir_path = sub_path / subdir
                    subdir_path.mkdir(exist_ok=True)
                    created_dirs.append(str(subdir_path))
        
        # Create README files
        self._create_layout_documentation(base_path, layout)
        
        return {
            'layout_created': True,
            'base_path': str(base_path),
            'directories_created': created_dirs,
            'structure': layout
        }
    
    def _create_layout_documentation(self, base_path: Path, layout: Dict) -> None:
        """Create documentation for the professional layout."""
        readme_content = """# Professional File Organization Layout

This directory structure is designed for optimal file organization and productivity.

## Structure Overview:

### Work/
- **Projects/**: Work-related projects
  - Active/: Current projects
  - Completed/: Finished projects
  - Archive/: Old projects for reference

- **Documents/**: Work documents
  - Contracts/: Legal and business documents
  - Reports/: Reports and analyses
  - Presentations/: Slides and presentations

- **Resources/**: Work resources
  - Templates/: Document templates
  - References/: Reference materials
  - Tools/: Utilities and tools

### Personal/
- **Documents/**: Personal documents organized by type
- **Media/**: Personal media files
- **Archive/**: Yearly archives

### Software/
- **Development/**: Programming and development files
- **Applications/**: Software and applications
- **Backup/**: Backup files

### Temp/
- **Downloads/**: Temporary downloads
- **Processing/**: Files being processed
- **Cache/**: Temporary cache files

## Usage Guidelines:
1. Always save files in appropriate categories
2. Use descriptive filenames with dates when relevant
3. Archive old files annually
4. Clean temp directories regularly
5. Backup important files

Generated by Sintaxes Deliciosas File Organizer
"""
        
        readme_path = base_path / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def rollback_organization(self, backup_id: str) -> Dict:
        """Rollback file organization using backup information."""
        if backup_id not in self.backup_info:
            raise ValueError(f"Backup ID {backup_id} not found")
        
        backup = self.backup_info[backup_id]
        results = {
            'backup_id': backup_id,
            'files_restored': 0,
            'errors': []
        }
        
        # Reverse the operations
        for operation in reversed(backup['operations']):
            try:
                if operation['type'] == 'move':
                    # Move file back to original location
                    target_path = Path(operation['target'])
                    source_path = Path(operation['source'])
                    
                    if target_path.exists():
                        # Ensure source directory exists
                        source_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(target_path), str(source_path))
                        results['files_restored'] += 1
                
            except Exception as e:
                error_msg = f"Error restoring {operation['source']}: {str(e)}"
                self.logger.error(error_msg)
                results['errors'].append(error_msg)
        
        return results
    
    def export_organization_plan(self, plan: Dict, output_path: str) -> None:
        """Export organization plan to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info(f"Organization plan exported to {output_path}")