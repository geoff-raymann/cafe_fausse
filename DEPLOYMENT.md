# 🚀 Deployment Checklist

## Pre-Deployment

### Backend
- [ ] All environment variables documented in `.env.example`
- [ ] `ENVIRONMENT=production` set
- [ ] `DEBUG=False` set
- [ ] Strong `JWT_SECRET` configured (minimum 32 characters)
- [ ] Admin password changed from default
- [ ] Email configuration tested (Gmail App Password)
- [ ] Database backup strategy in place
- [ ] Logging level set appropriately
- [ ] CORS origins include production frontend URL
- [ ] Health check endpoint responding: `/health`

### Frontend
- [ ] `REACT_APP_API_URL` points to production backend
- [ ] All hardcoded localhost URLs removed
- [ ] Build process tested: `npm run build`
- [ ] Error boundaries implemented
- [ ] Loading states for all async operations
- [ ] Form validation working
- [ ] Mobile responsiveness verified

### Security
- [ ] Admin credentials changed from defaults
- [ ] Secret codes for admin access gate updated
- [ ] JWT token expiration configured
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (input sanitization)
- [ ] HTTPS enabled on all endpoints
- [ ] Sensitive data not logged

## Railway Deployment (Backend)

### Step 1: Create Project
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `cafe-fausse-backend` repository/folder

### Step 2: Add Database
1. Click "New" → "Database" → "PostgreSQL"
2. Railway auto-sets `DATABASE_URL` variable
3. Database is automatically connected to backend

### Step 3: Configure Environment Variables
Go to backend service → Variables tab:

```bash
ENVIRONMENT=production
DEBUG=False
JWT_SECRET=<generate-strong-key-32+-characters>
JWT_EXPIRATION_HOURS=24
ADMIN_PASSWORD=<change-this-password>
EMAIL_ENABLED=True
EMAIL_ADDRESS=<your-gmail>
EMAIL_PASSWORD=<gmail-app-password>
ADMIN_EMAIL=<admin-email>
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com
CAFE_NAME=Café Fausse
CAFE_PHONE=+1 (555) 123-4567
CAFE_ADDRESS=123 Digital Street, Virtual City, VC 12345
TOTAL_TABLES=20
MIN_GUESTS_PER_RESERVATION=1
MAX_GUESTS_PER_RESERVATION=10
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=True
```

### Step 4: Verify Deployment
1. Check deployment logs for errors
2. Visit `/health` endpoint to verify API is running
3. Check database tables are created
4. Test a sample API call

### Step 5: Get Backend URL
1. Go to Settings → Domains
2. Copy the Railway-provided URL (e.g., `your-app.railway.app`)
3. Use this for frontend `REACT_APP_API_URL`

## Vercel Deployment (Frontend)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login
```bash
vercel login
```

### Step 3: Deploy from Frontend Directory
```bash
cd cafe-fausse-frontend
vercel
```

Follow prompts:
- Set up and deploy? **Y**
- Which scope? (Select your account)
- Link to existing project? **N**
- Project name? `cafe-fausse-frontend`
- Directory? `./`
- Override settings? **N**

### Step 4: Set Environment Variables
In Vercel Dashboard:
1. Go to Project Settings → Environment Variables
2. Add variables:
   ```
   REACT_APP_API_URL = https://your-backend.railway.app
   ```
3. Scope: All (Production, Preview, Development)

### Step 5: Deploy to Production
```bash
vercel --prod
```

### Step 6: Custom Domain (Optional)
1. Go to Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Wait for DNS propagation (up to 48 hours)

## Post-Deployment

### Backend Verification
- [ ] Health check: `https://your-backend.railway.app/health`
- [ ] Admin login working
- [ ] Reservation creation working
- [ ] Email notifications being sent
- [ ] Database persisting data
- [ ] CORS allowing frontend requests
- [ ] Logs showing no critical errors

