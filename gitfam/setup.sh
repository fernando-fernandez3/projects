#!/bin/bash
# GitFam Easy Setup Script

set -e

echo "🌳 GitFam Setup"
echo "==============="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell config to get uv in PATH
    if [ -f "$HOME/.bashrc" ]; then
        source "$HOME/.bashrc"
    elif [ -f "$HOME/.zshrc" ]; then
        source "$HOME/.zshrc"
    fi
    
    echo "✓ uv installed"
else
    echo "✓ uv already installed"
fi

echo ""
echo "📚 Installing GitFam CLI..."
uv sync

echo ""
echo "✓ Installation complete!"
echo ""
echo "🚀 Next steps:"
echo ""
echo "  Run the quick start wizard:"
echo "    uv run gitfam quick-start"
echo ""
echo "  Or initialize manually:"
echo "    uv run gitfam init-project"
echo "    uv run gitfam create-branch"
echo "    uv run gitfam add-family-member"
echo ""
echo "  Generate website:"
echo "    uv run gitfam generate-website"
echo ""
echo "💡 Tip: Activate virtual environment to use commands without 'uv run':"
echo "    source .venv/bin/activate"
echo ""
echo "📖 For more help, see: docs/CLI_GUIDE.md"
echo ""
