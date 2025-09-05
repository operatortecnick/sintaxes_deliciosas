# Sintaxes Deliciosas 🚀

**Supreme Computer Analyzer and File Organization System**

A comprehensive Python tool that analyzes your computer system, suggests and applies file organization improvements, and creates professional, clean, and dynamic layouts with cloud integration and virtual memory optimization.

## ✨ Features

### 🔍 System Analysis
- **Complete system scanning** - Analyzes disk usage, file types, and directory structures
- **Duplicate file detection** - Finds and manages duplicate files across your system
- **Storage optimization** - Identifies large files and suggests space-saving improvements
- **Performance insights** - Provides recommendations for system optimization

### 📁 Intelligent File Organization
- **Smart categorization** - Automatically categorizes files by type, content, and metadata
- **Professional naming** - Applies consistent, professional naming conventions
- **Safe organization** - Creates backups and provides rollback capabilities
- **Custom rules** - Flexible organization rules and patterns

### 🎨 Professional Layout Management
- **Multiple themes** - Professional, Modern, Minimal, and Colorful themes
- **Visual hierarchy** - Creates organized folder structures with priority numbering
- **Cross-platform** - Works on Windows, macOS, and Linux with platform-specific optimizations
- **Dynamic layouts** - Adaptive layouts that adjust to content and usage patterns

### ☁️ Cloud Integration & Virtual Memory
- **Multi-cloud support** - Integrates with Dropbox, Google Drive, OneDrive, AWS S3
- **Smart synchronization** - Intelligent sync strategies with conflict resolution
- **Virtual memory optimization** - Efficient caching and memory management
- **Bandwidth optimization** - Adaptive bandwidth usage and compression

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/operatortecnick/sintaxes_deliciosas.git
cd sintaxes_deliciosas

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

```bash
# Analyze your system
sintaxes-deliciosas analyze /path/to/directory

# Organize files with professional layout
sintaxes-deliciosas organize /path/to/messy/folder --theme professional

# Create a complete professional structure
sintaxes-deliciosas layout /path/to/new/structure --theme modern --dynamic

# Set up cloud integration
sintaxes-deliciosas cloud /path/to/sync --providers dropbox google_drive --optimize

# Complete system optimization
sintaxes-deliciosas complete /path/to/organize --theme professional --cloud-providers local_cloud
```

## 📚 Detailed Usage

### System Analysis

Analyze your computer system to understand file distribution and identify optimization opportunities:

```bash
# Basic analysis
sintaxes-deliciosas analyze ~/Documents

# Deep analysis with output
sintaxes-deliciosas analyze ~/Documents --deep --output analysis_report.json --format json

# Analyze multiple directories
sintaxes-deliciosas analyze ~/Documents ~/Downloads ~/Desktop
```

### File Organization

Organize files using intelligent categorization:

```bash
# Organize in place
sintaxes-deliciosas organize ~/Downloads

# Organize to specific target with theme
sintaxes-deliciosas organize ~/Downloads --target ~/Organized --theme professional

# Preview changes without applying
sintaxes-deliciosas organize ~/Downloads --dry-run

# Create backup before organizing
sintaxes-deliciosas organize ~/Downloads --backup
```

### Professional Layouts

Create professional directory structures:

```bash
# Create professional layout
sintaxes-deliciosas layout ~/WorkSpace --theme professional --templates

# Create dynamic adaptive layout
sintaxes-deliciosas layout ~/Projects --dynamic

# Available themes: professional, modern, minimal, colorful
sintaxes-deliciosas layout ~/Creative --theme colorful
```

### Cloud Integration

Set up cloud synchronization and virtual memory optimization:

```bash
# Set up local cloud simulation
sintaxes-deliciosas cloud ~/Documents --providers local_cloud

# Configure multiple cloud providers
sintaxes-deliciosas cloud ~/Documents --providers dropbox onedrive --strategy smart

# Optimize cloud storage
sintaxes-deliciosas cloud ~/Documents --optimize --cache-size 2048
```

### Complete Optimization

Perform end-to-end system optimization:

```bash
# Complete optimization with all features
sintaxes-deliciosas complete ~/MessyFolder \
  --target ~/Organized \
  --theme professional \
  --cloud-providers local_cloud dropbox

# Preview complete optimization
sintaxes-deliciosas complete ~/MessyFolder --dry-run
```

## ⚙️ Configuration

### Create Configuration File

