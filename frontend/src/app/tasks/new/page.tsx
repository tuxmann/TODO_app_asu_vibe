'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { todoAPI } from '@/lib/api';
import Link from 'next/link';

export default function NewTaskPage() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();
  
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'high' | 'medium' | 'low'>('medium');
  const [deadline, setDeadline] = useState('');
  const [selectedLabels, setSelectedLabels] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  // Redirect if not authenticated
  if (!isAuthenticated || !user) {
    router.push('/login');
    return null;
  }

  const availableLabels = ['Work', 'Personal', 'Urgent'];

  const toggleLabel = (label: string) => {
    setSelectedLabels(prev => 
      prev.includes(label)
        ? prev.filter(l => l !== label)
        : [...prev, label]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (!title.trim()) {
      setError('Task title is required');
      setLoading(false);
      return;
    }

    if (!deadline) {
      setError('Deadline is required');
      setLoading(false);
      return;
    }

    // Check if deadline is in the past
    const deadlineDate = new Date(deadline);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (deadlineDate < today) {
      setError('Deadline must be today or later');
      setLoading(false);
      return;
    }

    try {
      await todoAPI.create({
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        deadline,
        labels: selectedLabels,
        username: user.username,
        completed: false,
      });

      setShowSuccess(true);
      
      // Redirect after short delay
      setTimeout(() => {
        router.push('/tasks');
      }, 1500);
    } catch (err: any) {
      console.error('Failed to create task:', err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to create task. Please try again.'
      );
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
            <h2 className="text-3xl font-bold text-gray-900">Task Created!</h2>
            <p className="mt-4 text-lg text-gray-600">
              Your task has been successfully added.
            </p>
            <p className="mt-2 text-sm text-gray-500">
              Redirecting to your tasks...
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Get today's date in YYYY-MM-DD format for min date
  const today = new Date().toISOString().split('T')[0];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Navigation Bar */}
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <Link href="/welcome" className="text-2xl font-bold text-indigo-600 hover:text-indigo-700 transition">
                TODO App
              </Link>
              <span className="text-gray-400">|</span>
              <span className="text-gray-600 font-medium">New Task</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/welcome"
                className="text-gray-700 hover:text-indigo-600 font-medium transition"
              >
                Dashboard
              </Link>
              <Link
                href="/tasks"
                className="text-gray-700 hover:text-indigo-600 font-medium transition"
              >
                My Tasks
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-8 py-6">
            <div className="flex items-center space-x-3">
              <div className="bg-white rounded-lg p-2">
                <svg className="h-8 w-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">Create New Task</h1>
                <p className="text-indigo-100 mt-1">Add a new task to your list</p>
              </div>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-8 space-y-6">
            {/* Title */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Task Title *
              </label>
              <input
                type="text"
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-gray-900"
                placeholder="e.g., Complete project documentation"
                maxLength={100}
                required
              />
              <p className="mt-1 text-xs text-gray-500">{title.length}/100 characters</p>
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description (Optional)
              </label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                rows={4}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-gray-900"
                placeholder="Add more details about this task..."
                maxLength={500}
              />
              <p className="mt-1 text-xs text-gray-500">{description.length}/500 characters</p>
            </div>

            {/* Priority and Deadline Row */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Priority */}
              <div>
                <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-2">
                  Priority *
                </label>
                <div className="grid grid-cols-3 gap-2">
                  <button
                    type="button"
                    onClick={() => setPriority('low')}
                    className={`py-3 px-4 rounded-lg font-medium transition ${
                      priority === 'low'
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Low
                  </button>
                  <button
                    type="button"
                    onClick={() => setPriority('medium')}
                    className={`py-3 px-4 rounded-lg font-medium transition ${
                      priority === 'medium'
                        ? 'bg-yellow-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Medium
                  </button>
                  <button
                    type="button"
                    onClick={() => setPriority('high')}
                    className={`py-3 px-4 rounded-lg font-medium transition ${
                      priority === 'high'
                        ? 'bg-red-500 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    High
                  </button>
                </div>
              </div>

              {/* Deadline */}
              <div>
                <label htmlFor="deadline" className="block text-sm font-medium text-gray-700 mb-2">
                  Deadline *
                </label>
                <input
                  type="date"
                  id="deadline"
                  value={deadline}
                  onChange={(e) => setDeadline(e.target.value)}
                  min={today}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-gray-900"
                  required
                />
              </div>
            </div>

            {/* Labels */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Labels (Optional)
              </label>
              <div className="flex flex-wrap gap-2">
                {availableLabels.map((label) => (
                  <button
                    key={label}
                    type="button"
                    onClick={() => toggleLabel(label)}
                    className={`px-4 py-2 rounded-full font-medium transition ${
                      selectedLabels.includes(label)
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {selectedLabels.includes(label) && '✓ '}
                    {label}
                  </button>
                ))}
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="rounded-lg bg-red-50 p-4 border border-red-200">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm font-medium text-red-800">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200">
              <Link
                href="/welcome"
                className="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {loading ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Creating Task...
                  </span>
                ) : (
                  <span className="flex items-center">
                    <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    Create Task
                  </span>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Help Text */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>All tasks are private and only visible to you</p>
        </div>
      </div>
    </div>
  );
}

