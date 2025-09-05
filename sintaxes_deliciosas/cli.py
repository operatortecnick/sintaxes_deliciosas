"""
Command Line Interface for Sintaxes Deliciosas

Provides a comprehensive CLI for computer analysis, file organization,
and professional layout management.
"""

import click
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Optional
import colorama
from colorama import Fore, Back, Style
from tqdm import tqdm

from .analyzer import SystemAnalyzer
from .organizer import FileOrganizer
from .layout import LayoutManager
from .cloud import CloudManager
from .config import ConfigManager

# Initialize colorama for cross-platform colored output
colorama.init(autoreset=True)


@click.group()
@click.option('--config', '-c', type=click.Path(), help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--quiet', '-q', is_flag=True, help='Suppress output except errors')
@click.pass_context
def main(ctx, config, verbose, quiet):
    """
    Sintaxes Deliciosas - Supreme Computer Analyzer and File Organization System
    
    A comprehensive tool for analyzing your computer system, organizing files,
    and creating professional layouts with cloud integration.
    """
    # Set up logging
    log_level = logging.ERROR if quiet else (logging.DEBUG if verbose else logging.INFO)
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Load configuration
    config_manager = ConfigManager(config)
    ctx.ensure_object(dict)
    ctx.obj['config_manager'] = config_manager
    ctx.obj['config'] = config_manager.get_config()
    ctx.obj['verbose'] = verbose
    ctx.obj['quiet'] = quiet


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file for analysis results')
@click.option('--format', 'output_format', type=click.Choice(['json', 'txt', 'html']), 
              default='txt', help='Output format')
@click.option('--deep', is_flag=True, help='Perform deep analysis (slower but more thorough)')
@click.pass_context
def analyze(ctx, path, output, output_format, deep):
    """Analyze computer system and directory structure."""
    config = ctx.obj['config']
    verbose = ctx.obj['verbose']
    
    click.echo(f"{Fore.CYAN}🔍 Starting system analysis...{Style.RESET_ALL}")
    
    # Initialize analyzer
    analyzer = SystemAnalyzer(config.get('analyzer', {}))
    
    # Perform analysis
    with tqdm(desc="Analyzing system", disable=not verbose) as pbar:
        if deep:
            # Analyze specific path plus system
            results = analyzer.analyze_complete_system([path])
        else:
            # Quick analysis of specific path
            results = analyzer.analyze_complete_system([path])
        pbar.update(1)
    
    # Display results
    _display_analysis_results(results, verbose)
    
    # Save results if requested
    if output:
        if output_format == 'json':
            analyzer.export_analysis(output)
        else:
            _export_analysis_text(results, output, output_format)
        
        click.echo(f"{Fore.GREEN}✅ Analysis results saved to {output}{Style.RESET_ALL}")
    
    # Display recommendations
    if results.get('recommendations'):
        click.echo(f"\n{Fore.YELLOW}💡 Recommendations:{Style.RESET_ALL}")
        for i, rec in enumerate(results['recommendations'], 1):
            click.echo(f"  {i}. {rec}")


@main.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--target', '-t', type=click.Path(), help='Target organization directory')
@click.option('--dry-run', is_flag=True, help='Show what would be done without making changes')
@click.option('--theme', type=click.Choice(['professional', 'modern', 'minimal', 'colorful']),
              default='professional', help='Organization theme')
@click.option('--backup', is_flag=True, help='Create backup before organizing')
@click.pass_context
def organize(ctx, source, target, dry_run, theme, backup):
    """Organize files and create professional directory structure."""
    config = ctx.obj['config']
    verbose = ctx.obj['verbose']
    
    if dry_run:
        click.echo(f"{Fore.YELLOW}🧪 DRY RUN MODE - No changes will be made{Style.RESET_ALL}")
    
    click.echo(f"{Fore.CYAN}📁 Organizing files from {source}...{Style.RESET_ALL}")
    
    # Initialize organizer
    organizer = FileOrganizer(config.get('organizer', {}))
    
    # Organize files
    with tqdm(desc="Organizing files", disable=not verbose) as pbar:
        results = organizer.organize_directory(source, target, dry_run=dry_run)
        pbar.update(1)
    
    # Display results
    _display_organization_results(results, dry_run)
    
    # Apply layout if not dry run
    if not dry_run and target:
        click.echo(f"{Fore.CYAN}🎨 Applying {theme} layout...{Style.RESET_ALL}")
        
        layout_manager = LayoutManager(config.get('layout', {}))
        layout_results = layout_manager.apply_professional_layout(target, theme)
        
        click.echo(f"{Fore.GREEN}✅ Layout applied successfully{Style.RESET_ALL}")
        if verbose:
            _display_layout_results(layout_results)


@main.command()
@click.argument('path', type=click.Path())
@click.option('--theme', type=click.Choice(['professional', 'modern', 'minimal', 'colorful']),
              default='professional', help='Layout theme')
@click.option('--dynamic', is_flag=True, help='Create dynamic adaptive layout')
@click.option('--templates', is_flag=True, help='Include layout templates')
@click.pass_context
def layout(ctx, path, theme, dynamic, templates):
    """Create professional directory layout and visual organization."""
    config = ctx.obj['config']
    verbose = ctx.obj['verbose']
    
    click.echo(f"{Fore.CYAN}🎨 Creating {theme} layout at {path}...{Style.RESET_ALL}")
    
    # Create target directory if it doesn't exist
    Path(path).mkdir(parents=True, exist_ok=True)
    
    # Initialize layout manager
    layout_manager = LayoutManager(config.get('layout', {}))
    
    # Create professional layout
    with tqdm(desc="Creating layout", disable=not verbose) as pbar:
        if dynamic:
            results = layout_manager.create_dynamic_layout(path, 'adaptive')
        else:
            # Create standard professional layout
            organizer = FileOrganizer()
            layout_results = organizer.create_professional_layout(path)
            
            # Apply theme
            theme_results = layout_manager.apply_professional_layout(path, theme)
            
            results = {**layout_results, **theme_results}
        
        pbar.update(1)
    
    _display_layout_results(results)
    click.echo(f"{Fore.GREEN}✅ Professional layout created successfully{Style.RESET_ALL}")


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--providers', '-p', multiple=True, 
              type=click.Choice(['local_cloud', 'dropbox', 'google_drive', 'onedrive', 'aws_s3']),
              help='Cloud providers to configure')
