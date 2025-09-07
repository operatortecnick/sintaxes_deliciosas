#!/usr/bin/env python3
"""
GitHub Repository Search Application
A GUI application that allows users to search GitHub repositories worldwide
through a chat-like interface.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import threading
from datetime import datetime
import webbrowser
from urllib.parse import quote


class GitHubSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repository Search - Sintaxes Deliciosas")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # GitHub API base URL
        self.github_api_url = "https://api.github.com/search/repositories"
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔍 GitHub Repository Search", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        # Chat/Results area
        self.chat_frame = ttk.Frame(main_frame)
        self.chat_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)
        
        # Scrolled text for chat history
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame, 
            wrap=tk.WORD, 
            state=tk.DISABLED,
            font=("Consolas", 10),
            height=20
        )
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            input_frame, 
            textvariable=self.search_var,
            font=("Arial", 11),
            width=50
        )
        self.search_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.search_entry.bind('<Return>', self.on_search)
        
        # Search button
        self.search_button = ttk.Button(
            input_frame, 
            text="🔍 Search", 
            command=self.on_search
        )
        self.search_button.grid(row=0, column=1)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Search Options", padding="5")
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        
        # Language filter
        ttk.Label(options_frame, text="Language:").grid(row=0, column=0, padx=(0, 5))
        self.language_var = tk.StringVar()
        self.language_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.language_var,
            values=["", "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "TypeScript", "PHP", "Ruby"],
            state="readonly",
            width=15
        )
        self.language_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # Sort by
        ttk.Label(options_frame, text="Sort by:").grid(row=0, column=2, padx=(0, 5))
        self.sort_var = tk.StringVar(value="best match")
        self.sort_combo = ttk.Combobox(
            options_frame,
            textvariable=self.sort_var,
            values=["best match", "stars", "forks", "updated"],
            state="readonly",
            width=15
        )
        self.sort_combo.grid(row=0, column=3, sticky=tk.W)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to search GitHub repositories...")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
        # Add welcome message
        self.add_message("🤖 Welcome! Type your search query to find GitHub repositories worldwide.", "system")
        self.add_message("💡 Examples: 'spotify free', 'machine learning python', 'web scraper'", "system")
        
        # Focus on search entry
        self.search_entry.focus()
    
    def add_message(self, message, message_type="user"):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if message_type == "user":
            prefix = f"[{timestamp}] 🔍 You: "
            self.chat_display.insert(tk.END, prefix, "user_tag")
        elif message_type == "system":
            prefix = f"[{timestamp}] 🤖 System: "
            self.chat_display.insert(tk.END, prefix, "system_tag")
        elif message_type == "result":
            prefix = f"[{timestamp}] 📦 Results: "
            self.chat_display.insert(tk.END, prefix, "result_tag")
        elif message_type == "error":
            prefix = f"[{timestamp}] ❌ Error: "
            self.chat_display.insert(tk.END, prefix, "error_tag")
        
        # Configure tags for different message types
        self.chat_display.tag_config("user_tag", foreground="blue", font=("Consolas", 10, "bold"))
        self.chat_display.tag_config("system_tag", foreground="green", font=("Consolas", 10, "bold"))
        self.chat_display.tag_config("result_tag", foreground="purple", font=("Consolas", 10, "bold"))
        self.chat_display.tag_config("error_tag", foreground="red", font=("Consolas", 10, "bold"))
        
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def on_search(self, event=None):
        """Handle search button click or Enter key press"""
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Empty Query", "Please enter a search term.")
            return
        
        # Add user message to chat
        self.add_message(f'Searching for: "{query}"', "user")
        
        # Disable search button during search
        self.search_button.config(state=tk.DISABLED)
        self.status_var.set("Searching GitHub repositories...")
        
        # Run search in a separate thread to avoid blocking UI
        search_thread = threading.Thread(target=self.perform_search, args=(query,))
        search_thread.daemon = True
        search_thread.start()
    
    def perform_search(self, query):
        """Perform the actual GitHub API search"""
        try:
            # Build search parameters
            params = {
                'q': query,
                'sort': self.sort_var.get().replace(' ', '_').replace('best_match', ''),
                'per_page': 10
            }
            
            # Add language filter if specified
            language = self.language_var.get()
            if language:
                params['q'] += f' language:{language}'
            
            # Remove empty sort parameter
            if not params['sort']:
                del params['sort']
            
            # Add proper headers for GitHub API
            headers = {
                'User-Agent': 'GitHub-Search-App/1.0 (Educational Purpose)',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Make API request
            response = requests.get(self.github_api_url, params=params, headers=headers, timeout=10)
            
            # Handle rate limiting and other HTTP errors
            if response.status_code == 403:
                # Fallback to demo mode if rate limited
                self.root.after(0, self.display_demo_results, query)
                return
            elif response.status_code == 422:
                error_msg = "Invalid search query. Please try different keywords."
                self.root.after(0, self.handle_error, error_msg)
                return
            
            response.raise_for_status()
            data = response.json()
            
            # Update UI in main thread
            self.root.after(0, self.display_results, data, query)
            
        except requests.RequestException as e:
            # If API fails, show demo results
            if "403" in str(e) or "rate limit" in str(e).lower():
                self.root.after(0, self.display_demo_results, query)
            else:
                error_msg = f"Failed to search GitHub: {str(e)}"
                self.root.after(0, self.handle_error, error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.root.after(0, self.handle_error, error_msg)
    
    def display_demo_results(self, query):
        """Display demo results when API is unavailable"""
        self.add_message("⚠️ GitHub API is currently rate-limited. Showing demo results:", "result")
        
        # Create demo data based on query
        demo_repos = []
        
        if "spotify" in query.lower():
            demo_repos = [
                {
                    'name': 'spotify-web-api-sdk',
                    'full_name': 'spotify/web-api-sdk',
                    'description': 'A TypeScript SDK for the Spotify Web API with full type safety, runtime validation, and a built-in retry mechanism.',
                    'stargazers_count': 543,
                    'language': 'TypeScript',
                    'html_url': 'https://github.com/spotify/web-api-sdk'
                },
                {
                    'name': 'spotifydl',
                    'full_name': 'SathyaBhat/spotify-dl',
                    'description': 'Downloads songs from Spotify playlists (YouTube Music)',
                    'stargazers_count': 1234,
                    'language': 'Python',
                    'html_url': 'https://github.com/SathyaBhat/spotify-dl'
                },
                {
                    'name': 'spotify-clone',
                    'full_name': 'demo/spotify-clone',
                    'description': 'A Spotify clone built with React and Node.js',
                    'stargazers_count': 892,
                    'language': 'JavaScript',
                    'html_url': 'https://github.com/demo/spotify-clone'
                }
            ]
        elif "python" in query.lower():
            demo_repos = [
                {
                    'name': 'awesome-python',
                    'full_name': 'vinta/awesome-python',
                    'description': 'A curated list of awesome Python frameworks, libraries, software and resources',
                    'stargazers_count': 45678,
                    'language': 'Python',
                    'html_url': 'https://github.com/vinta/awesome-python'
                },
                {
                    'name': 'requests',
                    'full_name': 'psf/requests',
                    'description': 'A simple, yet elegant, HTTP library for Python',
                    'stargazers_count': 35432,
                    'language': 'Python',
                    'html_url': 'https://github.com/psf/requests'
                }
            ]
        else:
            demo_repos = [
                {
                    'name': f'{query.replace(" ", "-")}-demo',
                    'full_name': f'demo/{query.replace(" ", "-")}',
                    'description': f'Demo repository for {query}',
                    'stargazers_count': 123,
                    'language': 'Python',
                    'html_url': f'https://github.com/demo/{query.replace(" ", "-")}'
                },
                {
                    'name': f'{query}-example',
                    'full_name': f'example/{query.replace(" ", "-")}',
                    'description': f'Example implementation of {query}',
                    'stargazers_count': 456,
                    'language': 'JavaScript',
                    'html_url': f'https://github.com/example/{query.replace(" ", "-")}'
                }
            ]
        
        self.add_message(f"Found {len(demo_repos)} demo repositories for '{query}':", "result")
        
        for i, repo in enumerate(demo_repos, 1):
            name = repo.get('name', 'Unknown')
            full_name = repo.get('full_name', 'Unknown')
            description = repo.get('description', 'No description available')
            stars = repo.get('stargazers_count', 0)
            language = repo.get('language', 'Unknown')
            url = repo.get('html_url', '')
            
            result_text = f"""
{i}. 📦 {full_name}
   ⭐ {stars:,} stars | 💻 {language} | 🔗 {url}
   📝 {description}
