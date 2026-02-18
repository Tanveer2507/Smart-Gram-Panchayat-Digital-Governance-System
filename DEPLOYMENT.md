# Vercel Deployment Guide

## Prerequisites
- A Vercel account (sign up at https://vercel.com)
- Git repository pushed to GitHub

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com and sign in
2. Click "Add New Project"
3. Import your GitHub repository: `Smart-Gram-Panchayat-Digital-Governance-System`
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: Leave as default (root)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
5. Add Environment Variables (optional):
   - `SECRET_KEY`: Your Django secret key
   - `DEBUG`: False (for production)
6. Click "Deploy"

### Option 2: Deploy via Vercel CLI

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy from your project directory:
```bash
vercel
```

4. Follow the prompts and confirm deployment

## Important Notes

⚠️ **Database Limitation**: 
- Vercel uses serverless functions, which means SQLite database will reset on each deployment
- For production, you should use an external database like:
  - PostgreSQL (Neon, Supabase, Railway)
  - MySQL (PlanetScale)
  - MongoDB Atlas

⚠️ **Static Files**:
- Static files are served via WhiteNoise
- Run `python manage.py collectstatic` before deployment (handled automatically)

⚠️ **Media Files**:
- User-uploaded files won't persist on Vercel
- Use external storage like AWS S3, Cloudinary, or Vercel Blob

## Post-Deployment

After successful deployment:

1. Your app will be available at: `https://your-project-name.vercel.app`
2. Create a superuser (you'll need to use a persistent database for this)
3. Configure your domain (optional)

## Troubleshooting

If deployment fails:
- Check Vercel deployment logs
- Ensure all dependencies are in requirements.txt
- Verify Python version compatibility (3.9+)
- Check that ALLOWED_HOSTS includes '.vercel.app'

## Recommended Next Steps

1. Set up a PostgreSQL database (Neon.tech offers free tier)
2. Configure environment variables in Vercel dashboard
3. Set up external media storage
4. Enable HTTPS and configure security settings
5. Set DEBUG=False for production
