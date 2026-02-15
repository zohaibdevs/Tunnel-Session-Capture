#!/bin/bash
echo "🚀 Setting up Tunnel Session Capture..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing packages from requirements.txt..."
pip install -r requirements.txt

echo "✨ Setup complete!"
echo ""
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the application:"
echo "  python main.py"