### Frontend Verification
- [ ] Site loads: `https://your-frontend.vercel.app`
- [ ] All pages accessible
- [ ] Reservations form working
- [ ] Admin login functional
- [ ] API calls succeeding
- [ ] Mobile responsive
- [ ] No console errors

### Integration Testing
Test complete user flow:
1. **Customer Journey:**
   - [ ] Make a reservation
   - [ ] Receive confirmation email
   - [ ] Subscribe to newsletter

2. **Admin Journey:**
   - [ ] Access admin gate
   - [ ] Login to admin dashboard
   - [ ] View bookings
   - [ ] View subscribers
   - [ ] Check notifications
   - [ ] Cancel a booking

### Performance
- [ ] Backend response time < 500ms
- [ ] Frontend load time < 3s
- [ ] Database queries optimized
- [ ] Images optimized
- [ ] No memory leaks

### Monitoring Setup
- [ ] Railway logs configured
- [ ] Vercel analytics enabled
- [ ] Error tracking (optional: Sentry)
- [ ] Uptime monitoring (optional: UptimeRobot)
- [ ] Database backups scheduled

## Update CORS in Backend

After getting frontend URL, update backend:

**Railway:**
1. Go to backend service → Variables
2. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://your-frontend.vercel.app,https://custom-domain.com
   ```
3. Redeploy

## Database Backup

### Manual Backup (Railway)
```bash
# Get database URL from Railway
railway variables get DATABASE_URL

# Backup
pg_dump <DATABASE_URL> > backup.sql
```

### Restore
```bash
psql <DATABASE_URL> < backup.sql
```

## Rollback Plan

### Backend Rollback
1. Go to Railway → Deployments
2. Select previous successful deployment
3. Click "Redeploy"

### Frontend Rollback
```bash
vercel rollback
```

Or in Vercel dashboard:
1. Go to Deployments
2. Find previous deployment
3. Click "..." → "Promote to Production"

## Troubleshooting

### Backend Issues
**Database connection failed:**
- Check `DATABASE_URL` is set correctly
- Verify PostgreSQL database is running
- Check network connectivity

**Email not sending:**
- Verify Gmail App Password
- Check `EMAIL_ENABLED=True`
- Review email logs in Railway

**CORS errors:**
- Ensure frontend URL in `CORS_ORIGINS`
- Check for trailing slashes
- Verify HTTPS vs HTTP

### Frontend Issues
**API calls failing:**
- Check `REACT_APP_API_URL` is correct
- Verify backend is running
- Check CORS configuration
- Review browser console for errors

**Build failures:**
- Clear build cache in Vercel
- Check for import errors
- Verify all dependencies in `package.json`

### Performance Issues
**Slow response times:**
- Check database query performance
- Review connection pool settings
- Consider adding Redis caching
- Optimize images

**High memory usage:**
- Review connection pool size
- Check for memory leaks
- Monitor Railway metrics

## Monitoring Commands

### Railway
```bash
# View logs
railway logs

# View variables
railway variables

# Run commands in Railway environment
railway run python app.py
```

### Vercel
```bash
# View deployments
vercel list

# View logs
vercel logs

# Inspect deployment
vercel inspect <deployment-url>
```

## Emergency Contacts

- Railway Support: [help.railway.app](https://help.railway.app)
- Vercel Support: [vercel.com/support](https://vercel.com/support)
- Database Issues: Check Railway dashboard

## Cost Monitoring

### Railway
- Free tier: $5 credit/month
- Monitor usage in dashboard
- Set up billing alerts

### Vercel
- Free tier: 100 GB bandwidth
- Monitor in dashboard
- Upgrade if needed

## Success Criteria

Deployment is successful when:
- ✅ All tests pass
- ✅ Health check returns 200
- ✅ Reservations can be created
- ✅ Emails are being sent
- ✅ Admin login works
- ✅ No critical errors in logs
- ✅ Response times acceptable
- ✅ Mobile responsive
- ✅ HTTPS enabled
- ✅ Backups configured

---

**Last Updated:** 2024
**Version:** 1.0.0
