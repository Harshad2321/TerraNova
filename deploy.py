#!/usr/bin/env python3
"""
TerraNova Deployment Helper
Helps you deploy TerraNova to various platforms
"""

import subprocess
import sys
import os
import json

def check_requirements():
    """Check if all required tools are installed"""
    tools = {
        'git': 'git --version',
        'node': 'node --version',
        'npm': 'npm --version'
    }
    
    missing = []
    for tool, command in tools.items():
        try:
            subprocess.run(command.split(), capture_output=True, check=True)
            print(f"✅ {tool} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append(tool)
            print(f"❌ {tool} is not installed")
    
    return missing

def deploy_vercel():
    """Deploy to Vercel"""
    print("🚀 Deploying to Vercel...")
    
    # Check if vercel CLI is installed
    try:
        subprocess.run(['vercel', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing Vercel CLI...")
        subprocess.run(['npm', 'install', '-g', 'vercel'], check=True)
    
    # Deploy
    print("🌐 Starting deployment...")
    result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Deployment successful!")
        print(f"🌍 Your app is live at: {result.stdout.strip()}")
    else:
        print("❌ Deployment failed!")
        print(result.stderr)

def deploy_netlify():
    """Deploy frontend to Netlify"""
    print("🚀 Preparing for Netlify deployment...")
    
    # Create netlify.toml
    netlify_config = """[build]
  publish = "frontend"
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
    
    with open('netlify.toml', 'w') as f:
        f.write(netlify_config)
    
    print("✅ Created netlify.toml")
    print("📁 Drag and drop the 'frontend' folder to netlify.com")
    print("🔗 Or connect your GitHub repository for auto-deploys")

def deploy_github_pages():
    """Prepare for GitHub Pages deployment"""
    print("🚀 Preparing for GitHub Pages...")
    
    # Create .github/workflows/deploy.yml
    os.makedirs('.github/workflows', exist_ok=True)
    
    workflow = """name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Node.js
      uses: actions/setup-node@v2
      with:
        node-version: '16'
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./frontend
"""
    
    with open('.github/workflows/deploy.yml', 'w') as f:
        f.write(workflow)
    
    print("✅ Created GitHub Actions workflow")
    print("📁 Push to GitHub and enable Pages in repository settings")

def deploy_docker():
    """Build Docker image"""
    print("🐳 Building Docker image...")
    
    try:
        subprocess.run(['docker', 'build', '-t', 'terranova', '.'], check=True)
        print("✅ Docker image built successfully!")
        print("🚀 Run with: docker run -p 8000:8000 terranova")
    except subprocess.CalledProcessError:
        print("❌ Docker build failed!")

def main():
    """Main deployment menu"""
    print("🏙️ TerraNova Deployment Helper")
    print("=" * 40)
    
    # Check requirements
    missing = check_requirements()
    if missing:
        print(f"\n⚠️ Please install: {', '.join(missing)}")
        return
    
    print("\nChoose deployment option:")
    print("1. 🌐 Vercel (Recommended - Full Stack)")
    print("2. 🎯 Netlify (Frontend Only)")
    print("3. 📚 GitHub Pages (Static)")
    print("4. 🐳 Docker (Any Cloud)")
    print("5. 📖 Show deployment guides")
    print("0. ❌ Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == '1':
        deploy_vercel()
    elif choice == '2':
        deploy_netlify()
    elif choice == '3':
        deploy_github_pages()
    elif choice == '4':
        deploy_docker()
    elif choice == '5':
        print("\n📖 Check these files for detailed instructions:")
        print("- DEPLOYMENT.md")
        print("- DEPLOY_STEPS.md")
    elif choice == '0':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
