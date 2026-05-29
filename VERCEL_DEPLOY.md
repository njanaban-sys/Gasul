# Deploying GASUL to Vercel

## Steps

1. **Push to GitHub** — push this folder to a GitHub repo.

2. **Import in Vercel** — go to vercel.com → New Project → import your repo.

3. **Set Environment Variables** in Vercel dashboard → Settings → Environment Variables:

   | Variable | Value |
   |---|---|
   | `SECRET_KEY` | any long random string |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-app.vercel.app` |
   | `CSRF_TRUSTED_ORIGINS` | `https://your-app.vercel.app` |
   | `DB_NAME` | `postgres` |
   | `DB_USER` | `postgres.idbsyilhqbbdvrvryxql` |
   | `DB_PASSWORD` | `Dadar27032006` |
   | `DB_HOST` | `aws-1-ap-southeast-1.pooler.supabase.com` |
   | `DB_PORT` | `6543` |

4. **Set Build Command** in Vercel:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Output Directory: *(leave blank)*

5. **Run migrations** once after first deploy:
   ```
   python manage.py migrate
   ```

## Connection String (for reference)
```
postgresql://postgres.idbsyilhqbbdvrvryxql:Dadar27032006@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres
```

## Notes on Media Files
Vercel serverless functions have an **ephemeral filesystem** — uploaded product images
will be lost on each re-deploy. For persistent media storage, consider:
- **Cloudinary** (free tier, easy Django integration)
- **Supabase Storage** (already using Supabase)
- **AWS S3**
