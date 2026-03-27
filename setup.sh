#!/bin/bash
# Tanner's Tech News - Background Setup
# This script sets up the basic infrastructure

echo "🚀 Setting up Tanner's Tech News..."
echo "===================================="

# Create project directory
mkdir -p /home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/{scraper,articles,website,templates}

echo "✅ Project directories created"

# Create placeholder files
touch /home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/README.md
touch /home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/scraper/sources.txt
touch /home/dan/.openclaw/workspace/tanner-business/tanners-tech-news/articles/.gitkeep

echo "✅ Placeholder files created"
echo ""
echo "Project structure:"
find /home/dan/.openclaw/workspace/tanner-business/tanners-tech-news -type f -o -type d | head -20

echo ""
echo "Ready for development!"
