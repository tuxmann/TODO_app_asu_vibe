# Quick Start Guide

Get the TODO App frontend running in 5 minutes!

## TL;DR

```bash
cd frontend
./setup.sh          # Run setup script
npm run dev         # Start dev server
```

Open `http://localhost:3000` 🎉

## Prerequisites

- ✅ Node.js 18+ installed
- ✅ FastAPI backend running on port 8000

## Step by Step

### 1. Run Setup Script

```bash
cd frontend
chmod +x setup.sh
./setup.sh
```

This will:
- Install all dependencies
- Create `.env.local` configuration
- Set up the project

### 2. Start Backend (if not running)

```bash
# In another terminal, from project root
cd ..
python -m uvicorn app.main:app --reload
```

Verify it's running:
```bash
curl http://localhost:8000/health
```

### 3. Start Frontend

```bash
npm run dev
```

### 4. Open Browser

Go to: `http://localhost:3000`

### 5. Create Account

1. Click "Sign up here"
2. Fill in the form
3. Create your account
4. You'll be logged in automatically!

## Manual Setup (if script fails)

```bash
cd frontend
npm install
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1" > .env.local
npm run dev
```

## Troubleshooting

### Port 3000 is busy
```bash
PORT=3001 npm run dev
```

### Can't connect to backend
Check backend is running:
```bash
curl http://localhost:8000/health
```

### Module errors
```bash
rm -rf node_modules package-lock.json
npm install
```

## What's Next?

- 📖 Read [README.md](./README.md) for full documentation
- 🛠️ Read [FRONTEND_SETUP.md](../FRONTEND_SETUP.md) for detailed setup
- 🎨 Customize the UI in `src/app/` files
- 🔧 Modify API calls in `src/lib/api.ts`

## Features to Try

1. **Register** - Create a new account
2. **Login** - Sign in with your credentials
3. **Welcome Page** - View your dashboard
4. **Logout** - Sign out securely

## Need Help?

- Check browser console (F12) for errors
- Check terminal for server logs
- Review `FRONTEND_SETUP.md` for detailed troubleshooting

---

Happy coding! 🚀

