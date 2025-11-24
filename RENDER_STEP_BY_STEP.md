# 📸 Render Deployment - Visual Step-by-Step Guide

This guide walks you through each screen you'll see in Render.

---

## 🎬 PART 1: Setting Up Your Account

### Step 1.1: Sign Up
1. Go to **https://render.com**
2. Click the big **"Get Started for Free"** button
3. Choose **"Sign up with GitHub"** (easiest option)
4. Authorize Render to access your GitHub

**What you'll see**: GitHub authorization screen → Click "Authorize Render"

---

## 🗄️ PART 2: Creating the Database

### Step 2.1: Create New PostgreSQL
1. In Render dashboard, look for **"New +"** button (top right, blue button)
2. Click it → You'll see a dropdown menu
3. Click **"PostgreSQL"**

**What you'll see**: A form with database settings

### Step 2.2: Fill Database Form
Fill in these fields:

```
Name: document-platform-db
(Leave other fields as default)
Region: Oregon (US West)  [or closest to you]
PostgreSQL Version: 16
Plan: Free
```

**What you'll see**: 
- Name field (text input)
- Region dropdown
- Version dropdown
- Plan selector (Free/Starter/etc.)

### Step 2.3: Create and Wait
1. Click **"Create Database"** (green button at bottom)
2. **WAIT 2-3 minutes** - You'll see a progress indicator
3. Once done, you'll see a green checkmark ✅

**What you'll see**: 
- Loading spinner
- "Creating database..." message
- Then: Database dashboard with connection info

### Step 2.4: Copy Database URL
1. In the database dashboard, find **"Connections"** section
2. Look for **"Internal Database URL"**
3. Click the **copy icon** 📋 next to it
4. **SAVE THIS** - You'll need it for backend!

**What you'll see**: 
```
Internal Database URL:
postgresql://user:password@dpg-xxxxx-a/dbname
```

---

## ⚙️ PART 3: Deploying the Backend

### Step 3.1: Create Web Service
1. Click **"New +"** button again
2. Select **"Web Service"**

**What you'll see**: "Create a new Web Service" screen

### Step 3.2: Connect GitHub Repository
1. If you see "Connect account", click it
2. You'll see a list of your GitHub repositories
3. Find: **"AI-Assisted-Document-Authoring-and-Generation-"**
4. Click **"Connect"** next to it

**What you'll see**: 
- List of repositories
- Search box to filter
- "Connect" button next to each repo

### Step 3.3: Configure Backend Service
Fill in the form:

```
Name: document-platform-backend
Region: Oregon (US West)  [same as database]
Branch: master
Root Directory: backend  ⚠️ IMPORTANT!
Runtime: Python 3
Build Command: cd backend && pip install -r requirements.txt && alembic upgrade head
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

**What you'll see**: 
- Form with multiple fields
- Dropdowns for Region, Runtime, Plan
- Text inputs for commands

### Step 3.4: Add Environment Variables
1. Scroll down to **"Environment Variables"** section
2. Click **"Add Environment Variable"** button
3. Add each variable one by one:

**Variable 1:**
```
Key: DATABASE_URL
Value: [paste the database URL you copied]
```

**Variable 2:**
```
Key: JWT_SECRET
Value: [generate random string - see below]
```

**To generate JWT_SECRET**, run this in PowerShell:
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```
Or use any long random string (at least 32 characters)

**Variable 3:**
```
Key: LLM_PROVIDER
Value: gemini
```

**Variable 4:**
```
Key: LLM_API_KEY
Value: [your Gemini API key]
```

**Variable 5:**
```
Key: GEMINI_API_KEY
Value: [your Gemini API key - same as above]
```

**Variable 6:**
```
Key: EXPORT_TMP_DIR
Value: /tmp/exports
```

**Variable 7:**
```
Key: PYTHON_VERSION
Value: 3.11.0
```

**Variable 8 & 9** (Add these AFTER frontend is deployed):
```
Key: FRONTEND_URL
Value: [we'll update this later]

Key: CORS_ORIGINS
Value: [we'll update this later]
```

**What you'll see**: 
- List of environment variables
- "Add Environment Variable" button
- Key/Value input fields

### Step 3.5: Create Backend Service
1. Scroll to bottom
2. Click **"Create Web Service"** (green button)
3. **WAIT 5-10 minutes** for build

**What you'll see**: 
- Build logs scrolling
- "Building..." status
- Then: "Live" status with green dot 🟢

### Step 3.6: Get Backend URL
1. Once deployed, you'll see your service URL at the top
2. It looks like: `https://document-platform-backend.onrender.com`
3. **COPY THIS URL** - You'll need it for frontend!

