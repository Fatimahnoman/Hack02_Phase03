import React, { useState } from 'react';
import { Todo, TodoUpdate } from '../../types';
import { useRouter } from 'next/router';

interface MenuActionsPanelProps {
  todos: Todo[];
  onAddTodo: (todoData: any) => void;
  onToggleTodo: (id: number, completed: boolean) => void;
  onUpdateTodo: (id: number, updates: TodoUpdate) => void;
  onDeleteTodo: (id: number) => void;
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
  const [selectedTodoId, setSelectedTodoId] = useState<number | null>(null);
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

  const handleTaskSelection = (id: number) => {
    setSelectedTodoId(id);
  };

  const handleConfirmAction = () => {
    if (!selectedAction) return;

    switch (selectedAction) {
      case 'add':
        if (newTodoTitle.trim()) {
          onAddTodo({
            title: newTodoTitle,
            description: newTodoDescription,
            due_date: newTodoDueDate || undefined
          });
          setNewTodoTitle('');
          setNewTodoDescription('');
          setNewTodoDueDate('');
          // Show success message (the main success message is handled in dashboard)
          // Also close the menu after adding
          setShowMenu(false);
          setSelectedAction(null);
        } else {
          alert('Please enter a title for the new task');
          return;
        }
        break;

      case 'update':
        if (selectedTodoId !== null) {
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
                    onChange={(e) => handleTaskSelection(Number(e.target.value))}
                    className="task-select"
                  >
                    <option value="">Choose a task...</option>
                    {todos.map(todo => (
                      <option key={todo.id} value={todo.id}>
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
          margin-bottom: 24px;
          padding: 20px;
          border: 1px solid #e1e5e9;
          border-radius: 12px;
          background-color: white;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .menu-toggle-btn {
          background-color: #0070f3;
          color: white;
          border: none;
          padding: 12px 16px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 500;
          transition: all 0.2s ease;
        }

        .menu-toggle-btn:hover {
          background-color: #0060e0;
          transform: translateY(-1px);
        }

        .actions-menu {
          margin-top: 16px;
          padding: 20px;
          background-color: #f8fafc;
          border: 1px solid #e1e5e9;
          border-radius: 8px;
        }

        .main-menu h3 {
          margin-top: 0;
          margin-bottom: 16px;
          color: #111;
          font-size: 1.25rem;
          font-weight: 600;
        }

        .menu-options {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 12px;
        }

        .menu-btn {
          padding: 14px;
          border: 1px solid #d1d5da;
          border-radius: 8px;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 500;
          transition: all 0.2s ease;
          text-align: left;
        }

        .menu-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .add-btn {
          background-color: #f0f7ff;
          color: #0066cc;
          border-color: #c6e0ff;
        }

        .add-btn:hover {
          background-color: #e6f2ff;
        }

        .update-btn {
          background-color: #fff7e6;
          color: #d97706;
          border-color: #ffd88a;
        }

        .update-btn:hover {
          background-color: #fff4d1;
        }

        .delete-btn {
          background-color: #ffebee;
          color: #c5221f;
          border-color: #f8b4b0;
        }

        .delete-btn:hover {
          background-color: #fdd8d6;
        }

        .complete-btn {
          background-color: #e6f4ea;
          color: #137333;
          border-color: #b7e3c4;
        }

        .complete-btn:hover {
          background-color: #d2efda;
        }

        .incomplete-btn {
          background-color: #fff3e0;
          color: #e67700;
          border-color: #ffd8a8;
        }

        .incomplete-btn:hover {
          background-color: #ffe9c2;
        }

        .view-btn {
          background-color: #f3e5f5;
          color: #7b1fa2;
          border-color: #e1b3e8;
        }

        .view-btn:hover {
          background-color: #edccec;
        }

        .exit-btn {
          background-color: #f1f3f5;
          color: #495057;
          border-color: #d1d5da;
        }

        .exit-btn:hover {
          background-color: #e9ecef;
        }

        .action-form h3 {
          margin-top: 0;
          margin-bottom: 16px;
          color: #111;
          font-size: 1.25rem;
          font-weight: 600;
        }

        .form-fields {
          margin-bottom: 16px;
        }

        .form-input {
          display: block;
          width: 100%;
          margin-bottom: 12px;
          padding: 10px 12px;
          border: 1px solid #d1d5da;
          border-radius: 6px;
          font-size: 0.95rem;
          transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .form-input:focus {
          outline: none;
          border-color: #0070f3;
          box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1);
        }

        .form-input.title-input {
          font-size: 1rem;
          font-weight: 500;
        }

        .form-input.description-input {
          height: 80px;
          resize: vertical;
        }

        .task-selection {
          margin-bottom: 16px;
        }

        .task-selection label {
          display: block;
          margin-bottom: 8px;
          font-weight: 500;
          color: #333;
          font-size: 0.95rem;
        }

        .task-select {
          width: 100%;
          padding: 10px 12px;
          border: 1px solid #d1d5da;
          border-radius: 6px;
          font-size: 0.95rem;
          background-color: white;
          transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .task-select:focus {
          outline: none;
          border-color: #0070f3;
          box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1);
        }

        .form-actions {
          display: flex;
          gap: 12px;
          justify-content: flex-start;
        }

        .confirm-btn, .cancel-btn {
          padding: 10px 16px;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.95rem;
          font-weight: 500;
          transition: all 0.2s ease;
        }

        .confirm-btn {
          background-color: #0070f3;
          color: white;
        }

        .confirm-btn:hover {
          background-color: #0060e0;
        }

        .cancel-btn {
          background-color: #fa5252;
          color: white;
        }

        .cancel-btn:hover {
          background-color: #f03e3e;
        }

        @media (max-width: 768px) {
          .menu-options {
            grid-template-columns: 1fr;
          }

          .form-actions {
            flex-direction: column;
          }

          .confirm-btn, .cancel-btn {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default MenuActionsPanel;