import React, { useState } from 'react';
import { Todo, TodoUpdate } from '../../types';
import { Task, TaskUpdate } from '../../services/api';
import { useRouter } from 'next/router';

// Define a unified interface for both todos and tasks
interface UnifiedItem extends Todo {
  type?: 'todo' | 'task';
  originalId: string | number;
}

interface MenuActionsPanelProps {
  todos: UnifiedItem[];
  onAddTodo: (todoData: any) => void;
  onToggleTodo: (id: string | number, completed: boolean) => void;
  onUpdateTodo: (id: string | number, updates: TodoUpdate | TaskUpdate) => void;
  onDeleteTodo: (id: string | number) => void;
  onSetViewMode?: (viewMode: boolean) => void;
  onSetShowAddForm?: (show: boolean) => void;
}

const MenuActionsPanel = ({
  todos,
  onAddTodo,
  onToggleTodo,
  onUpdateTodo,
  onDeleteTodo,
  onSetViewMode,
  onSetShowAddForm
}: MenuActionsPanelProps) => {
  const router = useRouter();
  const [showMenu, setShowMenu] = useState(false);
  const [selectedAction, setSelectedAction] = useState<string | null>(null);
  const [selectedTodoId, setSelectedTodoId] = useState<string | number | null>(null);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const [newTodoDueDate, setNewTodoDueDate] = useState('');

  const toggleMenu = () => {
    setShowMenu(!showMenu);
    // Reset selections when closing menu
    if (showMenu) {
      setSelectedAction(null);
      setSelectedTodoId(null);
      // Also reset view mode if it was set
      if (onSetViewMode) {
        onSetViewMode(false);
      }
    }
  };

  const handleActionSelect = (action: string) => {
    setSelectedAction(action);

    // If the action is 'add', we should show the add form
    if (action === 'add') {
      if (onSetViewMode) {
        onSetViewMode(false); // Make sure we're in add mode, not view mode
      }
      if (onSetShowAddForm) {
        onSetShowAddForm(true);
      }
      // We can close the menu since the form will be shown separately
      setShowMenu(false);
      return;
    }

    // For actions that require a specific task, select one
    if (['update', 'delete', 'complete', 'incomplete'].includes(action)) {
      if (todos.length > 0) {
        // For demo purposes, let user select a task
        // In a real implementation, you might show a dropdown to select a task
      } else {
        alert('No tasks available!');
        setSelectedAction(null);
        return;
      }
    }
  };

  const handleTaskSelection = (id: string | number) => {
    setSelectedTodoId(id);
  };

  const handleConfirmAction = () => {
    if (!selectedAction) return;

    switch (selectedAction) {
      case 'add':
        if (newTodoTitle.trim()) {
          // Call the onAddTodo function passed from the dashboard
          onAddTodo({
            title: newTodoTitle,
            description: newTodoDescription,
            due_date: newTodoDueDate || undefined
          });
          // Clear the form fields
          setNewTodoTitle('');
          setNewTodoDescription('');
          setNewTodoDueDate('');
          // Close the menu after adding
          setShowMenu(false);
          setSelectedAction(null);
        } else {
          alert('Please enter a title for the new task');
          return;
        }
        break;

      case 'update':
        if (selectedTodoId !== null) {
          // For update, we need to check if this is a task or todo
          onUpdateTodo(selectedTodoId, {
            title: newTodoTitle || undefined,
            description: newTodoDescription || undefined,
            due_date: newTodoDueDate || undefined
          });
          setSelectedTodoId(null);
        } else {
          alert('Please select a task to update');
          return;
        }
        break;

      case 'delete':
        if (selectedTodoId !== null) {
          onDeleteTodo(selectedTodoId);
          setSelectedTodoId(null);
        } else {
          alert('Please select a task to delete');
          return;
        }
        break;

      case 'complete':
        if (selectedTodoId !== null) {
          onToggleTodo(selectedTodoId, true);
          setSelectedTodoId(null);
        } else {
          alert('Please select a task to mark as complete');
          return;
        }
        break;

      case 'incomplete':
        if (selectedTodoId !== null) {
          onToggleTodo(selectedTodoId, false);
          setSelectedTodoId(null);
        } else {
          alert('Please select a task to mark as incomplete');
          return;
        }
        break;

      case 'view':
        // Set view mode to true to hide the add task form
        if (onSetViewMode) {
          onSetViewMode(true);
        }
        break;

      case 'exit':
        // Clear any stored authentication tokens
        localStorage.removeItem('access_token');
        // Redirect to signup page
        window.location.href = '/signup';
        return;
    }

    // Reset action after successful execution
    setSelectedAction(null);
  };

  const handleCancel = () => {
    setSelectedAction(null);
    setSelectedTodoId(null);
  };

  return (
    <div className="menu-actions-panel">
      <button onClick={toggleMenu} className="menu-toggle-btn">
        {showMenu ? 'Close Menu' : 'Open Actions Menu'}
      </button>

      {showMenu && (
        <div className="actions-menu">
          {!selectedAction ? (
            <div className="main-menu">
              <h3>Task Actions Menu</h3>
              <div className="menu-options">
                <button
                  onClick={() => handleActionSelect('add')}
                  className="menu-btn add-btn"
                >
                  Add Task
                </button>

                <button
                  onClick={() => handleActionSelect('update')}
                  className="menu-btn update-btn"
                >
                  Update Task
                </button>

                <button
                  onClick={() => handleActionSelect('delete')}
                  className="menu-btn delete-btn"
                >
                  Delete Task
                </button>

                <button
                  onClick={() => handleActionSelect('complete')}
                  className="menu-btn complete-btn"
                >
                  Mark as Complete
                </button>

                <button
                  onClick={() => handleActionSelect('incomplete')}
                  className="menu-btn incomplete-btn"
                >
                  Mark as Incomplete
                </button>

                <button
                  onClick={() => handleActionSelect('view')}
                  className="menu-btn view-btn"
                >
                  View Todo List
                </button>

                <button
                  onClick={() => handleActionSelect('exit')}
                  className="menu-btn exit-btn"
                >
                  Exit
                </button>
              </div>
            </div>
          ) : (
            <div className="action-form">
              <h3>{selectedAction.charAt(0).toUpperCase() + selectedAction.slice(1)} Task</h3>

              {(selectedAction === 'add' || selectedAction === 'update') && (
                <div className="form-fields">
                  <input
                    type="text"
                    placeholder="Task title"
                    value={newTodoTitle}
                    onChange={(e) => setNewTodoTitle(e.target.value)}
                    className="form-input title-input"
                  />

                  <textarea
                    placeholder="Task description"
                    value={newTodoDescription}
                    onChange={(e) => setNewTodoDescription(e.target.value)}
                    className="form-input description-input"
                  />

                  <input
                    type="date"
                    value={newTodoDueDate}
                    onChange={(e) => setNewTodoDueDate(e.target.value)}
                    className="form-input date-input"
                  />
                </div>
              )}

              {(selectedAction === 'update' || selectedAction === 'delete' ||
                selectedAction === 'complete' || selectedAction === 'incomplete') && (
                <div className="task-selection">
                  <label>Select a task:</label>
                  <select
                    value={selectedTodoId || ''}
                    onChange={(e) => {
                      // Check if the value is a number or string to determine the type
                      const value = e.target.value;
                      const parsedValue = Number(value);
                      handleTaskSelection(isNaN(parsedValue) ? value : parsedValue);
                    }}
                    className="task-select"
                  >
                    <option value="">Choose a task...</option>
                    {todos.map(todo => (
                      <option key={todo.originalId || todo.id} value={todo.originalId || todo.id}>
                        {todo.title}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              <div className="form-actions">
                <button
                  onClick={handleConfirmAction}
                  className="confirm-btn"
                >
                  Confirm
                </button>
                <button
                  onClick={handleCancel}
                  className="cancel-btn"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .menu-actions-panel {
          margin-bottom: 30px;
          padding: 25px;
          background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
          border-radius: 16px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
          border: 1px solid rgba(255, 255, 255, 0.2);
          backdrop-filter: blur(10px);
        }

        .menu-toggle-btn {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 14px 24px;
          border-radius: 12px;
          cursor: pointer;
          font-size: 1.1rem;
          font-weight: 600;
          transition: all 0.3s ease;
          box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
          width: 100%;
          letter-spacing: 0.5px;
        }

        .menu-toggle-btn:hover {
          transform: translateY(-3px);
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        .actions-menu {
          margin-top: 20px;
          padding: 25px;
          background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
          border-radius: 12px;
          box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
          border: 1px solid rgba(255, 255, 255, 0.3);
        }

        .main-menu h3 {
          margin-top: 0;
          margin-bottom: 20px;
          color: #2d3748;
          font-size: 1.4rem;
          font-weight: 700;
          text-align: center;
          background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .menu-options {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
          gap: 15px;
        }

        .menu-btn {
          padding: 16px;
          border: none;
          border-radius: 10px;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 600;
          transition: all 0.3s ease;
          text-align: left;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
          position: relative;
          overflow: hidden;
        }

        .menu-btn::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%);
          z-index: 1;
        }

        .menu-btn span {
          position: relative;
          z-index: 2;
        }

        .menu-btn:hover {
          transform: translateY(-4px);
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }

        .add-btn {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .add-btn:hover {
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        }

        .update-btn {
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
        }

        .update-btn:hover {
          background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
        }

        .delete-btn {
          background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
          color: #2d3748;
        }

        .delete-btn:hover {
          background: linear-gradient(135deg, #fecfef 0%, #ff9a9e 100%);
        }

        .complete-btn {
          background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
          color: white;
        }

        .complete-btn:hover {
          background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        }

        .incomplete-btn {
          background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
          color: white;
        }

        .incomplete-btn:hover {
          background: linear-gradient(135deg, #38f9d7 0%, #43e97b 100%);
        }

        .view-btn {
          background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
          color: white;
        }

        .view-btn:hover {
          background: linear-gradient(135deg, #fee140 0%, #fa709a 100%);
        }

        .exit-btn {
          background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
          color: #2d3748;
        }

        .exit-btn:hover {
          background: linear-gradient(135deg, #fed6e3 0%, #a8edea 100%);
        }

        .action-form h3 {
          margin-top: 0;
          margin-bottom: 20px;
          color: #2d3748;
          font-size: 1.4rem;
          font-weight: 700;
          text-align: center;
          background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .form-fields {
          margin-bottom: 20px;
        }

        .form-input {
          display: block;
          width: 100%;
          margin-bottom: 15px;
          padding: 12px 16px;
          border: 2px solid #e2e8f0;
          border-radius: 10px;
          font-size: 1rem;
          transition: all 0.3s ease;
          background: white;
        }

        .form-input:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }

        .form-input.title-input {
          font-size: 1.05rem;
          font-weight: 500;
        }

        .form-input.description-input {
          height: 100px;
          resize: vertical;
          font-family: inherit;
        }

        .task-selection {
          margin-bottom: 20px;
        }

        .task-selection label {
          display: block;
          margin-bottom: 10px;
          font-weight: 600;
          color: #4a5568;
          font-size: 1rem;
        }

        .task-select {
          width: 100%;
          padding: 12px 16px;
          border: 2px solid #e2e8f0;
          border-radius: 10px;
          font-size: 1rem;
          background: white;
          transition: all 0.3s ease;
        }

        .task-select:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }

        .form-actions {
          display: flex;
          gap: 15px;
          justify-content: center;
        }

        .confirm-btn, .cancel-btn {
          padding: 12px 24px;
          border: none;
          border-radius: 10px;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 600;
          transition: all 0.3s ease;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .confirm-btn {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .confirm-btn:hover {
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
          transform: translateY(-2px);
          box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
        }

        .cancel-btn {
          background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
          color: #2d3748;
        }

        .cancel-btn:hover {
          background: linear-gradient(135deg, #fecfef 0%, #ff9a9e 100%);
          transform: translateY(-2px);
          box-shadow: 0 6px 12px rgba(255, 154, 158, 0.3);
        }

        @media (max-width: 768px) {
          .menu-actions-panel {
            padding: 20px;
            margin-bottom: 25px;
          }

          .menu-options {
            grid-template-columns: 1fr;
          }

          .form-actions {
            flex-direction: column;
          }

          .confirm-btn, .cancel-btn {
            width: 100%;
          }

          .main-menu h3, .action-form h3 {
            font-size: 1.2rem;
          }
        }
      `}</style>
    </div>
  );
};

export default MenuActionsPanel;