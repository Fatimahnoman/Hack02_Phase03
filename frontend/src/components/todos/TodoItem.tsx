import React from 'react';
import { Todo, TodoUpdate } from '../../types';
import { todoAPI } from '../../services/api';

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: number, completed: boolean) => void;
  onUpdate: (id: number, updates: TodoUpdate) => void;
  onDelete: (id: number) => void;
}

const TodoItem = ({ todo, onToggle, onUpdate, onDelete }: TodoItemProps) => {
  const [isEditing, setIsEditing] = React.useState(false);
  const [editTitle, setEditTitle] = React.useState(todo.title);
  const [editDescription, setEditDescription] = React.useState(todo.description || '');
  const [editDueDate, setEditDueDate] = React.useState(todo.due_date || '');
  const [editCompleted, setEditCompleted] = React.useState(todo.completed);

  const handleToggle = () => {
    onToggle(todo.id, !todo.completed);
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditDueDate(todo.due_date || '');
    setEditCompleted(todo.completed);
  };

  const handleSave = () => {
    onUpdate(todo.id, {
      title: editTitle,
      description: editDescription,
      due_date: editDueDate || undefined,
      completed: editCompleted
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditDueDate(todo.due_date || '');
    setEditCompleted(todo.completed);
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        {isEditing ? (
          <div className="edit-form">
            <div className="edit-header">
              <div
                className={`edit-checkbox ${editCompleted ? 'completed' : 'incomplete'}`}
                onClick={() => setEditCompleted(!editCompleted)}
              >
                {editCompleted ? '✓' : '✕'}
              </div>
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="edit-title"
                placeholder="Task title"
              />
            </div>
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="edit-description"
              placeholder="Task description"
            />
            <input
              type="date"
              value={editDueDate}
              onChange={(e) => setEditDueDate(e.target.value)}
              className="edit-date"
            />
            <div className="edit-buttons">
              <button onClick={handleSave} className="save-btn btn-primary">Save</button>
              <button onClick={handleCancel} className="cancel-btn btn-secondary">Cancel</button>
            </div>
          </div>
        ) : (
          <>
            <div className="todo-header">
              <div
                className={`todo-checkbox ${todo.completed ? 'completed' : 'incomplete'}`}
                onClick={handleToggle}
              >
                {todo.completed ? '✓' : '✕'}
              </div>
              <div className="todo-text">
                <h3 className={`todo-title ${todo.completed ? 'completed' : ''}`}>{todo.title}</h3>
                {todo.description && (
                  <p className={`todo-description ${todo.completed ? 'completed' : ''}`}>{todo.description}</p>
                )}
                {todo.due_date && (
                  <div className="todo-meta">
                    <span className={`todo-due-date ${todo.completed ? 'completed' : ''}`}>
                      📅 {new Date(todo.due_date).toLocaleDateString()}
                    </span>
                    {todo.completed && (
                      <span className="todo-completed-badge">✓ Completed</span>
                    )}
                  </div>
                )}
              </div>
            </div>
            <div className="todo-actions">
              <button onClick={handleEdit} className="edit-btn btn-secondary" title="Edit task">
                ✏️
              </button>
              <button onClick={handleDelete} className="delete-btn btn-danger" title="Delete task">
                🗑️
              </button>
            </div>
          </>
        )}
      </div>
      <style jsx>{`
        .todo-item {
          background: white;
          border: 1px solid #e1e5e9;
          border-radius: 12px;
          padding: 16px;
          margin-bottom: 12px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          transition: box-shadow 0.2s ease, transform 0.2s ease;
        }

        .todo-item:hover {
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
          transform: translateY(-2px);
        }

        .todo-item.completed {
          opacity: 0.85;
          background-color: #f8f9fa;
        }

        .todo-content {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          gap: 12px;
        }

        .todo-header {
          display: flex;
          align-items: flex-start;
          flex: 1;
          min-width: 0;
        }

        .todo-checkbox {
          width: 24px;
          height: 24px;
          cursor: pointer;
          border: 2px solid #d1d5da;
          border-radius: 4px;
          background-color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: bold;
          transition: all 0.2s ease;
          flex-shrink: 0;
          margin-right: 12px;
          margin-top: 4px;
        }

        .todo-checkbox.completed {
          background-color: #0070f3;
          border-color: #0070f3;
          color: white;
        }

        .todo-checkbox.incomplete {
          background-color: white;
          border-color: #d1d5da;
          color: #fa5252;
        }

        .todo-checkbox:hover {
          transform: scale(1.05);
        }

        .todo-checkbox.completed:hover {
          background-color: #0060e0;
          border-color: #0060e0;
        }

        .todo-checkbox.incomplete:hover {
          background-color: #fff5f5;
          border-color: #fa5252;
        }

        .todo-text {
          flex: 1;
          min-width: 0;
        }

        .todo-title {
          margin: 0 0 8px 0;
          font-size: 1.1rem;
          font-weight: 600;
          color: #111;
          line-height: 1.4;
        }

        .todo-title.completed {
          text-decoration: line-through;
          color: #666;
        }

        .todo-description {
          margin: 0 0 8px 0;
          color: #555;
          font-size: 0.95rem;
          line-height: 1.5;
        }

        .todo-description.completed {
          text-decoration: line-through;
          color: #888;
        }

        .todo-meta {
          display: flex;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
        }

        .todo-due-date {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 4px 8px;
          background-color: #f0f7ff;
          color: #0066cc;
          border-radius: 6px;
          font-size: 0.85rem;
          font-weight: 500;
        }

        .todo-due-date.completed {
          background-color: #e6f4ea;
          color: #137333;
        }

        .todo-completed-badge {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 4px 8px;
          background-color: #e6f4ea;
          color: #137333;
          border-radius: 6px;
          font-size: 0.85rem;
          font-weight: 500;
        }

        .todo-actions {
          display: flex;
          gap: 8px;
          margin-left: 12px;
          flex-shrink: 0;
        }

        .btn-primary, .btn-secondary, .btn-danger {
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 0.9rem;
          padding: 8px 12px;
          transition: all 0.2s ease;
          display: inline-flex;
          align-items: center;
          justify-content: center;
        }

        .btn-primary {
          background-color: #0070f3;
          color: white;
        }

        .btn-primary:hover {
          background-color: #0060e0;
        }

        .btn-secondary {
          background-color: #f1f3f5;
          color: #495057;
        }

        .btn-secondary:hover {
          background-color: #e9ecef;
        }

        .btn-danger {
          background-color: #fa5252;
          color: white;
        }

        .btn-danger:hover {
          background-color: #f03e3e;
        }

        .edit-form {
          flex: 1;
          width: 100%;
        }

        .edit-header {
          display: flex;
          align-items: flex-start;
          gap: 12px;
          margin-bottom: 12px;
        }

        .edit-checkbox {
          width: 24px;
          height: 24px;
          cursor: pointer;
          border: 2px solid #d1d5da;
          border-radius: 4px;
          background-color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: bold;
          transition: all 0.2s ease;
          flex-shrink: 0;
          margin-right: 12px;
          margin-top: 4px;
        }

        .edit-checkbox.completed {
          background-color: #0070f3;
          border-color: #0070f3;
          color: white;
        }

        .edit-checkbox.incomplete {
          background-color: white;
          border-color: #d1d5da;
          color: #fa5252;
        }

        .edit-checkbox:hover {
          transform: scale(1.05);
        }

        .edit-checkbox.completed:hover {
          background-color: #0060e0;
          border-color: #0060e0;
        }

        .edit-checkbox.incomplete:hover {
          background-color: #fff5f5;
          border-color: #fa5252;
        }

        .edit-title {
          flex: 1;
          padding: 10px 12px;
          border: 1px solid #d1d5da;
          border-radius: 6px;
          font-size: 1rem;
          font-weight: 500;
          transition: border-color 0.2s ease;
        }

        .edit-title:focus {
          outline: none;
          border-color: #0070f3;
          box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1);
        }

        .edit-description {
          width: 100%;
          padding: 10px 12px;
          margin-bottom: 12px;
          border: 1px solid #d1d5da;
          border-radius: 6px;
          height: 80px;
          resize: vertical;
          font-size: 0.95rem;
          transition: border-color 0.2s ease;
        }

        .edit-description:focus {
          outline: none;
          border-color: #0070f3;
          box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1);
        }

        .edit-date {
          width: 100%;
          padding: 10px 12px;
          margin-bottom: 12px;
          border: 1px solid #d1d5da;
          border-radius: 6px;
          font-size: 0.95rem;
          transition: border-color 0.2s ease;
        }

        .edit-date:focus {
          outline: none;
          border-color: #0070f3;
          box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1);
        }

        .edit-buttons {
          display: flex;
          gap: 8px;
        }

        @media (max-width: 768px) {
          .todo-content {
            flex-direction: column;
            gap: 12px;
          }

          .todo-actions {
            margin-top: 8px;
            justify-content: flex-end;
          }

          .todo-meta {
            flex-direction: column;
            align-items: flex-start;
            gap: 6px;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoItem;