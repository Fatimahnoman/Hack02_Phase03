# Deployment Guide: Backend on Hugging Face Spaces

This guide will walk you through deploying your backend application on Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at https://huggingface.co/join)
2. Git installed on your local machine
3. Your backend code prepared with the files in this directory

## Step-by-Step Deployment

### Step 1: Create a New Space on Hugging Face

1. Log in to your Hugging Face account
2. Click on your profile picture in the top-right corner
3. Select "New Space"
4. Fill in the form:
   - Name: Choose a unique name for your space
   - License: Select an appropriate license
   - SDK: Select "Docker" (we're using a custom Dockerfile)
   - Hardware: Choose CPU or GPU based on your needs
   - Visibility: Public or Private as per your preference
5. Click "Create Space"

### Step 2: Clone Your Space Repository

Once your space is created, Hugging Face will provide you with a git repository URL. Clone it:

```bash
git clone https://huggingface.co/spaces/[your-username]/[your-space-name]
cd [your-space-name]
```

### Step 3: Copy Your Backend Files

Copy all the necessary files to your space directory:

```bash
# From your project directory, copy the backend files
cp -r E:\Hackathon_Two\Phase_03\backend/* [your-space-directory]/
```

Make sure these files are copied:
- `app.py` - Entry point for the application
- `Dockerfile` - Container configuration
- `README.md` - Information about your space
- `requirements.txt` - Python dependencies
- `huggingface.yml` - Hugging Face configuration
- The entire `src` directory with your application code
- Any other necessary files

### Step 4: Configure Environment Variables

If your application requires environment variables (API keys, database URLs, etc.):

1. Go to your Space page on Hugging Face
2. Navigate to the "Files" tab
3. Look for "Secrets" or "Environment Variables" settings
4. Add your required environment variables:
   - DATABASE_URL
   - COHERE_API_KEY
   - JWT_SECRET_KEY
   - Any other required variables

### Step 5: Commit and Push Your Code

```bash
git add .
git commit -m "Add backend application for deployment"
git push origin main
```

### Step 6: Monitor the Deployment

1. After pushing, Hugging Face will automatically start building your Space
2. Go to the "Logs" tab in your Space to monitor the build process
3. Wait for the build to complete (this may take several minutes)
4. Once built, your application will be accessible at:
   `https://[your-username]-[your-space-name].hf.space`

## Important Notes

1. **Database Configuration**: If your application uses a persistent database, consider using a cloud database service (like Neon.tech, AWS RDS, etc.) rather than a local SQLite file, as the Space filesystem is ephemeral.

2. **API Keys**: Never hardcode API keys in your source code. Always use environment variables or Hugging Face Secrets.

3. **Port Configuration**: The application is configured to run on port 7860, which is the standard port for Hugging Face Spaces.

4. **Build Time**: The first build may take several minutes as it installs all dependencies. Subsequent builds will be faster due to Docker layer caching.

5. **Rate Limits**: Free Hugging Face Spaces go to sleep after 48 hours of inactivity. Consider upgrading to PRO tier if you need consistent uptime.

## Troubleshooting

- If the build fails, check the "Logs" tab for error messages
- Ensure all required dependencies are listed in requirements.txt
- Make sure your application listens on the PORT environment variable (defaults to 7860)
- Verify that your Dockerfile is correctly configured

## Updating Your Deployment

To update your deployed application:
1. Make changes to your local code
2. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
3. Hugging Face will automatically rebuild and redeploy your application