"""
            self.add_message(result_text.strip(), "result")
        
        # Re-enable search button
        self.search_button.config(state=tk.NORMAL)
        self.status_var.set(f"Demo search complete. Showing {len(demo_repos)} sample repositories.")
        
        # Clear search entry for next search
        self.search_var.set("")

    def display_results(self, data, query):
        """Display search results in the chat"""
        total_count = data.get('total_count', 0)
        items = data.get('items', [])
        
        if total_count == 0:
            self.add_message(f"No repositories found for '{query}'. Try different keywords.", "result")
        else:
            self.add_message(f"Found {total_count:,} repositories for '{query}'. Showing top {len(items)}:", "result")
            
            for i, repo in enumerate(items, 1):
                name = repo.get('name', 'Unknown')
                full_name = repo.get('full_name', 'Unknown')
                description = repo.get('description', 'No description available')
                stars = repo.get('stargazers_count', 0)
                language = repo.get('language', 'Unknown')
                url = repo.get('html_url', '')
                
                # Truncate long descriptions
                if len(description) > 100:
                    description = description[:97] + "..."
                
                result_text = f"""
{i}. 📦 {full_name}
   ⭐ {stars:,} stars | 💻 {language} | 🔗 {url}
   📝 {description}
"""
                self.add_message(result_text.strip(), "result")
        
        # Re-enable search button
        self.search_button.config(state=tk.NORMAL)
        self.status_var.set(f"Search complete. Found {total_count:,} repositories.")
        
        # Clear search entry for next search
        self.search_var.set("")
    
    def handle_error(self, error_msg):
        """Handle and display errors"""
        self.add_message(error_msg, "error")
        self.search_button.config(state=tk.NORMAL)
        self.status_var.set("Ready to search GitHub repositories...")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = GitHubSearchApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application interrupted by user")


if __name__ == "__main__":
    main()