```bash
# Create default configuration
sintaxes-deliciosas config --create

# Edit configuration
sintaxes-deliciosas config --edit

# Show current configuration
sintaxes-deliciosas config --show

# Validate configuration
sintaxes-deliciosas config --validate
```

### Configuration Options

The configuration file supports extensive customization:

```json
{
  "analyzer": {
    "deep_analysis": false,
    "include_hidden_files": false,
    "max_file_size_mb": 1000,
    "excluded_extensions": [".tmp", ".cache", ".log"]
  },
  "organizer": {
    "create_backups": true,
    "safe_mode": true,
    "preserve_timestamps": true
  },
  "layout": {
    "default_theme": "professional",
    "auto_apply_icons": true,
    "folder_color_coding": true
  },
  "cloud": {
    "default_strategy": "smart",
    "cache_size_mb": 1024,
    "auto_sync": false
  }
}
```

## 🎨 Themes

### Professional Theme
- Clean, business-oriented layout
- Priority-based organization
- Conservative color scheme
- Comprehensive documentation

### Modern Theme
- Contemporary design elements
- Dynamic folder icons
- Vibrant color palette
- Streamlined structure

### Minimal Theme
- Simplified organization
- No visual distractions
- Essential features only
- Clean typography

### Colorful Theme
- Vibrant visual elements
- Creative folder icons
- High-contrast colors
- Artistic organization

## 🔧 Advanced Features

### Monitoring and Automation

```bash
# Monitor directory for automatic organization
sintaxes-deliciosas monitor ~/Downloads --watch --interval 60
```

### Custom Organization Rules

Create custom rules in your configuration:

```json
{
  "organizer": {
    "custom_categories": {
      "MyCategory": {
        "extensions": [".custom"],
        "keywords": ["special"],
        "destination": "Custom/MyFiles"
      }
    }
  }
}
```

### Cloud Provider Setup

#### Dropbox
```json
{
  "cloud": {
    "providers": {
      "dropbox": {
        "enabled": true,
        "access_token": "your_dropbox_token"
      }
    }
  }
}
```

#### Google Drive
```json
{
  "cloud": {
    "providers": {
      "google_drive": {
        "enabled": true,
        "credentials_file": "/path/to/credentials.json"
      }
    }
  }
}
```

#### AWS S3
```json
{
  "cloud": {
    "providers": {
      "aws_s3": {
        "enabled": true,
        "access_key_id": "your_access_key",
        "secret_access_key": "your_secret_key",
        "bucket": "your_bucket_name"
      }
    }
  }
}
```

## 📊 Output Formats

### Analysis Reports

- **JSON**: Machine-readable format for integration
- **TXT**: Human-readable text reports
- **HTML**: Rich formatted reports with styling

### Organization Plans

Export organization plans before applying:

```bash
sintaxes-deliciosas organize ~/Downloads --dry-run --output plan.json
```

## 🛡️ Safety Features

- **Backup creation** before any destructive operations
- **Dry run mode** to preview changes
- **Rollback capability** to undo organization
- **Safe mode** with additional confirmation prompts
- **File integrity checks** during operations

## 🚨 Error Handling

The system includes comprehensive error handling:

- Graceful handling of permission errors
- Recovery from interrupted operations
- Detailed error logging
- User-friendly error messages

## 🔄 Rollback Operations

```bash
# Rollback organization using backup ID
python -c "
from sintaxes_deliciosas import FileOrganizer
organizer = FileOrganizer()
organizer.rollback_organization('backup_id_here')
"
```

## 🧪 Testing

```bash
# Test with sample data
mkdir test_directory
echo "test" > test_directory/document.txt
echo "test" > test_directory/image.jpg

# Run organization
sintaxes-deliciosas organize test_directory --dry-run
```

## 📈 Performance

- **Multi-threaded processing** for large directories
- **Memory-efficient** file handling
- **Progress indicators** for long operations
- **Configurable performance settings**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- Create an issue for bug reports
- Use discussions for questions
- Check the wiki for additional documentation

## 🌟 Examples

### Example 1: Clean Desktop
```bash
sintaxes-deliciosas complete ~/Desktop \
  --target ~/Desktop/Organized \
  --theme minimal
```

### Example 2: Developer Workspace
```bash
sintaxes-deliciosas layout ~/Development \
  --theme modern \
  --dynamic \
  --templates
```

### Example 3: Media Collection
```bash
sintaxes-deliciosas organize ~/Media \
  --theme colorful \
  --cloud-providers google_drive
```

---

**Sintaxes Deliciosas** - Transform your digital chaos into organized perfection! 🎯
