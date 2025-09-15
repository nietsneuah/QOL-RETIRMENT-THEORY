#!/bin/bash
# LaTeX PATH Setup Script
# Sets up the PATH to include LaTeX BasicTeX installation

export PATH="/usr/local/texlive/2025basic/bin/universal-darwin:$PATH"

echo "✅ LaTeX PATH configured"
echo "📄 LaTeX installation: $(which pdflatex 2>/dev/null || echo 'Not found')"

# Verify LaTeX is working
if command -v pdflatex >/dev/null 2>&1; then
    echo "🔧 LaTeX Version: $(pdflatex --version | head -1)"
else
    echo "❌ LaTeX not found in PATH"
    echo "💡 Make sure BasicTeX is installed: brew install basictex"
fi