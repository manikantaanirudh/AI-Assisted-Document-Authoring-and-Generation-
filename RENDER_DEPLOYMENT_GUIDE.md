# Complete Render Deployment Guide

## 📚 What is Render?

Render is a cloud platform that makes it easy to deploy web applications. Think of it as a service that:
- Hosts your backend (FastAPI) server
- Hosts your frontend (React) website
- Provides a PostgreSQL database
- Handles all the server management for you

**Free Tier Available**: Render offers a free tier perfect for learning and small projects!

---

## 🎯 Overview: What We're Deploying

Your application has **3 parts** that need to be deployed:

1. **PostgreSQL Database** - Stores all your data
2. **Backend Service** (FastAPI) - Handles API requests
3. **Frontend Service** (React) - The website users see

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- ✅ A GitHub account (you already have this!)
- ✅ Your code pushed to GitHub (already done!)
- ✅ A Render account (we'll create this)
- ✅ Your Gemini API key ready

---

## 🚀 Step-by-Step Deployment

### **STEP 1: Create Render Account**

1. Go to **https://render.com**
2. Click **"Get Started for Free"** or **"Sign Up"**
3. Sign up using your **GitHub account** (easiest option)
4. Authorize Render to access your GitHub repositories

---

### **STEP 2: Create PostgreSQL Database**

1. In your Render dashboard, click **"New +"** button (top right)
2. Select **"PostgreSQL"**
3. Fill in the form:
   - **Name**: `document-platform-db` (or any name you like)
   - **Database**: `document_platform` (or leave default)
   - **User**: Leave default (auto-generated)
   - **Region**: Choose closest to you (e.g., `Oregon (US West)`)
   - **PostgreSQL Version**: `16` (or latest)
   - **Plan**: Select **"Free"** (for testing)
4. Click **"Create Database"**
5. **IMPORTANT**: Wait 2-3 minutes for database to be created
6. Once created, click on your database
7. Find **"Internal Database URL"** - **COPY THIS** (looks like: `postgresql://user:password@host:port/dbname`)
   - This is your `DATABASE_URL` - save it for later!

---

### **STEP 3: Deploy Backend (FastAPI)**

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click **"Connect account"** if not connected
   - Find and select: `AI-Assisted-Document-Authoring-and-Generation-`
   - Click **"Connect"**
3. Configure the service:
   - **Name**: `document-platform-backend` (or any name)
   - **Region**: Same as database (e.g., `Oregon (US West)`)
   - **Branch**: `master` (or `main`)
   - **Root Directory**: `backend` ⚠️ **IMPORTANT!**
   - **Runtime**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt && alembic upgrade head`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Select **"Free"**
4. Click **"Advanced"** to add Environment Variables:
   
   Add these variables (click "Add Environment Variable" for each):
   
   | Key | Value | Notes |
   |-----|-------|-------|
   | `DATABASE_URL` | `[paste your database URL from Step 2]` | The Internal Database URL you copied |
   | `JWT_SECRET` | `[generate a random secret]` | Use: `openssl rand -hex 32` or any long random string |
   | `LLM_PROVIDER` | `gemini` | |
   | `LLM_API_KEY` | `[your Gemini API key]` | Your Gemini API key |
   | `GEMINI_API_KEY` | `[your Gemini API key]` | Same as above |
   | `FRONTEND_URL` | `https://your-frontend-name.onrender.com` | We'll update this after deploying frontend |
   | `CORS_ORIGINS` | `https://your-frontend-name.onrender.com` | Same as above |
   | `EXPORT_TMP_DIR` | `/tmp/exports` | For Render's temporary storage |
   | `PYTHON_VERSION` | `3.11.0` | Python version |

5. Click **"Create Web Service"**
6. Wait 5-10 minutes for the build to complete
7. Once deployed, you'll get a URL like: `https://document-platform-backend.onrender.com`
   - **COPY THIS URL** - this is your backend API URL!

---

### **STEP 4: Update Backend Environment Variables**

After deploying frontend (next step), come back and update:
- `FRONTEND_URL` → Your frontend URL
- `CORS_ORIGINS` → Your frontend URL

Click on your backend service → **"Environment"** tab → Edit the variables → **"Save Changes"**

---

### **STEP 5: Database Migrations (Already Included!)**

**✅ Good News**: Migrations are already included in the build command above!

The build command `pip install -r requirements.txt && alembic upgrade head` will:
1. Install all Python packages
2. Automatically run database migrations
3. Create all necessary tables

**Verify**: After deployment, check the **"Logs"** tab to see migration output. You should see messages like:
- "Running upgrade..."
- "INFO [alembic.runtime.migration] Running upgrade..."
- Success messages confirming tables were created

**Note**: Shell access is not available in Render's free tier, so we include migrations in the build process instead.

---

### **STEP 6: Deploy Frontend (React)**

1. In Render dashboard, click **"New +"** → **"Static Site"**
2. Connect your GitHub repository (same one)
3. Configure:
   - **Name**: `document-platform-frontend` (or any name)
   - **Branch**: `master` (or `main`)
   - **Root Directory**: `frontend` ⚠️ **IMPORTANT!**
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`
   - **Environment Variables**: Click "Add Environment Variable"
     - **Key**: `REACT_APP_API_URL`
     - **Value**: `https://your-backend-url.onrender.com` (from Step 3)
4. Click **"Create Static Site"**
5. Wait 5-10 minutes for build
6. Once deployed, you'll get a URL like: `https://document-platform-frontend.onrender.com`
   - This is your live website! 🎉

---

### **STEP 7: Update Backend CORS (Final Step)**

1. Go back to your **Backend Service** in Render
2. Click **"Environment"** tab
3. Update these variables:
   - `FRONTEND_URL` → `https://document-platform-frontend.onrender.com`
   - `CORS_ORIGINS` → `https://document-platform-frontend.onrender.com`
4. Click **"Save Changes"**
5. Render will automatically redeploy with new settings

---

## 🔧 Troubleshooting

### Backend won't start?
- Check **"Logs"** tab in Render dashboard
- Make sure `DATABASE_URL` is correct
- Verify all environment variables are set

### Frontend can't connect to backend?
- Check `REACT_APP_API_URL` in frontend environment variables
- Make sure backend URL is correct (no trailing slash)
- Check backend CORS settings

### Database connection errors?
- Verify `DATABASE_URL` uses **Internal Database URL** (not External)
- Make sure database is fully created (wait 2-3 minutes)
- Check database is in same region as backend

### Build fails?
- Check **"Logs"** tab for error messages
- Make sure `Root Directory` is set correctly (`backend` or `frontend`)
- Verify all dependencies are in `requirements.txt` or `package.json`

---

## 📝 Quick Reference: Environment Variables

### Backend Environment Variables:
```
DATABASE_URL=postgresql://user:pass@host:port/dbname
JWT_SECRET=your-random-secret-here
LLM_PROVIDER=gemini
LLM_API_KEY=your-gemini-api-key
GEMINI_API_KEY=your-gemini-api-key
FRONTEND_URL=https://your-frontend.onrender.com
CORS_ORIGINS=https://your-frontend.onrender.com
EXPORT_TMP_DIR=/tmp/exports
PYTHON_VERSION=3.11.0
```

### Frontend Environment Variables:
```
REACT_APP_API_URL=https://your-backend.onrender.com
```

---

## 🎉 You're Done!

Once everything is deployed:
1. Visit your frontend URL
2. Register a new account
3. Start creating documents!

---

## 💡 Pro Tips

1. **Free Tier Limits**: 
   - Services spin down after 15 minutes of inactivity
   - First request after spin-down takes 30-60 seconds
   - Upgrade to paid plan for always-on services

2. **Database Backups**: 
   - Free tier doesn't include automatic backups
   - Consider upgrading for production use

3. **Custom Domains**: 
   - You can add your own domain in Render settings
   - Free tier supports custom domains

4. **Monitoring**: 
   - Check "Metrics" tab to see service health
   - "Logs" tab shows real-time application logs

---

## 🆘 Need Help?

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Check your service logs in Render dashboard

---

**Good luck with your deployment! 🚀**

