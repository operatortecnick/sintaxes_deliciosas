"""
Sintaxes Deliciosas - Supreme Computer Analyzer and File Organization System

A comprehensive tool for analyzing your computer system, suggesting file organization
improvements, and creating professional, clean, and dynamic layouts with cloud integration.
"""

__version__ = "1.0.0"
__author__ = "operatortecnick"
__email__ = ""

from .analyzer import SystemAnalyzer
from .organizer import FileOrganizer
from .layout import LayoutManager
from .cloud import CloudManager

__all__ = [
    "SystemAnalyzer",
    "FileOrganizer", 
    "LayoutManager",
    "CloudManager"
]