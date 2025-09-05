"""
System Analyzer Module

Analyzes the computer system comprehensively, including:
- Disk usage and storage analysis
- File type distribution
- Duplicate file detection
- System resource utilization
- Directory structure analysis
"""

import os
import sys
import hashlib
import psutil
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional
import time
import logging

class SystemAnalyzer:
    """Comprehensive system analyzer for file organization insights."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the system analyzer."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.analysis_results = {}
        
    def analyze_complete_system(self, target_paths: Optional[List[str]] = None) -> Dict:
        """
        Perform complete system analysis.
        
        Args:
            target_paths: Specific paths to analyze. If None, analyzes common user directories.
            
        Returns:
            Dictionary containing comprehensive analysis results.
        """
        if target_paths is None:
            target_paths = self._get_default_analysis_paths()
            
        self.logger.info("Starting comprehensive system analysis...")
        
        results = {
            'system_info': self._get_system_info(),
            'disk_usage': self._analyze_disk_usage(),
            'file_analysis': {},
            'duplicates': {},
            'directory_structure': {},
            'recommendations': []
        }
        
        for path in target_paths:
            if os.path.exists(path):
                self.logger.info(f"Analyzing path: {path}")
                results['file_analysis'][path] = self._analyze_path(path)
                results['duplicates'][path] = self._find_duplicates(path)
                results['directory_structure'][path] = self._analyze_directory_structure(path)
        
        results['recommendations'] = self._generate_recommendations(results)
        self.analysis_results = results
        
        return results
    
    def _get_default_analysis_paths(self) -> List[str]:
        """Get default paths for analysis based on the operating system."""
        paths = []
        
        if sys.platform == "win32":
            # Windows paths
            user_profile = os.environ.get('USERPROFILE', '')
            if user_profile:
                paths.extend([
                    os.path.join(user_profile, 'Desktop'),
                    os.path.join(user_profile, 'Documents'),
                    os.path.join(user_profile, 'Downloads'),
                    os.path.join(user_profile, 'Pictures'),
                    os.path.join(user_profile, 'Videos'),
                    os.path.join(user_profile, 'Music'),
                ])
        else:
            # Unix-like systems (Linux, macOS)
            home = os.path.expanduser('~')
            paths.extend([
                os.path.join(home, 'Desktop'),
                os.path.join(home, 'Documents'),
                os.path.join(home, 'Downloads'),
                os.path.join(home, 'Pictures'),
                os.path.join(home, 'Videos'),
                os.path.join(home, 'Music'),
            ])
        
        return [p for p in paths if os.path.exists(p)]
    
    def _get_system_info(self) -> Dict:
        """Get basic system information."""
        return {
            'platform': sys.platform,
            'python_version': sys.version,
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'boot_time': psutil.boot_time(),
        }
    
    def _analyze_disk_usage(self) -> Dict:
        """Analyze disk usage across all mounted drives."""
        disk_info = {}
        
        # Get all disk partitions
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    'mountpoint': partition.mountpoint,
                    'file_system': partition.fstype,
                    'total': partition_usage.total,
                    'used': partition_usage.used,
                    'free': partition_usage.free,
                    'percentage': (partition_usage.used / partition_usage.total) * 100
                }
            except PermissionError:
                # This can happen on Windows
                self.logger.warning(f"Permission denied accessing {partition.device}")
                continue
                
        return disk_info
    
    def _analyze_path(self, path: str) -> Dict:
        """Analyze a specific path for file distribution and characteristics."""
        path_obj = Path(path)
        analysis = {
            'total_files': 0,
            'total_size': 0,
            'file_types': Counter(),
            'size_distribution': defaultdict(int),
            'large_files': [],  # Files larger than 100MB
            'old_files': [],    # Files older than 2 years
            'recent_files': []  # Files modified in last 30 days
        }
        
        current_time = time.time()
        thirty_days_ago = current_time - (30 * 24 * 60 * 60)
        two_years_ago = current_time - (2 * 365 * 24 * 60 * 60)
        
        try:
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    try:
                        stat = file_path.stat()
                        file_size = stat.st_size
                        mod_time = stat.st_mtime
                        
                        analysis['total_files'] += 1
                        analysis['total_size'] += file_size
                        
                        # File type analysis
                        suffix = file_path.suffix.lower()
                        analysis['file_types'][suffix or 'no_extension'] += 1
                        
                        # Size distribution
                        if file_size < 1024:  # < 1KB
                            analysis['size_distribution']['< 1KB'] += 1
                        elif file_size < 1024 * 1024:  # < 1MB
                            analysis['size_distribution']['1KB - 1MB'] += 1
                        elif file_size < 100 * 1024 * 1024:  # < 100MB
                            analysis['size_distribution']['1MB - 100MB'] += 1
                        else:  # >= 100MB
                            analysis['size_distribution']['> 100MB'] += 1
                            analysis['large_files'].append({
                                'path': str(file_path),
                                'size': file_size
                            })
                        
                        # Time-based analysis
                        if mod_time > thirty_days_ago:
                            analysis['recent_files'].append(str(file_path))
                        elif mod_time < two_years_ago:
                            analysis['old_files'].append(str(file_path))
                            
                    except (OSError, PermissionError):
                        continue
                        
        except PermissionError:
            self.logger.warning(f"Permission denied accessing {path}")
        
        return analysis
    
    def _find_duplicates(self, path: str) -> Dict:
        """Find duplicate files in the given path."""
        path_obj = Path(path)
        size_groups = defaultdict(list)
        duplicates = {}
        
        # Group files by size first (quick elimination)
        try:
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    try:
                        file_size = file_path.stat().st_size
                        size_groups[file_size].append(file_path)
                    except (OSError, PermissionError):
                        continue
        except PermissionError:
            self.logger.warning(f"Permission denied accessing {path}")
            return duplicates
        
        # Check files with same size for actual duplicates
        for size, files in size_groups.items():
            if len(files) > 1:
                hash_groups = defaultdict(list)
                
                for file_path in files:
                    try:
                        file_hash = self._calculate_file_hash(file_path)
                        hash_groups[file_hash].append(str(file_path))
                    except (OSError, PermissionError):
                        continue
                
                for file_hash, file_list in hash_groups.items():
                    if len(file_list) > 1:
                        duplicates[file_hash] = {
                            'files': file_list,
                            'size': size,
                            'total_wasted_space': size * (len(file_list) - 1)
                        }
        
        return duplicates
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _analyze_directory_structure(self, path: str) -> Dict:
        """Analyze directory structure and organization."""
        path_obj = Path(path)
        structure = {
            'total_directories': 0,
            'max_depth': 0,
            'empty_directories': [],
            'deeply_nested': [],  # Directories with depth > 5
            'large_directories': []  # Directories with > 1000 files
        }
        
        try:
            for dir_path in path_obj.rglob('*'):
                if dir_path.is_dir():
                    structure['total_directories'] += 1
                    
                    # Calculate depth
                    depth = len(dir_path.relative_to(path_obj).parts)
                    structure['max_depth'] = max(structure['max_depth'], depth)
                    
                    if depth > 5:
                        structure['deeply_nested'].append(str(dir_path))
                    
                    # Check if empty
                    try:
                        if not any(dir_path.iterdir()):
                            structure['empty_directories'].append(str(dir_path))
                        else:
                            # Count files in directory
                            file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())
                            if file_count > 1000:
                                structure['large_directories'].append({
                                    'path': str(dir_path),
                                    'file_count': file_count
                                })
                    except (OSError, PermissionError):
                        continue
                        
        except PermissionError:
            self.logger.warning(f"Permission denied accessing {path}")
        
        return structure
    
    def _generate_recommendations(self, analysis_results: Dict) -> List[str]:
        """Generate organization recommendations based on analysis."""
        recommendations = []
        
        # Disk space recommendations
        for device, disk_info in analysis_results['disk_usage'].items():
            if disk_info['percentage'] > 90:
                recommendations.append(f"Critical: Disk {device} is {disk_info['percentage']:.1f}% full. Urgent cleanup needed.")
            elif disk_info['percentage'] > 80:
                recommendations.append(f"Warning: Disk {device} is {disk_info['percentage']:.1f}% full. Consider cleanup.")
        
        # Duplicate file recommendations
        total_wasted_space = 0
        total_duplicates = 0
        for path, duplicates in analysis_results['duplicates'].items():
            for dup_hash, dup_info in duplicates.items():
                total_wasted_space += dup_info['total_wasted_space']
                total_duplicates += len(dup_info['files']) - 1
        
        if total_duplicates > 0:
            recommendations.append(f"Found {total_duplicates} duplicate files wasting {self._format_size(total_wasted_space)} of space.")
        
        # File organization recommendations
        for path, file_analysis in analysis_results['file_analysis'].items():
            if len(file_analysis['large_files']) > 0:
                recommendations.append(f"Consider moving {len(file_analysis['large_files'])} large files from {path} to external storage.")
            
            if len(file_analysis['old_files']) > 10:
                recommendations.append(f"Archive {len(file_analysis['old_files'])} old files from {path} to save space.")
        
        # Directory structure recommendations
        for path, dir_structure in analysis_results['directory_structure'].items():
            if len(dir_structure['empty_directories']) > 5:
                recommendations.append(f"Remove {len(dir_structure['empty_directories'])} empty directories in {path}.")
            
            if dir_structure['max_depth'] > 8:
                recommendations.append(f"Simplify deeply nested directory structure in {path} (max depth: {dir_structure['max_depth']}).")
        
        return recommendations
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def export_analysis(self, output_path: str) -> None:
        """Export analysis results to a file."""
        import json
        
        # Convert analysis results to JSON-serializable format
        exportable_results = self._make_json_serializable(self.analysis_results)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(exportable_results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Analysis results exported to {output_path}")
    
    def _make_json_serializable(self, obj):
        """Convert objects to JSON-serializable format."""
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, (Counter, defaultdict)):
            return dict(obj)
        else:
            return obj