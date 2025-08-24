# 🚀 TerraNova Deployment Guide

## 🌐 Deployment Options

### 1. **Vercel (Recommended for Beginners)**

**Frontend + Backend Together**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json` in root directory**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "backend/main.py",
         "use": "@vercel/python"
       },
       {
         "src": "frontend/**",
         "use": "@vercel/static"
       }
     ],
     "routes": [
       {
         "src": "/api/(.*)",
         "dest": "backend/main.py"
       },
       {
         "src": "/(.*)",
         "dest": "frontend/$1"
       }
     ]
   }
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

---

### 2. **Netlify (Best for Frontend)**

**Frontend Only (Static)**
1. Build static version
2. Upload `frontend/` folder to Netlify
3. Configure redirects for SPA

**With Netlify Functions (Backend)**
1. Move backend to `netlify/functions/`
2. Convert FastAPI to serverless functions

---

### 3. **Heroku (Full Stack)**

**Complete Application**

1. **Create `Procfile`**
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Create `runtime.txt`**
   ```
   python-3.11.0
   ```

3. **Update `requirements.txt`**
   ```
   fastapi>=0.104.1
   uvicorn[standard]>=0.24.0
   pydantic>=2.5.0
   numpy>=1.24.0
   python-multipart>=0.0.6
   gunicorn>=21.2.0
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

---

### 4. **Railway (Modern Alternative)**

1. **Connect GitHub repository**
2. **Auto-deploys from main branch**
3. **Supports both frontend and backend**

---

### 5. **Docker Deployment**

**For Any Cloud Provider**

1. **Create `Dockerfile`**
2. **Build and deploy container**
3. **Works on AWS, GCP, Azure, DigitalOcean**

---

### 6. **GitHub Pages (Frontend Only)**

**Static Frontend with External Backend**
1. Enable GitHub Pages
2. Deploy frontend to `gh-pages` branch
3. Use external API service

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Best For |
|----------|-----------|------------|----------|
| Vercel | Yes (Generous) | $20/month | Full-stack apps |
| Netlify | Yes | $19/month | Static sites + functions |
| Heroku | No (was free) | $7/month | Full applications |
| Railway | Yes (Limited) | $5/month | Modern apps |
| GitHub Pages | Yes | Free | Static sites only |

---

## 🎯 Recommended Approach

**For TerraNova, I recommend Vercel because:**
- ✅ Supports both frontend and backend
- ✅ Easy deployment process
- ✅ Generous free tier
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ GitHub integration

---

## 🔧 Quick Setup Instructions

Choose your preferred method below:
