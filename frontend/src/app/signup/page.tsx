'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

// Helper function to parse and format detailed error messages
const parseErrorMessage = (error: any): { title: string; details: string[]; suggestion?: string } => {
  console.log('Full error object:', error);
  
  // Default error structure
  let title = 'Registration Failed';
  let details: string[] = [];
  let suggestion: string | undefined;

  // Try to extract the error message from various possible locations
  const errorMessage = 
    error?.response?.data?.detail || 
    error?.message || 
    'Unknown error occurred';

  console.log('Error message:', errorMessage);

  // Check for specific error types
  if (typeof errorMessage === 'string') {
    const lowerMsg = errorMessage.toLowerCase();
    
    // Username already exists
    if (lowerMsg.includes('username') && (lowerMsg.includes('exists') || lowerMsg.includes('already'))) {
      title = 'Username Already Taken';
      details = [
        'This username is already registered in our system',
        `The username "${error.username || 'you entered'}" is not available`
      ];
      suggestion = 'Please try a different username or sign in if you already have an account';
    }
    // Email already exists
    else if (lowerMsg.includes('email') && (lowerMsg.includes('exists') || lowerMsg.includes('already'))) {
      title = 'Email Already Registered';
      details = [
        'This email address is already associated with an account',
        'Each email can only be used once'
      ];
      suggestion = 'Try signing in, or use a different email address';
    }
    // Password validation errors
    else if (lowerMsg.includes('password')) {
      title = 'Password Requirements Not Met';
      details = [errorMessage];
      
      if (lowerMsg.includes('uppercase')) {
        details.push('Must contain at least one uppercase letter (A-Z)');
      }
      if (lowerMsg.includes('lowercase')) {
        details.push('Must contain at least one lowercase letter (a-z)');
      }
      if (lowerMsg.includes('digit') || lowerMsg.includes('number')) {
        details.push('Must contain at least one digit (0-9)');
      }
      if (lowerMsg.includes('8 characters') || lowerMsg.includes('length')) {
        details.push('Must be at least 8 characters long');
      }
      
      suggestion = 'Create a stronger password that meets all requirements';
    }
    // Username format errors
    else if (lowerMsg.includes('username') && (lowerMsg.includes('only contain') || lowerMsg.includes('invalid') || lowerMsg.includes('alphanumeric'))) {
      title = 'Invalid Username Format';
      details = [
        errorMessage,
        'Username can only contain letters, numbers, underscores (_), and hyphens (-)',
        'Username must be between 4 and 32 characters'
      ];
      suggestion = 'Choose a username with only allowed characters';
    }
    // Network/connection errors
    else if (lowerMsg.includes('network') || lowerMsg.includes('connection') || lowerMsg.includes('timeout')) {
      title = 'Connection Problem';
      details = [
        'Unable to connect to the server',
        'This might be a temporary network issue'
      ];
      suggestion = 'Please check your internet connection and try again';
    }
    // Server errors
    else if (lowerMsg.includes('500') || lowerMsg.includes('internal server')) {
      title = 'Server Error';
      details = [
        'The server encountered an unexpected error',
        'This is not your fault - something went wrong on our end'
      ];
      suggestion = 'Please try again in a few moments, or contact support if the problem persists';
    }
    // Database errors
    else if (lowerMsg.includes('database') || lowerMsg.includes('db')) {
      title = 'Database Error';
      details = [
        'There was a problem saving your account',
        'The database service may be temporarily unavailable'
      ];
      suggestion = 'Please try again in a moment';
    }
    // Generic validation error
    else if (lowerMsg.includes('validation') || lowerMsg.includes('invalid')) {
      title = 'Validation Error';
      details = [errorMessage];
      suggestion = 'Please check all fields and ensure they meet the requirements';
    }
    // Default case - show the exact error message
    else {
      details = [errorMessage];
      suggestion = 'Please check your information and try again';
    }
  } else if (Array.isArray(errorMessage)) {
    // Handle array of errors
    title = 'Multiple Validation Errors';
    details = errorMessage;
    suggestion = 'Please fix the errors above and try again';
  } else if (typeof errorMessage === 'object' && errorMessage !== null) {
    // Handle object with multiple error fields
    title = 'Validation Errors';
    details = Object.entries(errorMessage).map(([field, msg]) => `${field}: ${msg}`);
    suggestion = 'Please correct the errors above';
  }

  // Check for HTTP status codes
  const status = error?.response?.status;
  if (status === 400) {
    if (details.length === 0) {
      details = ['The information you provided is invalid or incomplete'];
    }
  } else if (status === 409) {
    if (title === 'Registration Failed') {
      title = 'Conflict - Resource Already Exists';
    }
  } else if (status === 422) {
    if (title === 'Registration Failed') {
      title = 'Unprocessable Entity';
      details = ['The server cannot process your request due to validation errors'];
    }
  } else if (status === 503) {
    title = 'Service Unavailable';
    details = ['The server is temporarily unavailable'];
    suggestion = 'Please try again in a few minutes';
  }

  // If still no details, provide a generic message
  if (details.length === 0) {
    details = ['An unexpected error occurred during registration'];
  }

  return { title, details, suggestion };
};

