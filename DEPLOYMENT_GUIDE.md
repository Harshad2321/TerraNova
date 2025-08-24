# GitHub Pages Deployment Instructions

## Step 1: Initialize Git Repository
Open PowerShell in your project directory and run:

```powershell
cd "c:\Users\pradi\OneDrive\Documents\GitHub\TerraNova"
git init
git add .
git commit -m "Initial commit: TerraNova AI City Builder"
```

## Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `TerraNova`
3. Description: `AI-Powered Sustainable City Builder`
4. Set to Public (required for GitHub Pages)
5. Don't initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Connect Local Repository to GitHub
Replace `YOUR_USERNAME` with your GitHub username:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/TerraNova.git
git branch -M main
git push -u origin main
```

## Step 4: Enable GitHub Pages
1. Go to your repository on GitHub
2. Click "Settings" tab
3. Scroll down to "Pages" in the left sidebar
4. Under "Source", select "GitHub Actions"
5. The workflow will automatically deploy your site

## Step 5: Access Your Deployed Site
Your site will be available at:
`https://YOUR_USERNAME.github.io/TerraNova/`

## What's Already Configured

✅ **GitHub Actions Workflow**: `.github/workflows/deploy.yml`
- Automatically builds and deploys on every push to main
- Optimized for GitHub Pages
- Includes all necessary build steps

✅ **PWA Manifest**: `frontend/manifest.json`
- Progressive Web App configuration
- Installable on mobile devices
- Offline capability ready

✅ **Environment Detection**: Frontend automatically detects:
- Local development (uses localhost:8000 for API)
- GitHub Pages (uses demo mode)

## Backend Deployment (Optional)
For full functionality, you can deploy the backend to:
- **Railway**: Easy Python deployment
- **Render**: Free tier available
- **Heroku**: Classic platform choice

Then update the API URL in `frontend/script.js`:
```javascript
const API_CONFIG = {
    production: 'https://your-backend-url.com'
};
```

## Troubleshooting

### If GitHub Pages doesn't work:
1. Check the Actions tab for deployment status
2. Ensure repository is public
3. Verify Pages is enabled in Settings

### If you get permission errors:
1. Make sure you're signed in to GitHub
2. Check your Git credentials
3. Use personal access token if needed

## Next Steps
1. Customize the site URL in README.md
2. Add your own branding/styling
3. Deploy backend for full functionality
4. Add more AI features!