@click.option('--strategy', type=click.Choice(['smart', 'mirror', 'backup', 'selective']),
              default='smart', help='Sync strategy')
@click.option('--optimize', is_flag=True, help='Optimize cloud storage usage')
@click.option('--cache-size', type=int, default=1024, help='Virtual memory cache size in MB')
@click.pass_context
def cloud(ctx, path, providers, strategy, optimize, cache_size):
    """Set up cloud integration and virtual memory optimization."""
    config = ctx.obj['config']
    verbose = ctx.obj['verbose']
    
    click.echo(f"{Fore.CYAN}☁️ Setting up cloud integration...{Style.RESET_ALL}")
    
    # Initialize cloud manager
    cloud_manager = CloudManager(config.get('cloud', {}))
    
    # Set up virtual memory optimization
    with tqdm(desc="Optimizing virtual memory", disable=not verbose) as pbar:
        vm_results = cloud_manager.setup_virtual_memory_optimization(path, cache_size)
        pbar.update(1)
    
    if verbose:
        click.echo(f"{Fore.GREEN}Virtual memory optimization:{Style.RESET_ALL}")
        for feature in vm_results['optimization_applied']:
            click.echo(f"  ✓ {feature.replace('_', ' ').title()}")
    
    # Set up cloud providers
    if providers:
        with tqdm(desc="Configuring cloud providers", disable=not verbose) as pbar:
            cloud_results = cloud_manager.setup_cloud_integration(
                path, list(providers), strategy
            )
            pbar.update(1)
        
        click.echo(f"{Fore.GREEN}Cloud providers configured:{Style.RESET_ALL}")
        for provider in cloud_results['providers_configured']:
            click.echo(f"  ✓ {provider.replace('_', ' ').title()}")
    
    # Optimize cloud storage
    if optimize:
        with tqdm(desc="Optimizing cloud storage", disable=not verbose) as pbar:
            opt_results = cloud_manager.optimize_cloud_storage(path)
            pbar.update(1)
        
        if opt_results['storage_saved'] > 0:
            savings_mb = opt_results['storage_saved'] / (1024 * 1024)
            click.echo(f"{Fore.GREEN}Storage optimized: {savings_mb:.1f} MB saved{Style.RESET_ALL}")