**What you'll see**: 
- Service dashboard
- URL at the top (clickable link)
- "Live" status indicator

---

## 🗄️ PART 4: Run Database Migrations

**⚠️ IMPORTANT**: Shell is not available in Render's free tier. We'll add migrations to the build command instead.

### Step 4.1: Update Backend Build Command
1. Go to your **Backend Service** dashboard
2. Click **"Settings"** tab (top menu)
3. Scroll down to **"Build Command"** section
4. **Change** the build command from:
   ```
   pip install -r requirements.txt
   ```
   **To:**
   ```
   pip install -r requirements.txt && alembic upgrade head
   ```
5. Click **"Save Changes"** (blue button at bottom)
6. Render will automatically redeploy with the new build command

**What you'll see**: 
- Settings page with build command field
- Save button
- Automatic redeploy starting

### Step 4.2: Verify Migrations Ran
1. After redeploy completes, click **"Logs"** tab
2. Look for messages like:
   - "Running upgrade..."
   - "INFO [alembic.runtime.migration] Running upgrade..."
   - "✓ Upgrade complete" or similar

**What you'll see**: 
- Build logs showing migration output
- Success messages if migrations worked

**Alternative Method** (if above doesn't work):
If you need to run migrations separately, you can temporarily upgrade to a paid plan, run migrations, then downgrade. But the build command method above should work fine!

---

## 🎨 PART 5: Deploying the Frontend

### Step 5.1: Create Static Site
1. Click **"New +"** button
2. Select **"Static Site"**

**What you'll see**: "Create a new Static Site" screen

### Step 5.2: Connect Repository (Same One)
1. Select the same repository: **"AI-Assisted-Document-Authoring-and-Generation-"**
2. Click **"Connect"**

### Step 5.3: Configure Frontend
Fill in:

```
Name: document-platform-frontend
Branch: master
Root Directory: frontend  ⚠️ IMPORTANT!
Build Command: npm install && npm run build
Publish Directory: build
```

**What you'll see**: Similar form to backend, but for static site

### Step 5.4: Add Frontend Environment Variable
1. Scroll to **"Environment Variables"**
2. Click **"Add Environment Variable"**
3. Add:

```
Key: REACT_APP_API_URL
Value: https://document-platform-backend.onrender.com
(Use your actual backend URL from Step 3.6)
```

**What you'll see**: Environment variable form

### Step 5.5: Create Frontend Service
1. Click **"Create Static Site"** (green button)
2. **WAIT 5-10 minutes** for build

**What you'll see**: Build logs, then "Live" status

### Step 5.6: Get Frontend URL
1. Copy the frontend URL (e.g., `https://document-platform-frontend.onrender.com`)
2. **SAVE THIS** - This is your live website!

---

## 🔗 PART 6: Final Configuration

### Step 6.1: Update Backend CORS
1. Go back to your **Backend Service** dashboard
2. Click **"Environment"** tab (top menu)
3. Find these variables and click **"Edit"**:
   - `FRONTEND_URL` → Change to your frontend URL
   - `CORS_ORIGINS` → Change to your frontend URL
4. Click **"Save Changes"**

**What you'll see**: 
- List of environment variables
- Edit buttons
- Save button

### Step 6.2: Wait for Redeploy
1. Render will automatically redeploy
2. Wait 2-3 minutes
3. Check "Logs" tab to see redeploy progress

---

## ✅ PART 7: Testing

### Step 7.1: Visit Your Site
1. Open your frontend URL in a browser
2. You should see the login page!

**What you'll see**: Your beautiful dark-themed login page

### Step 7.2: Test Features
1. Click "Create account" or "Sign in"
2. Register a new account
3. Create a project
4. Try AI features
5. Export a document

**What you'll see**: Your full application working!

---

## 🎉 Success!

If everything works, congratulations! Your app is live on the internet!

---

## 🆘 Common Issues & Solutions

### Issue: "Build failed"
**Solution**: Check "Logs" tab for error messages. Common causes:
- Wrong Root Directory
- Missing dependencies
- Wrong build command

### Issue: "Cannot connect to backend"
**Solution**: 
- Check `REACT_APP_API_URL` in frontend
- Check backend CORS settings
- Make sure backend is "Live" (not "Stopped")

### Issue: "Database connection error"
**Solution**:
- Use Internal Database URL (not External)
- Make sure database and backend are in same region
- Check DATABASE_URL environment variable

### Issue: "Service is sleeping"
**Solution**: 
- Free tier services sleep after 15 min inactivity
- First request takes 30-60 seconds to wake up
- This is normal for free tier!

---

**Need more help? Check the full guide: RENDER_DEPLOYMENT_GUIDE.md**

