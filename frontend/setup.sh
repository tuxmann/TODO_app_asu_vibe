#!/bin/bash

# Frontend Setup Script for TODO App
# This script helps set up the Next.js frontend

set -e  # Exit on error

echo "=================================="
echo "TODO App Frontend Setup"
echo "=================================="
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "Please install Node.js 18.x or higher from https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js found: $(node --version)"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not installed"
    exit 1
fi

echo "✓ npm found: $(npm --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"
echo ""

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    echo "⚙️  Creating .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
    echo "✓ .env.local created"
else
    echo "ℹ️  .env.local already exists"
fi

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Make sure your FastAPI backend is running:"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "2. Start the frontend development server:"
echo "   npm run dev"
echo ""
echo "3. Open your browser to:"
echo "   http://localhost:3000"
echo ""
echo "Happy coding! 🚀"

