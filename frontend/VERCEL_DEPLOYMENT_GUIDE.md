# Deployment Guide: Frontend on Vercel

This guide will walk you through deploying your frontend application on Vercel and connecting it to your backend.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Git installed on your local machine
3. Your frontend code prepared with the files in this directory

## Step-by-Step Deployment

### Step 1: Prepare Your Frontend Code

Make sure you have these files in your frontend directory:
- `package.json` - Contains project dependencies and scripts
- `next.config.js` - Next.js configuration with backend URL
- `vercel.json` - Vercel-specific configuration
- `README.md` - Information about your project
- `src/` - Your application source code
- `src/services/api.ts` - API service for backend communication

### Step 2: Create a GitHub Repository (if not already done)

1. Create a new repository on GitHub
2. Push your frontend code to this repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with frontend code"
   git branch -M main
   git remote add origin https://github.com/[your-username]/[your-repo-name].git
   git push -u origin main
   ```

### Step 3: Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and log in
2. Click "New Project"
3. Select your GitHub account and choose your frontend repository
4. Vercel will automatically detect it's a Next.js project
5. In the Environment Variables section, add:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://fatimahnoman-phase-three.hf.space`
6. Click "Deploy"

### Step 4: Configure Environment Variables

If you didn't add the environment variable during deployment:

1. Go to your project dashboard on Vercel
2. Click on your project
3. Go to Settings → Environment Variables
4. Add:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://fatimahnoman-phase-three.hf.space`

### Step 5: Verify the Deployment

1. Once deployed, Vercel will provide you with a URL like:
   `https://[your-project-name].vercel.app`
2. Visit this URL to access your frontend
3. Test that API calls are properly routed to your backend

## Important Notes

1. **Backend Connection**: The frontend is configured to connect to your backend at https://fatimahnoman-phase-three.hf.space

2. **API Rewrites**: The configuration includes API rewrites to proxy requests to your backend

3. **Environment Variables**: The `NEXT_PUBLIC_API_URL` variable ensures all API calls go to your deployed backend

4. **Authentication**: The API service handles authentication tokens automatically

## Troubleshooting

- If API calls fail, check that the `NEXT_PUBLIC_API_URL` is correctly set
- If the site doesn't load, verify that your backend is running at the specified URL
- Check browser console for any CORS or network errors

## Updating Your Deployment

To update your deployed application:
1. Make changes to your local code
2. Commit and push the changes to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
3. Vercel will automatically rebuild and redeploy your application