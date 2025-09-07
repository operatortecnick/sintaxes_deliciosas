# Environment Setup and Troubleshooting

## Running the Application

### Desktop Environment (Recommended)
The application is designed to run on systems with a graphical interface:
- **Windows**: Should work out of the box with Python installed
- **macOS**: Should work out of the box with Python installed  
- **Linux**: Requires X11 or Wayland display server

### Headless/Server Environment
If running on a headless server, you'll need to set up a virtual display:

```bash
# Install virtual display
sudo apt install xvfb

# Run with virtual display
xvfb-run -a python3 github_search_app.py
```

### Common Issues and Solutions

#### 1. "no display name and no $DISPLAY environment variable"
**Solution**: You're running on a headless system. Use `xvfb-run` as shown above.

#### 2. "ModuleNotFoundError: No module named 'tkinter'"
**Solution**: Install tkinter:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# CentOS/RHEL/Fedora
sudo yum install tkinter
# or
sudo dnf install python3-tkinter

# macOS (if using Homebrew)
brew install python-tk
```

#### 3. GitHub API Rate Limiting
**Solution**: The app automatically switches to demo mode when rate limited. For production use, consider:
- Adding GitHub API token authentication
- Implementing proper rate limiting handling
- Caching search results

#### 4. Network/Firewall Issues
**Solution**: Ensure outbound HTTPS connections to api.github.com are allowed.

## Testing

Run the test suite to verify functionality:
```bash
python3 test_app.py
```

## Development

For development and debugging:
```bash
# Run with verbose output
python3 -v github_search_app.py

# Run API tests separately
python3 test_api.py
```