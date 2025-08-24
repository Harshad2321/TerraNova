# 🚀 Step-by-Step Deployment Instructions

## 🥇 Method 1: Vercel (Recommended)

### Why Vercel?
- ✅ **Free tier** with generous limits
- ✅ **Automatic HTTPS** and global CDN
- ✅ **GitHub integration** for auto-deploys
- ✅ **Supports both** frontend and backend
- ✅ **Zero configuration** needed

### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from your TerraNova directory**
   ```bash
   cd "c:\Users\pradi\OneDrive\Documents\GitHub\TerraNova"
   vercel --prod
   ```

4. **Follow the prompts:**
   - Link to existing project? **N**
   - Project name: **terranova**
   - Directory: **./  (current directory)**
   - Auto-deploy? **Y**

5. **Your app will be live at:** `https://terranova-[random].vercel.app`

### Update Frontend API URL:
After deployment, update `frontend/script.js` to use your new backend URL:
```javascript
// Change this line:
const response = await fetch("http://127.0.0.1:8000/city/generate_plan", {

// To this (replace with your actual Vercel URL):
const response = await fetch("https://your-app-name.vercel.app/api/city/generate_plan", {
```

---

## 🥈 Method 2: Netlify + Railway

### Frontend on Netlify (Free)

1. **Go to [netlify.com](https://netlify.com)**
2. **Drag and drop** your `frontend/` folder
3. **Your frontend is live** at `https://random-name.netlify.app`

### Backend on Railway (Free tier)

1. **Go to [railway.app](https://railway.app)**
2. **Connect your GitHub** repository
3. **Deploy from** `backend/` folder
4. **Environment variables:**
   - `PORT`: 8000
   - `PYTHONPATH`: /app

---

## 🥉 Method 3: GitHub Pages + External Backend

### Frontend on GitHub Pages (Free)

1. **Push your code to GitHub**
2. **Go to repository Settings**
3. **Enable GitHub Pages** from `main` branch `/frontend` folder
4. **Your site is live** at `https://username.github.io/TerraNova`

### Backend Options:
- **Railway** (free tier)
- **Heroku** ($7/month)
- **PythonAnywhere** (free tier)

---

## 🐳 Method 4: Docker Deployment

### For Any Cloud Provider

1. **Build Docker image**
   ```bash
   docker build -t terranova .
   ```

2. **Run locally to test**
   ```bash
   docker run -p 8000:8000 terranova
   ```

3. **Deploy to:**
   - **AWS ECS/Fargate**
   - **Google Cloud Run**
   - **Azure Container Instances**
   - **DigitalOcean App Platform**

---

## 🌩️ Method 5: Cloud Platforms

### AWS (Amazon Web Services)
- **Frontend**: S3 + CloudFront
- **Backend**: Lambda + API Gateway
- **Cost**: Pay-as-you-go

### Google Cloud Platform
- **Frontend**: Firebase Hosting
- **Backend**: Cloud Run
- **Cost**: Free tier available

### Microsoft Azure
- **Frontend**: Static Web Apps
- **Backend**: Container Instances
- **Cost**: Free tier available

---

## 📱 Method 6: Mobile App (PWA)

Your TerraNova is already a **Progressive Web App**! Users can:

1. **Open in mobile browser**
2. **"Add to Home Screen"**
3. **Use like a native app**

To enhance PWA features, add:
- Service worker for offline functionality
- Web app manifest
- Push notifications

---

## 🔧 Production Optimizations

### 1. **Environment Variables**
```bash
# Backend
export API_URL="https://your-backend.com"
export DEBUG="false"
export LOG_LEVEL="info"

# Frontend
export BACKEND_URL="https://your-backend.com/api"
```

### 2. **Performance Optimizations**
- Minify CSS/JavaScript
- Compress images
- Enable gzip compression
- Use CDN for static assets

### 3. **Security**
- Enable CORS properly
- Use HTTPS everywhere
- Add rate limiting
- Implement API authentication

### 4. **Monitoring**
- Add error tracking (Sentry)
- Set up analytics (Google Analytics)
- Monitor uptime (UptimeRobot)
- Log aggregation (LogRocket)

---

## 🎯 Quick Start Recommendations

### For Beginners:
👉 **Use Vercel** - One command deployment

### For Static Sites:
👉 **Use Netlify** - Drag and drop frontend

### For Full Control:
👉 **Use Docker** - Deploy anywhere

### For Enterprise:
👉 **Use AWS/GCP/Azure** - Scalable infrastructure

---

## 🆘 Troubleshooting

### Common Issues:

**❌ "Build failed"**
- Check Python version (3.8+)
- Verify all dependencies in requirements.txt
- Check for syntax errors

**❌ "CORS errors"**
- Update backend CORS settings
- Check API URLs in frontend
- Verify protocol (http vs https)

**❌ "Function timeout"**
- Optimize city generation algorithm
- Add pagination for large grids
- Implement caching

### Getting Help:
- Check deployment logs
- Test locally first
- Use platform documentation
- Ask community forums

---

## 🎉 Your TerraNova is Ready for the World!

Choose your deployment method and share your AI city builder with everyone! 🌍✨