@main.command()
@click.argument('source', type=click.Path(exists=True))
@click.option('--target', '-t', type=click.Path(), help='Target directory for organized files')
@click.option('--theme', type=click.Choice(['professional', 'modern', 'minimal', 'colorful']),
              default='professional', help='Layout theme')
@click.option('--cloud-providers', '-c', multiple=True,
              type=click.Choice(['local_cloud', 'dropbox', 'google_drive', 'onedrive', 'aws_s3']),
              help='Cloud providers for integration')
@click.option('--dry-run', is_flag=True, help='Preview changes without applying them')
@click.pass_context
def complete(ctx, source, target, theme, cloud_providers, dry_run):
    """Perform complete system analysis, organization, and optimization."""
    config = ctx.obj['config']
    verbose = ctx.obj['verbose']
    
    if dry_run:
        click.echo(f"{Fore.YELLOW}🧪 PREVIEW MODE - No changes will be made{Style.RESET_ALL}")
    
    click.echo(f"{Fore.CYAN}🚀 Starting complete system optimization...{Style.RESET_ALL}")
    
    # Step 1: Analysis
    click.echo(f"\n{Fore.BLUE}Step 1: System Analysis{Style.RESET_ALL}")
    analyzer = SystemAnalyzer(config.get('analyzer', {}))
    
    with tqdm(desc="Analyzing system", disable=not verbose) as pbar:
        analysis_results = analyzer.analyze_complete_system([source])
        pbar.update(1)
    
    _display_analysis_summary(analysis_results)
    
    # Step 2: Organization
    if not dry_run:
        click.echo(f"\n{Fore.BLUE}Step 2: File Organization{Style.RESET_ALL}")
        organizer = FileOrganizer(config.get('organizer', {}))
        
        # Use target or create organized folder in source
        org_target = target or str(Path(source) / "Organized")
        
        with tqdm(desc="Organizing files", disable=not verbose) as pbar:
            org_results = organizer.organize_directory(source, org_target, dry_run=False)
            pbar.update(1)
        
        _display_organization_summary(org_results)
        
        # Step 3: Layout Application
        click.echo(f"\n{Fore.BLUE}Step 3: Professional Layout{Style.RESET_ALL}")
        layout_manager = LayoutManager(config.get('layout', {}))
        
        with tqdm(desc="Applying layout", disable=not verbose) as pbar:
            layout_results = layout_manager.apply_professional_layout(org_target, theme)
            pbar.update(1)
        
        click.echo(f"  ✓ {theme.title()} theme applied")
        
        # Step 4: Cloud Integration
        if cloud_providers:
            click.echo(f"\n{Fore.BLUE}Step 4: Cloud Integration{Style.RESET_ALL}")
            cloud_manager = CloudManager(config.get('cloud', {}))
            
            with tqdm(desc="Setting up cloud", disable=not verbose) as pbar:
                # Virtual memory optimization
                vm_results = cloud_manager.setup_virtual_memory_optimization(org_target)
                
                # Cloud provider setup
                cloud_results = cloud_manager.setup_cloud_integration(
                    org_target, list(cloud_providers), 'smart'
                )
                pbar.update(1)
            
            click.echo(f"  ✓ {len(cloud_results['providers_configured'])} cloud providers configured")
    
    # Final summary
    click.echo(f"\n{Fore.GREEN}🎉 Complete optimization finished!{Style.RESET_ALL}")
    
    if not dry_run:
        final_target = target or str(Path(source) / "Organized")
        click.echo(f"📁 Organized files location: {final_target}")
        click.echo(f"🎨 Theme applied: {theme}")
        if cloud_providers:
            click.echo(f"☁️ Cloud providers: {', '.join(cloud_providers)}")


