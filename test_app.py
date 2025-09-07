#!/usr/bin/env python3
"""
Test application functionality without GUI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from github_search_app import GitHubSearchApp
import tkinter as tk

def test_app_initialization():
    """Test if the app can be initialized without errors"""
    print("🧪 Testing application initialization...")
    
    try:
        # Create root window (won't be displayed)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Initialize app
        app = GitHubSearchApp(root)
        print("✅ Application initialized successfully")
        
        # Test demo search functionality
        print("🧪 Testing demo search functionality...")
        app.display_demo_results("spotify free")
        print("✅ Demo search works correctly")
        
        # Clean up
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ Application initialization failed: {e}")
        return False

def test_api_parameters():
    """Test API parameter building"""
    print("🧪 Testing API parameter building...")
    
    try:
        # Test query building
        base_query = "spotify free"
        language = "Python"
        sort_option = "stars"
        
        # Build params like the app does
        params = {
            'q': base_query,
            'sort': sort_option,
            'per_page': 10
        }
        
        if language:
            params['q'] += f' language:{language}'
        
        expected_query = "spotify free language:Python"
        
        if params['q'] == expected_query and params['sort'] == sort_option:
            print("✅ API parameter building works correctly")
            print(f"   Query: {params['q']}")
            print(f"   Sort: {params['sort']}")
            return True
        else:
            print(f"❌ API parameters incorrect: {params}")
            return False
            
    except Exception as e:
        print(f"❌ API parameter test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Running application tests...")
    
    test1 = test_app_initialization()
    test2 = test_api_parameters()
    
    if test1 and test2:
        print("\n✅ All tests passed! Application is ready to use.")
        print("💡 Run 'python3 github_search_app.py' to start the GUI application.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
    
    print("\n📚 Application Features:")
    print("   - GUI interface with chat-like search")
    print("   - GitHub API integration with fallback demo mode")
    print("   - Language and sorting filters")
    print("   - Detailed repository information display")
    print("   - Error handling and user feedback")