'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function WelcomePage() {
  const { user, loading, logout, isAuthenticated } = useAuth();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !loading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, loading, router, mounted]);

  const handleLogout = async () => {
    await logout();
  };

  if (loading || !mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-indigo-600">TODO App</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700 font-medium">{user.username}</span>
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition duration-150"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Welcome Hero Section */}
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden mb-8">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-8 py-12">
            <div className="flex items-center space-x-4">
              <div className="bg-white rounded-full p-4">
                <svg className="h-12 w-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <h1 className="text-4xl font-bold text-white">
                  Welcome back, {user.full_name || user.username}!
                </h1>
                <p className="text-indigo-100 mt-2 text-lg">
                  Ready to tackle your tasks today?
                </p>
              </div>
            </div>
          </div>

          {/* User Info Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-8">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-500 rounded-lg p-3">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p className="text-sm text-gray-600 font-medium">Username</p>
                  <p className="text-lg font-bold text-gray-900">{user.username}</p>
                </div>
              </div>
            </div>

            {user.email && (
              <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border border-green-200">
                <div className="flex items-center space-x-3">
                  <div className="bg-green-500 rounded-lg p-3">
                    <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600 font-medium">Email</p>
                    <p className="text-lg font-bold text-gray-900">{user.email}</p>
                  </div>
                </div>
              </div>
            )}

            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border border-purple-200">
              <div className="flex items-center space-x-3">
                <div className="bg-purple-500 rounded-lg p-3">
                  <svg className="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className="text-sm text-gray-600 font-medium">Member Since</p>
                  <p className="text-sm font-bold text-gray-900">{new Date(user.created_at).toLocaleDateString()}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Account Details Section */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="px-8 py-6 bg-gray-50 border-b border-gray-200">
            <h2 className="text-2xl font-bold text-gray-900">Account Details</h2>
          </div>
          <div className="px-8 py-6">
            <dl className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div className="border-l-4 border-indigo-500 pl-4">
                <dt className="text-sm font-medium text-gray-500">Account ID</dt>
                <dd className="mt-1 text-sm text-gray-900 font-mono">{user.id}</dd>
              </div>
              
              <div className="border-l-4 border-indigo-500 pl-4">
                <dt className="text-sm font-medium text-gray-500">Account Status</dt>
                <dd className="mt-1">
                  <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user.is_active ? '✓ Active' : '✗ Inactive'}
                  </span>
                </dd>
              </div>
              
              <div className="border-l-4 border-indigo-500 pl-4">
                <dt className="text-sm font-medium text-gray-500">Account Created</dt>
                <dd className="mt-1 text-sm text-gray-900">{formatDate(user.created_at)}</dd>
              </div>
              
              <div className="border-l-4 border-indigo-500 pl-4">
                <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                <dd className="mt-1 text-sm text-gray-900">{formatDate(user.updated_at)}</dd>
              </div>

              {user.is_superuser && (
                <div className="border-l-4 border-indigo-500 pl-4 sm:col-span-2">
                  <dt className="text-sm font-medium text-gray-500">Role</dt>
                  <dd className="mt-1">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                      ⭐ Super User
                    </span>
                  </dd>
                </div>
              )}
            </dl>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <Link href="/tasks" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition duration-200 cursor-pointer border-2 border-transparent hover:border-indigo-500">
            <div className="flex items-center space-x-4">
              <div className="bg-indigo-100 rounded-lg p-3">
                <svg className="h-8 w-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">My Tasks</h3>
                <p className="text-sm text-gray-500">View and manage tasks</p>
              </div>
            </div>
          </Link>

          <Link href="/tasks/new" className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition duration-200 cursor-pointer border-2 border-transparent hover:border-green-500">
            <div className="flex items-center space-x-4">
              <div className="bg-green-100 rounded-lg p-3">
                <svg className="h-8 w-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">New Task</h3>
                <p className="text-sm text-gray-500">Create a new task</p>
              </div>
            </div>
          </Link>

          <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition duration-200 cursor-pointer border-2 border-transparent hover:border-purple-500 opacity-60">
            <div className="flex items-center space-x-4">
              <div className="bg-purple-100 rounded-lg p-3">
                <svg className="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Settings</h3>
                <p className="text-sm text-gray-500">Coming soon</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