@main.command()
@click.option('--create', is_flag=True, help='Create default configuration file')
@click.option('--edit', is_flag=True, help='Open configuration in default editor')
@click.option('--show', is_flag=True, help='Show current configuration')
@click.option('--validate', is_flag=True, help='Validate configuration file')
@click.pass_context
def config(ctx, create, edit, show, validate):
    """Manage configuration settings."""
    config_manager = ctx.obj['config_manager']
    
    if create:
        config_path = config_manager.create_default_config()
        click.echo(f"{Fore.GREEN}✅ Default configuration created at {config_path}{Style.RESET_ALL}")
    
    elif edit:
        config_path = config_manager.get_config_path()
        if config_path and config_path.exists():
            click.edit(filename=str(config_path))
        else:
            click.echo(f"{Fore.RED}❌ Configuration file not found{Style.RESET_ALL}")
    
    elif show:
        config_data = config_manager.get_config()
        click.echo(f"{Fore.CYAN}Current configuration:{Style.RESET_ALL}")
        click.echo(json.dumps(config_data, indent=2))
    
    elif validate:
        is_valid, errors = config_manager.validate_config()
        if is_valid:
            click.echo(f"{Fore.GREEN}✅ Configuration is valid{Style.RESET_ALL}")
        else:
            click.echo(f"{Fore.RED}❌ Configuration validation failed:{Style.RESET_ALL}")
            for error in errors:
                click.echo(f"  • {error}")
    
    else:
        click.echo(f"{Fore.YELLOW}Use --help to see available configuration options{Style.RESET_ALL}")


@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--watch', is_flag=True, help='Monitor directory for real-time organization')
@click.option('--interval', type=int, default=60, help='Monitoring interval in seconds')
@click.pass_context
def monitor(ctx, path, watch, interval):
    """Monitor directory and apply automatic organization."""
    config = ctx.obj['config']
    
    if not watch:
        click.echo(f"{Fore.YELLOW}Use --watch flag to start monitoring{Style.RESET_ALL}")
        return
    
    click.echo(f"{Fore.CYAN}👁️ Monitoring {path} for automatic organization...{Style.RESET_ALL}")
    click.echo(f"Interval: {interval} seconds")
    click.echo("Press Ctrl+C to stop monitoring")
    
    try:
        import time
        from .monitor import DirectoryMonitor
        
        monitor = DirectoryMonitor(path, config)
        monitor.start_monitoring(interval)
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        click.echo(f"\n{Fore.YELLOW}Monitoring stopped{Style.RESET_ALL}")
    except ImportError:
        click.echo(f"{Fore.RED}❌ Monitoring feature not available{Style.RESET_ALL}")


# Helper functions for displaying results

def _display_analysis_results(results: Dict, verbose: bool = False):
    """Display system analysis results."""
    click.echo(f"\n{Fore.GREEN}📊 Analysis Results:{Style.RESET_ALL}")
    
    # System info
    sys_info = results.get('system_info', {})
    click.echo(f"  🖥️  Platform: {sys_info.get('platform', 'Unknown')}")
    click.echo(f"  🧠 CPU Cores: {sys_info.get('cpu_count', 'Unknown')}")
    
    memory_gb = sys_info.get('memory_total', 0) / (1024**3)
    click.echo(f"  💾 Total Memory: {memory_gb:.1f} GB")
    
    # Disk usage
    click.echo(f"\n  💿 Disk Usage:")
    for device, info in results.get('disk_usage', {}).items():
        usage_pct = info.get('percentage', 0)
        color = Fore.RED if usage_pct > 90 else Fore.YELLOW if usage_pct > 80 else Fore.GREEN
        click.echo(f"    {color}{device}: {usage_pct:.1f}% used{Style.RESET_ALL}")
    
    # File analysis summary
    total_files = 0
    total_size = 0
    for path, analysis in results.get('file_analysis', {}).items():
        total_files += analysis.get('total_files', 0)
        total_size += analysis.get('total_size', 0)
    
    if total_files > 0:
        size_gb = total_size / (1024**3)
        click.echo(f"\n  📁 Files analyzed: {total_files:,}")
        click.echo(f"  📏 Total size: {size_gb:.2f} GB")
    
    # Duplicates
    total_duplicates = sum(len(dups) for dups in results.get('duplicates', {}).values())
    if total_duplicates > 0:
        click.echo(f"  🔄 Duplicate groups found: {total_duplicates}")