export default function SignupPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [errorInfo, setErrorInfo] = useState<{ title: string; details: string[]; suggestion?: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const { register } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorInfo(null);
    setLoading(true);

    // Validate passwords match
    if (password !== confirmPassword) {
      setErrorInfo({
        title: 'Passwords Do Not Match',
        details: [
          'The password and confirm password fields must be identical',
          'Please make sure you typed the same password in both fields'
        ],
        suggestion: 'Check your password carefully and re-enter it in both fields'
      });
      setLoading(false);
      return;
    }

    // Validate password requirements
    const passwordErrors: string[] = [];
    if (password.length < 8) {
      passwordErrors.push('Password must be at least 8 characters long');
    }
    if (!/[A-Z]/.test(password)) {
      passwordErrors.push('Password must contain at least one uppercase letter (A-Z)');
    }
    if (!/[a-z]/.test(password)) {
      passwordErrors.push('Password must contain at least one lowercase letter (a-z)');
    }
    if (!/[0-9]/.test(password)) {
      passwordErrors.push('Password must contain at least one digit (0-9)');
    }

    if (passwordErrors.length > 0) {
      setErrorInfo({
        title: 'Password Requirements Not Met',
        details: passwordErrors,
        suggestion: 'Create a stronger password that includes uppercase, lowercase, and numbers'
      });
      setLoading(false);
      return;
    }

    // Validate username format (client-side check)
    if (username.length < 4 || username.length > 32) {
      setErrorInfo({
        title: 'Invalid Username Length',
        details: [
          `Username must be between 4 and 32 characters (currently ${username.length} characters)`,
          'Please choose a shorter or longer username'
        ]
      });
      setLoading(false);
      return;
    }

    if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
      setErrorInfo({
        title: 'Invalid Username Format',
        details: [
          'Username can only contain letters, numbers, underscores (_), and hyphens (-)',
          'Special characters and spaces are not allowed'
        ],
        suggestion: 'Try a username like: john_doe, user-123, or myusername'
      });
      setLoading(false);
      return;
    }

    try {
      // Store username in case we need it for error messages
      await register(username, password, email || undefined, fullName || undefined);
      setShowSuccess(true);
      
      // Redirect to welcome page after showing success message
      setTimeout(() => {
        router.push('/welcome');
      }, 2000);
    } catch (err: any) {
      console.error('Registration error:', err);
      
      // Add username to error object for better error messages
      if (err.response) {
        err.username = username;
      }
      
      const errorDetails = parseErrorMessage(err);
      setErrorInfo(errorDetails);
      setLoading(false);
    }
  };

  if (showSuccess) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100 px-4">
        <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-2xl text-center">
          <div className="flex justify-center">
            <div className="rounded-full bg-green-100 p-3">
              <svg className="h-16 w-16 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Account Created!</h2>
            <p className="mt-4 text-lg text-gray-600">
              Your account has been successfully created.
            </p>
            <p className="mt-2 text-sm text-gray-500">
              Redirecting you to your dashboard...
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-pink-100 px-4 py-12">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-2xl shadow-2xl">
        <div>
          <h2 className="mt-2 text-center text-4xl font-extrabold text-gray-900">
            Create Account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Join us today and start managing your tasks
          </p>
        </div>

        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
          <div className="rounded-md shadow-sm space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                Username *
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-150"
                placeholder="Choose a username"
                minLength={4}
                maxLength={32}
              />
              <p className="mt-1 text-xs text-gray-500">4-32 characters, letters, numbers, _ and -</p>
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email (Optional)
              </label>
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-150"
                placeholder="your.email@example.com"
              />
            </div>

            <div>
              <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 mb-1">
                Full Name (Optional)
              </label>
              <input
                id="fullName"
                name="fullName"
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-150"
                placeholder="Your full name"
                maxLength={100}
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password *
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-150"
                placeholder="Create a strong password"
                minLength={8}
              />
              <p className="mt-1 text-xs text-gray-500">
                Min 8 chars, 1 uppercase, 1 lowercase, 1 digit
              </p>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                Confirm Password *
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="appearance-none relative block w-full px-4 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-150"
                placeholder="Confirm your password"
              />
            </div>
          </div>

          {errorInfo && (
            <div className="rounded-lg bg-red-50 p-5 border-2 border-red-200 shadow-sm">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-6 w-6 text-red-600" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3 flex-1">
                  <h3 className="text-base font-bold text-red-900 mb-2">
                    {errorInfo.title}
                  </h3>
                  <div className="space-y-1.5">
                    {errorInfo.details.map((detail, index) => (
                      <div key={index} className="flex items-start">
                        <span className="text-red-600 mr-2 mt-0.5">•</span>
                        <p className="text-sm text-red-800">{detail}</p>
                      </div>
                    ))}
                  </div>
                  {errorInfo.suggestion && (
                    <div className="mt-3 pt-3 border-t border-red-200">
                      <div className="flex items-start">
                        <svg className="h-5 w-5 text-red-500 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-sm font-medium text-red-700">
                          <span className="font-bold">Suggestion: </span>
                          {errorInfo.suggestion}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150"
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Creating account...
                </span>
              ) : (
                'Create Account'
              )}
            </button>
          </div>

          <div className="text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <Link href="/login" className="font-medium text-purple-600 hover:text-purple-500 transition duration-150">
                Sign in here
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}

