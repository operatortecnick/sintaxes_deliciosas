#!/usr/bin/env python3
"""
Test script for GitHub API functionality
"""

import requests
import json

def test_github_search():
    """Test GitHub API search functionality"""
    print("🔍 Testing GitHub API search...")
    
    # Test search
    api_url = "https://api.github.com/search/repositories"
    params = {
        'q': 'spotify free',
        'per_page': 5
    }
    
    try:
        # Add User-Agent header to comply with GitHub API guidelines
        headers = {
            'User-Agent': 'GitHub-Search-App/1.0 (Educational Purpose)',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        # Check response status and handle rate limiting
        if response.status_code == 403:
            print(f"❌ GitHub API rate limit exceeded or access forbidden")
            print(f"Response headers: {dict(response.headers)}")
            return False
        
        response.raise_for_status()
        
        data = response.json()
        total_count = data.get('total_count', 0)
        items = data.get('items', [])
        
        print(f"✅ API request successful!")
        print(f"📊 Found {total_count:,} total repositories")
        print(f"📦 Showing top {len(items)} results:")
        
        for i, repo in enumerate(items, 1):
            name = repo.get('full_name', 'Unknown')
            stars = repo.get('stargazers_count', 0)
            language = repo.get('language', 'Unknown')
            description = repo.get('description', 'No description')
            
            if len(description) > 80:
                description = description[:77] + "..."
            
            print(f"  {i}. {name} ⭐{stars:,} 💻{language}")
            print(f"     {description}")
        
        return True
        
    except requests.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_github_search()
    if success:
        print("\n✅ GitHub API integration is working correctly!")
    else:
        print("\n❌ GitHub API integration has issues.")