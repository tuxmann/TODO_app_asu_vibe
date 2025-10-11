# Frontend Setup Guide

This guide will help you set up and run the Next.js frontend for the TODO App.

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

The frontend needs to know where your FastAPI backend is running. Create a `.env.local` file:

```bash
cd frontend
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
EOF
```

### 3. Start the Development Server

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Full Setup Instructions

### Prerequisites

Before starting, ensure you have:

1. **Node.js** (version 18.x or higher)
   ```bash
   node --version
   ```

2. **npm** (comes with Node.js)
   ```bash
   npm --version
   ```

3. **FastAPI Backend** running on port 8000
   ```bash
   # In another terminal, from project root
   cd /home/jason/Python/fastapi_app/TODO_app_asu_vibe
   python -m uvicorn app.main:app --reload
   ```

### Step-by-Step Installation

#### 1. Navigate to Frontend Directory

```bash
cd /home/jason/Python/fastapi_app/TODO_app_asu_vibe/frontend
```

#### 2. Install Node Modules

```bash
npm install
```

This will install all required dependencies:
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Axios
- And their dependencies

#### 3. Environment Configuration

Create `.env.local` file in the `frontend` directory:

```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
```

**Important:** The `.env.local` file is ignored by git for security reasons.

#### 4. Verify Backend Connection

Before starting the frontend, make sure your FastAPI backend is running:

```bash
# Test the backend health endpoint
curl http://localhost:8000/health
```

You should see a response like:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### 5. Start Development Server

```bash
npm run dev
```

You should see output like:
```
▲ Next.js 14.0.3
- Local:        http://localhost:3000
- Ready in 2.5s
```

#### 6. Open in Browser

Navigate to `http://localhost:3000`

You should be automatically redirected to the login page.

## Usage Guide

### Creating Your First Account

1. Go to `http://localhost:3000`
2. Click **"Sign up here"** at the bottom of the login page
3. Fill in the registration form:
   - **Username**: Choose a unique username (4-32 characters)
   - **Email**: Optional, but recommended
   - **Full Name**: Optional
   - **Password**: Must meet requirements:
     - At least 8 characters
     - 1 uppercase letter
     - 1 lowercase letter  
     - 1 digit
   - **Confirm Password**: Must match password
4. Click **"Create Account"**
5. You'll see a success message and be automatically logged in
6. You'll be redirected to the welcome page

### Logging In

1. Go to `http://localhost:3000/login`
2. Enter your **username** and **password**
3. Click **"Sign In"**
4. You'll be redirected to the welcome page

### Welcome Page

After logging in, you'll see:
- Personalized welcome message
- Your account information
- Quick action cards (for future features)
- Logout button in the navigation bar

### Logging Out

Click the **"Logout"** button in the top-right corner of the navigation bar.

## Development Workflow

### File Structure Overview

```
frontend/
├── src/
│   ├── app/                    # Pages (Next.js App Router)
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home (redirect page)
│   │   ├── login/page.tsx      # Login page
│   │   ├── signup/page.tsx     # Signup page
│   │   └── welcome/page.tsx    # Dashboard
│   ├── contexts/
│   │   └── AuthContext.tsx     # Auth state management
│   └── lib/
│       └── api.ts              # API client
├── public/                      # Static files
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript config
├── tailwind.config.ts          # Tailwind config
└── next.config.js              # Next.js config
```

### Making Changes

1. **Edit files** in `src/` directory
2. **Hot reload** is enabled - changes appear automatically
3. **Check console** for any TypeScript or build errors

### Adding New Pages

Create a new directory in `src/app/`:

```bash
mkdir -p src/app/my-page
touch src/app/my-page/page.tsx
```

Example page:
```typescript
'use client';

export default function MyPage() {
  return (
    <div className="min-h-screen p-8">
      <h1>My New Page</h1>
    </div>
  );
}
```

Access at: `http://localhost:3000/my-page`

### Styling with Tailwind

The app uses Tailwind CSS. Add classes directly to elements:

```typescript
<div className="bg-blue-500 text-white p-4 rounded-lg">
  Styled with Tailwind
</div>
```

## Production Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized production build in `.next/` directory.

### Start Production Server

```bash
npm start
```

### Deploy to Vercel (Recommended)

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Your production API URL
5. Deploy!

### Deploy to Other Platforms

The app can be deployed to:
- **Netlify**
- **AWS Amplify**
- **DigitalOcean App Platform**
- **Railway**
- Any Node.js hosting platform

## Troubleshooting

### Common Issues

#### 1. "Cannot connect to backend"

**Symptoms:** Login/signup fails with connection errors

**Solutions:**
- Verify FastAPI backend is running: `curl http://localhost:8000/health`
- Check `.env.local` has correct API URL
- Check CORS settings in FastAPI backend
- Look at browser console for detailed errors

#### 2. "Module not found" errors

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

#### 3. Port 3000 already in use

**Solution:**
```bash
# Find process using port 3000
lsof -ti:3000

# Kill the process
kill -9 $(lsof -ti:3000)

# Or run on different port
PORT=3001 npm run dev
```

#### 4. TypeScript errors

**Solution:**
```bash
# Check for errors
npm run build

# If errors persist, delete type cache
rm -rf .next
npm run dev
```

#### 5. Styling not working

**Solution:**
```bash
# Ensure Tailwind is properly configured
npm install -D tailwindcss postcss autoprefixer

# Restart dev server
npm run dev
```

#### 6. Authentication loops/redirects

**Solutions:**
- Clear browser localStorage: DevTools → Application → Local Storage → Clear
- Clear cookies
- Restart both frontend and backend
- Check token expiration settings

### Getting Detailed Logs

#### Browser Console

Open DevTools (F12) and check:
- **Console tab**: JavaScript errors
- **Network tab**: API requests/responses
- **Application tab**: localStorage (token)

#### Server Logs

The Next.js dev server shows logs in terminal:
```
GET /login 200 in 45ms
GET /api/auth/me 401 in 12ms
```

## Testing

### Manual Testing Checklist

- [ ] Can register new user
- [ ] Registration validates password requirements
- [ ] Can login with correct credentials
- [ ] Login fails with wrong credentials
- [ ] Welcome page shows user info
- [ ] Can logout
- [ ] After logout, redirected to login
- [ ] Cannot access /welcome without login
- [ ] Token persists across page refreshes

### Testing with Different Browsers

Test on:
- Chrome/Chromium
- Firefox
- Safari (if on Mac)
- Edge

### Mobile Testing

```bash
# Find your local IP
ip addr show | grep 192.168

# Start dev server
npm run dev

# Access from phone: http://192.168.x.x:3000
```

## Performance Optimization

### Production Build Optimizations

Next.js automatically:
- Minifies JavaScript and CSS
- Optimizes images
- Code splits pages
- Tree shakes unused code
- Generates static pages where possible

### Image Optimization

Use Next.js Image component:
```typescript
import Image from 'next/image';

<Image 
  src="/logo.png" 
  width={200} 
  height={100} 
  alt="Logo" 
/>
```

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Yes | FastAPI backend URL | `http://localhost:8000/api/v1` |

**Note:** Variables prefixed with `NEXT_PUBLIC_` are exposed to the browser.

## Scripts Reference

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint |

## Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)

## Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Check browser console for errors
3. Check server logs
4. Review the main README.md
5. Check FastAPI backend logs

## Next Steps

After setting up the frontend:

1. Test the authentication flow
2. Explore the code structure
3. Customize the styling
4. Add TODO list management features
5. Deploy to production

Happy coding! 🚀