def _display_organization_results(results: Dict, dry_run: bool = False):
    """Display file organization results."""
    action = "would be" if dry_run else "were"
    
    click.echo(f"\n{Fore.GREEN}📁 Organization Results:{Style.RESET_ALL}")
    click.echo(f"  📄 Files processed: {results.get('files_processed', 0)}")
    click.echo(f"  ✅ Files {action} organized: {results.get('files_organized', 0)}")
    click.echo(f"  📂 Categories created: {len(results.get('categories_created', []))}")
    
    if results.get('errors'):
        click.echo(f"  ⚠️  Errors: {len(results['errors'])}")


def _display_layout_results(results: Dict):
    """Display layout application results."""
    click.echo(f"  🎨 Theme: {results.get('theme_applied', 'Unknown')}")
    click.echo(f"  ✨ Features applied: {len(results.get('features_applied', []))}")
    
    for feature in results.get('features_applied', []):
        click.echo(f"    ✓ {feature.replace('_', ' ').title()}")


def _display_analysis_summary(results: Dict):
    """Display brief analysis summary."""
    total_files = sum(
        analysis.get('total_files', 0) 
        for analysis in results.get('file_analysis', {}).values()
    )
    
    recommendations_count = len(results.get('recommendations', []))
    
    click.echo(f"  📄 Files analyzed: {total_files:,}")
    click.echo(f"  💡 Recommendations: {recommendations_count}")


def _display_organization_summary(results: Dict):
    """Display brief organization summary."""
    click.echo(f"  ✅ Files organized: {results.get('files_organized', 0)}")
    click.echo(f"  📂 Categories: {len(results.get('categories_created', []))}")


def _export_analysis_text(results: Dict, output_path: str, format_type: str):
    """Export analysis results to text or HTML format."""
    if format_type == 'html':
        content = _generate_html_report(results)
    else:
        content = _generate_text_report(results)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)


def _generate_text_report(results: Dict) -> str:
    """Generate text report from analysis results."""
    report = "SINTAXES DELICIOSAS - SYSTEM ANALYSIS REPORT\n"
    report += "=" * 50 + "\n\n"
    
    # System information
    sys_info = results.get('system_info', {})
    report += "SYSTEM INFORMATION\n"
    report += "-" * 20 + "\n"
    report += f"Platform: {sys_info.get('platform', 'Unknown')}\n"
    report += f"CPU Cores: {sys_info.get('cpu_count', 'Unknown')}\n"
    
    memory_gb = sys_info.get('memory_total', 0) / (1024**3)
    report += f"Total Memory: {memory_gb:.1f} GB\n\n"
    
    # Disk usage
    report += "DISK USAGE\n"
    report += "-" * 10 + "\n"
    for device, info in results.get('disk_usage', {}).items():
        usage_pct = info.get('percentage', 0)
        report += f"{device}: {usage_pct:.1f}% used\n"
    
    report += "\n"
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        report += "RECOMMENDATIONS\n"
        report += "-" * 15 + "\n"
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
    
    return report


def _generate_html_report(results: Dict) -> str:
    """Generate HTML report from analysis results."""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Sintaxes Deliciosas - Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #2C3E50; }
        h2 { color: #3498DB; }
        .metric { background: #F8F9FA; padding: 10px; margin: 5px 0; border-left: 4px solid #3498DB; }
        .recommendation { background: #FFF3CD; padding: 10px; margin: 5px 0; border-left: 4px solid #FFB347; }
    </style>
</head>
<body>
    <h1>System Analysis Report</h1>
    <p>Generated by Sintaxes Deliciosas</p>
"""
    
    # Add content sections
    sys_info = results.get('system_info', {})
    html += f"""
    <h2>System Information</h2>
    <div class="metric">Platform: {sys_info.get('platform', 'Unknown')}</div>
    <div class="metric">CPU Cores: {sys_info.get('cpu_count', 'Unknown')}</div>
    <div class="metric">Total Memory: {sys_info.get('memory_total', 0) / (1024**3):.1f} GB</div>
"""
    
    # Recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        html += "<h2>Recommendations</h2>"
        for rec in recommendations:
            html += f'<div class="recommendation">{rec}</div>'
    
    html += "</body></html>"
    return html


if __name__ == '__main__':
    main()