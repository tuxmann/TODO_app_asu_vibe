# TODO App Frontend - Next.js

A modern, beautiful frontend for the TODO App with authentication built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

- 🔐 **Authentication System**
  - User registration with validation
  - User login with JWT tokens
  - Protected routes
  - Automatic token refresh
  - Secure logout

- 🎨 **Beautiful UI/UX**
  - Modern gradient designs
  - Responsive layout (mobile, tablet, desktop)
  - Smooth animations and transitions
  - Loading states and error handling
  - Success confirmations

- 🚀 **Modern Tech Stack**
  - Next.js 14 with App Router
  - TypeScript for type safety
  - Tailwind CSS for styling
  - Axios for API communication
  - React Context for state management

## Prerequisites

- Node.js 18.x or higher
- npm or yarn
- Running FastAPI backend on `http://localhost:8000`

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment configuration:**
   
   Create a `.env.local` file in the frontend directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
   ```

## Running the Application

### Development Mode

```bash
npm run dev
```

The application will start on `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout with AuthProvider
│   │   ├── page.tsx            # Home page (redirects to login/welcome)
│   │   ├── globals.css         # Global styles
│   │   ├── login/
│   │   │   └── page.tsx        # Login page
│   │   ├── signup/
│   │   │   └── page.tsx        # Signup page
│   │   └── welcome/
│   │       └── page.tsx        # Welcome/Dashboard page
│   ├── contexts/
│   │   └── AuthContext.tsx     # Authentication context and hooks
│   └── lib/
│       └── api.ts              # API client and auth functions
├── public/                      # Static assets
├── package.json                # Dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.ts          # Tailwind CSS configuration
├── next.config.js              # Next.js configuration
└── README.md                   # This file
```

## Pages Overview

### 1. Login Page (`/login`)
- Clean, modern login form
- Username and password fields
- Error handling with user-friendly messages
- Link to signup page
- Automatic redirect to welcome page on success

### 2. Signup Page (`/signup`)
- Comprehensive registration form
- Fields:
  - Username (required, 4-32 chars)
  - Email (optional)
  - Full Name (optional)
  - Password (required, with strength requirements)
  - Confirm Password (required)
- Real-time password validation
- Success confirmation message
- Automatic login after successful registration

### 3. Welcome Page (`/welcome`)
- Protected route (requires authentication)
- Personalized welcome message
- User information dashboard:
  - Username
  - Email (if provided)
  - Member since date
  - Account status
  - Account ID
- Quick action cards (placeholders for future features)
- Logout functionality

## API Integration

The application communicates with the FastAPI backend through the following endpoints:

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login/json` - User login
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - Logout

### Authentication Flow

1. User registers or logs in
2. JWT token is stored in localStorage
3. Token is automatically included in all API requests
4. Token is validated on protected routes
5. Expired tokens trigger automatic logout and redirect

## Password Requirements

Passwords must meet the following criteria:
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit

Username requirements:
- 4-32 characters
- Letters, numbers, underscores, and hyphens only

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | FastAPI backend URL | `http://localhost:8000/api/v1` |

## Development Tips

### Running with Backend

1. Start the FastAPI backend:
   ```bash
   # In the project root
   python -m uvicorn app.main:app --reload
   ```

2. Start the Next.js frontend:
   ```bash
   # In the frontend directory
   npm run dev
   ```

3. Open `http://localhost:3000` in your browser

### Testing Authentication

1. Visit `http://localhost:3000`
2. Click "Sign up here" to create an account
3. Fill in the registration form
4. You'll be automatically logged in and redirected to the welcome page
5. Try logging out and logging back in

## Customization

### Colors

The app uses Tailwind CSS with custom color schemes. To customize:

Edit `tailwind.config.ts`:
```typescript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom color palette
      },
    },
  },
}
```

### API URL

To connect to a different backend, update the `.env.local` file:
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com/api/v1
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors:
1. Ensure the FastAPI backend has proper CORS configuration
2. Check that `allow_origins` includes your frontend URL
3. Verify the API URL in `.env.local` is correct

### Authentication Errors

If authentication isn't working:
1. Check that the FastAPI backend is running
2. Verify the API endpoints are accessible
3. Clear browser localStorage and try again
4. Check browser console for error messages

### Build Errors

If you encounter build errors:
```bash
# Clear Next.js cache
rm -rf .next

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

## Future Enhancements

- [ ] TODO list management interface
- [ ] User profile editing
- [ ] Password reset functionality
- [ ] Remember me option
- [ ] Social authentication (Google, GitHub)
- [ ] Dark mode toggle
- [ ] Mobile app (React Native)

## License

This project is part of the TODO App ASU Vibe application.

## Support

For issues or questions, please refer to the main project documentation or create an issue in the repository.

