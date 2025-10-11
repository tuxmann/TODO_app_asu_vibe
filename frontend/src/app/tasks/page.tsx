'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { todoAPI, TodoResponse } from '@/lib/api';
import Link from 'next/link';

export default function TasksPage() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();
  
  const [tasks, setTasks] = useState<TodoResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    if (user) {
      loadTasks();
    }
  }, [user, filter]);

  const loadTasks = async () => {
    if (!user) return;
    
    setLoading(true);
    setError('');
    
    try {
      const completed = filter === 'all' ? undefined : filter === 'completed';
      const data = await todoAPI.getByUsername(user.username, { completed });
      setTasks(data);
    } catch (err: any) {
      console.error('Failed to load tasks:', err);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleTaskCompletion = async (taskId: string, currentStatus: boolean) => {
    try {
      if (currentStatus) {
        await todoAPI.markIncomplete(taskId);
      } else {
        await todoAPI.markComplete(taskId);
      }
      // Reload tasks
      await loadTasks();
    } catch (err: any) {
      console.error('Failed to toggle task:', err);
      alert('Failed to update task');
    }
  };

  const deleteTask = async (taskId: string) => {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
      await todoAPI.delete(taskId);
      await loadTasks();
    } catch (err: any) {
      console.error('Failed to delete task:', err);
      alert('Failed to delete task');
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800 border-red-200';
      case 'medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (authLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
      </div>
    );
  }

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
              <span className="text-gray-600 font-medium">My Tasks</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/welcome"
                className="text-gray-700 hover:text-indigo-600 font-medium transition"
              >
                Dashboard
              </Link>
              <Link
                href="/tasks/new"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 transition"
              >
                <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                New Task
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">My Tasks</h1>
          <p className="mt-2 text-gray-600">Manage and organize your tasks</p>
        </div>

        {/* Filters */}
        <div className="mb-6 flex space-x-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            All Tasks
          </button>
          <button
            onClick={() => setFilter('active')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === 'active'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            Active
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-4 py-2 rounded-lg font-medium transition ${
              filter === 'completed'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50'
            }`}
          >
            Completed
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 rounded-lg bg-red-50 p-4 border border-red-200">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
            <span className="ml-3 text-gray-600">Loading tasks...</span>
          </div>
        )}

        {/* Tasks List */}
        {!loading && tasks.length === 0 && (
          <div className="bg-white rounded-xl shadow-lg p-12 text-center">
            <div className="flex justify-center mb-4">
              <svg className="h-16 w-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No tasks found</h3>
            <p className="text-gray-600 mb-6">
              {filter === 'all' 
                ? "Get started by creating your first task!"
                : `No ${filter} tasks yet.`}
            </p>
            <Link
              href="/tasks/new"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 transition"
            >
              <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Your First Task
            </Link>
          </div>
        )}

        {!loading && tasks.length > 0 && (
          <div className="space-y-4">
            {tasks.map((task) => (
              <div
                key={task.id}
                className={`bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition ${
                  task.completed ? 'opacity-75' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    {/* Checkbox */}
                    <button
                      onClick={() => toggleTaskCompletion(task.id, task.completed)}
                      className="mt-1 flex-shrink-0"
                    >
                      {task.completed ? (
                        <svg className="h-6 w-6 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-6 w-6 text-gray-400 hover:text-indigo-600 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <circle cx="12" cy="12" r="10" strokeWidth="2" />
                        </svg>
                      )}
                    </button>

                    {/* Task Details */}
                    <div className="flex-1 min-w-0">
                      <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                        {task.title}
                      </h3>
                      {task.description && (
                        <p className="mt-1 text-sm text-gray-600">{task.description}</p>
                      )}
                      
                      {/* Meta Information */}
                      <div className="mt-3 flex flex-wrap items-center gap-3">
                        {/* Priority Badge */}
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${getPriorityColor(task.priority)}`}>
                          {task.priority.toUpperCase()}
                        </span>

                        {/* Deadline */}
                        <span className="inline-flex items-center text-sm text-gray-600">
                          <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          {formatDate(task.deadline)}
                        </span>

                        {/* Labels */}
                        {task.labels.map((label) => (
                          <span
                            key={label}
                            className="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-indigo-100 text-indigo-800"
                          >
                            {label}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="ml-4 flex items-center space-x-2 flex-shrink-0">
                    <Link
                      href={`/tasks/edit/${task.id}`}
                      className="text-indigo-600 hover:text-indigo-800 transition"
                      title="Edit task"
                    >
                      <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </Link>
                    <button
                      onClick={() => deleteTask(task.id)}
                      className="text-red-600 hover:text-red-800 transition"
                      title="Delete task"
                    >
                      <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

