import React, { useState, useEffect } from 'react';
import Layout from '../components/layout/Layout';
import TodoForm from '../components/todos/TodoForm';
import TodoList from '../components/todos/TodoList';
import MenuActionsPanel from '../components/todos/MenuActionsPanel';
import { Todo, TodoCreate, TodoUpdate } from '../types';
import { todoAPI } from '../services/api';
import { useRouter } from 'next/router';

const DashboardPage = () => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<boolean>(false);
  const [showAddForm, setShowAddForm] = useState<boolean>(false);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated before accessing dashboard
    if (!localStorage.getItem('access_token')) {
      alert('Signin First then you\'ll able to see the Dashboard');
      router.push('/signin');
      return;
    }

    const fetchTodos = async () => {
      try {
        const response = await todoAPI.getAll();
        setTodos(response.data);
      } catch (error) {
        console.error('Error fetching todos:', error);
        // Redirect to sign in if unauthorized
        if ((error as any).response?.status === 401) {
          alert('Signin First then you\'ll able to see the Dashboard');
          router.push('/signin');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTodos();
  }, [router]);

  const handleAddTodo = async (todoData: TodoCreate) => {
    try {
      const response = await todoAPI.create(todoData);
      setTodos([...todos, response.data]);
      setViewMode(false); // Reset view mode to show the form again
      setShowAddForm(false); // Hide the form after adding
      setSuccessMessage('Task Added Successfully in Todo List');
      // Clear the message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      console.error('Error creating todo:', error);
    }
  };

  const handleToggleTodo = async (id: number, completed: boolean) => {
    try {
      const response = await todoAPI.toggleComplete(id, completed);
      setTodos(todos.map(todo =>
        todo.id === id ? { ...todo, completed: response.data.completed } : todo
      ));
      const message = completed
        ? 'Task Marked as Complete Successfully'
        : 'Task Marked as Incomplete Successfully';
      setSuccessMessage(message);
      // Clear the message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      console.error('Error toggling todo:', error);
    }
  };

  const handleUpdateTodo = async (id: number, updates: TodoUpdate) => {
    try {
      const response = await todoAPI.update(id, updates);
      setTodos(todos.map(todo =>
        todo.id === id ? response.data : todo
      ));
      setViewMode(false); // Reset view mode to show the form again
      setShowAddForm(false); // Hide the form if it was shown
      setSuccessMessage('Task Updated Successfully in Todo List');
      // Clear the message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await todoAPI.delete(id);
      setTodos(todos.filter(todo => todo.id !== id));
      setViewMode(false); // Reset view mode to show the form again
      setShowAddForm(false); // Hide the form if it was shown
      setSuccessMessage('Task Deleted Successfully from Todo List');
      // Clear the message after 3 seconds
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="container">
          <p>Loading...</p>
        </div>
      </Layout>
    );
  }

  // Double check authentication before rendering content
  if (!localStorage.getItem('access_token')) {
    // Show message and redirect
    if (typeof window !== 'undefined') {
      alert('Signin First then you\'ll able to see the Dashboard');
      window.location.href = '/signin';
    }

    return (
      <Layout>
        <div className="container">
          <p>Redirecting to sign in...</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="dashboard-container">
        <div className="page-header">
          <h1 className="evolution-text">Evolution of Todo</h1>
          <h2>Task Manager</h2>
          <p className="page-subtitle">Organize your tasks and boost your productivity</p>
        </div>

        <MenuActionsPanel
          todos={todos}
          onAddTodo={handleAddTodo}
          onToggleTodo={handleToggleTodo}
          onUpdateTodo={handleUpdateTodo}
          onDeleteTodo={handleDeleteTodo}
          onSetViewMode={setViewMode}
          onSetShowAddForm={setShowAddForm}
        />

        {/* Success message display */}
        {successMessage && (
          <div className="success-message">
            {successMessage}
          </div>
        )}

        {/* Conditionally render TodoForm based on showAddForm state */}
        {showAddForm && <TodoForm onSubmit={handleAddTodo} />}

        <TodoList
          todos={todos}
          onToggle={handleToggleTodo}
          onUpdate={handleUpdateTodo}
          onDelete={handleDeleteTodo}
          emptyState={<div className="empty-state">No tasks yet. Add one to get started!</div>}
        />
      </div>

      <style jsx global>{`
        .dashboard-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }

        .page-header {
          margin-bottom: 24px;
          padding-bottom: 16px;
          border-bottom: 1px solid #e1e5e9;
        }

        .page-header h1 {
          margin: 0 0 8px 0;
          font-size: 2rem;
          font-weight: 700;
          color: #111;
        }

        .page-header h2 {
          margin: 0 0 8px 0;
          font-size: 2rem;
          font-weight: 700;
          color: #111;
        }

        .page-subtitle {
          margin: 0;
          color: #666;
          font-size: 1.1rem;
        }

        .evolution-text {
          margin: 0 0 8px 0;
          font-size: 1.8rem;
          color: #0070f3;
          text-decoration: underline;
          text-decoration-color: #000;
          text-align: center;
        }

        .success-message {
          margin: 16px 0;
          padding: 12px 16px;
          background-color: #d4edda;
          color: #155724;
          border: 1px solid #c3e6cb;
          border-radius: 8px;
          font-weight: 500;
          text-align: center;
          animation: fadeInSlideDown 0.3s ease-out;
        }

        @keyframes fadeInSlideDown {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @media (max-width: 768px) {
          .dashboard-container {
            padding: 16px;
          }

          .page-header h1 {
            font-size: 1.75rem;
          }
        }
      `}</style>
    </Layout>
  );
};

export default DashboardPage;