'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter, useParams } from 'next/navigation';
import { todoAPI, TodoResponse } from '@/lib/api';
import Link from 'next/link';

export default function EditTaskPage() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;
  
  const [task, setTask] = useState<TodoResponse | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<'high' | 'medium' | 'low'>('medium');
  const [deadline, setDeadline] = useState('');
  const [selectedLabels, setSelectedLabels] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [showSuccess, setShowSuccess] = useState(false);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated || !user) {
      router.push('/login');
    }
  }, [isAuthenticated, user, router]);

  // Load task data
  useEffect(() => {
    if (taskId && user) {
      loadTask();
    }
  }, [taskId, user]);

  const loadTask = async () => {
    try {
      const data = await todoAPI.getById(taskId);
      setTask(data);
      
      // Populate form fields
      setTitle(data.title);
      setDescription(data.description || '');
      setPriority(data.priority as 'high' | 'medium' | 'low');
      setDeadline(data.deadline);
      setSelectedLabels(data.labels);
      
      setLoading(false);
    } catch (err: any) {
      console.error('Failed to load task:', err);
      setError('Failed to load task. It may not exist or you may not have permission to edit it.');
      setLoading(false);
    }
  };

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
    setSaving(true);

    // Validation
    if (!title.trim()) {
      setError('Task title is required');
      setSaving(false);
      return;
    }

    if (!deadline) {
      setError('Deadline is required');
      setSaving(false);
      return;
    }

    // Check if deadline is in the past
    const deadlineDate = new Date(deadline);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (deadlineDate < today) {
      setError('Deadline must be today or later');
      setSaving(false);
      return;
    }

    try {
      await todoAPI.update(taskId, {
        title: title.trim(),
        description: description.trim() || undefined,
        priority,
        deadline,
        labels: selectedLabels,
      });

      setShowSuccess(true);
      
      // Redirect after short delay
      setTimeout(() => {
        router.push('/tasks');
      }, 1500);
    } catch (err: any) {
      console.error('Failed to update task:', err);
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Failed to update task. Please try again.'
      );
      setSaving(false);
    }
  };

  if (!isAuthenticated || !user) {
    return null;
  }

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
            <h2 className="text-3xl font-bold text-gray-900">Task Updated!</h2>
            <p className="mt-4 text-lg text-gray-600">
              Your changes have been saved successfully.
            </p>
            <p className="mt-2 text-sm text-gray-500">
              Redirecting to your tasks...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        <div className="flex items-center space-x-3">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
          <span className="text-gray-600 font-medium">Loading task...</span>
        </div>
      </div>
    );
  }

  if (error && !task) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 px-4">
        <div className="max-w-md w-full bg-white p-8 rounded-2xl shadow-2xl text-center">
          <div className="flex justify-center mb-4">
            <div className="rounded-full bg-red-100 p-3">
              <svg className="h-16 w-16 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <Link
            href="/tasks"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 transition"
          >
            Back to Tasks
          </Link>
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
              <span className="text-gray-600 font-medium">Edit Task</span>
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-white">Edit Task</h1>
                <p className="text-indigo-100 mt-1">Update your task details</p>
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
                href="/tasks"
                className="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={saving}
                className="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {saving ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Saving Changes...
                  </span>
                ) : (
                  <span className="flex items-center">
                    <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                    </svg>
                    Save Changes
                  </span>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Task Info */}
        {task && (
          <div className="mt-6 text-center text-sm text-gray-600">
            <p>Created: {new Date(task.created_at).toLocaleString()}</p>
            {task.updated_at !== task.created_at && (
              <p>Last updated: {new Date(task.updated_at).toLocaleString()}</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

