#!/bin/bash
# Setup script for API Extractor

echo "🚀 Setting up API Extractor..."

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ Edit .env file to add your API keys (optional - many APIs work without keys)"
else
    echo "✅ .env file already exists"
fi

# Test the installation
echo "🧪 Testing installation..."
python3 -c "
import sys
try:
    from api_extractor import APIExtractor
    extractor = APIExtractor()
    print('✅ API Extractor imported successfully')
    
    # Test basic functionality
    status = extractor.get_api_status()
    print(f'✅ Found {len(status[\"stock_apis\"])} stock APIs')
    print(f'✅ Found {len(status[\"ai_apis\"])} AI APIs')
    
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'⚠️  Warning: {e}')
"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env file to add API keys (optional)"
echo "2. Run: python3 example.py"
echo "3. Try CLI: python3 cli.py --help"
echo "4. Test APIs: python3 cli.py test"
echo ""
echo "📖 Quick examples:"
echo "  python3 cli.py stock price AAPL"
echo "  python3 cli.py ai ask 'What is Python?'"
echo "  python3 cli.py analyze TSLA"