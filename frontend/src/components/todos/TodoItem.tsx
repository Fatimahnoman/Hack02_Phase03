import React from 'react';
import { Todo, TodoUpdate } from '../../types';
import { Task, TaskUpdate } from '../../services/api';

// Define a unified interface for both todos and tasks
interface UnifiedItem extends Todo {
  type?: 'todo' | 'task';
  originalId: string | number;
  created_at?: string;
  updated_at?: string;
  completed_at?: string | null;
}

interface TodoItemProps {
  todo: UnifiedItem;
  onToggle: (id: string | number, completed: boolean) => void;
  onUpdate: (id: string | number, updates: TodoUpdate | TaskUpdate) => void;
  onDelete: (id: string | number) => void;
}

const TodoItem = ({ todo, onToggle, onUpdate, onDelete }: TodoItemProps) => {
  const [isEditing, setIsEditing] = React.useState(false);
  const [editTitle, setEditTitle] = React.useState(todo.title);
  const [editDescription, setEditDescription] = React.useState(todo.description || '');
  const [editDueDate, setEditDueDate] = React.useState(todo.due_date || '');
  const [editCompleted, setEditCompleted] = React.useState(todo.completed);

  // Determine the actual ID to use based on the item type
  const actualId = todo.originalId !== undefined ? todo.originalId : todo.id;

  const handleToggle = () => {
    onToggle(actualId, !todo.completed);
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditDueDate(todo.due_date || '');
    setEditCompleted(todo.completed);
  };

  const handleSave = () => {
    // Determine if this is a TodoUpdate or TaskUpdate based on the item type
    if (todo.type === 'task') {
      // For tasks, we'll use TaskUpdate format
      onUpdate(actualId, {
        title: editTitle,
        description: editDescription,
        status: editCompleted ? 'completed' : 'pending'
      });
    } else {
      // For todos, use TodoUpdate format
      onUpdate(actualId, {
        title: editTitle,
        description: editDescription,
        due_date: editDueDate || undefined,
        completed: editCompleted
      });
    }
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
    onDelete(actualId);
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
                {(todo.due_date || todo.created_at) && (
                  <div className="todo-meta">
                    {todo.due_date ? (
                      <span className={`todo-due-date ${todo.completed ? 'completed' : ''}`}>
                        📅 {new Date(todo.due_date).toLocaleDateString()}
                      </span>
                    ) : (
                      <span className={`todo-created ${todo.completed ? 'completed' : ''}`}>
                        📅 Created: {todo.created_at ? new Date(todo.created_at).toLocaleDateString() : ''}
                      </span>
                    )}
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
          background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
          border: none;
          border-radius: 16px;
          padding: 20px;
          margin-bottom: 16px;
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
        }

        .todo-item::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          width: 4px;
          height: 100%;
          background: linear-gradient(to bottom, #667eea 0%, #764ba2 100%);
          border-radius: 16px 0 0 16px;
        }

        .todo-item:hover {
          box-shadow: 0 12px 30px rgba(102, 126, 234, 0.2);
          transform: translateY(-3px);
        }

        .todo-item.completed {
          opacity: 0.85;
          background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
        }

        .todo-content {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          gap: 16px;
        }

        .todo-header {
          display: flex;
          align-items: flex-start;
          flex: 1;
          min-width: 0;
        }

        .todo-checkbox {
          width: 28px;
          height: 28px;
          cursor: pointer;
          border: 2px solid #d1d5da;
          border-radius: 8px;
          background-color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          font-weight: bold;
          transition: all 0.3s ease;
          flex-shrink: 0;
          margin-right: 16px;
          margin-top: 2px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .todo-checkbox.completed {
          background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
          border-color: #4facfe;
          color: white;
        }

        .todo-checkbox.incomplete {
          background-color: white;
          border-color: #e2e8f0;
          color: #ff6b6b;
        }

        .todo-checkbox:hover {
          transform: scale(1.1);
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .todo-checkbox.completed:hover {
          background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        }

        .todo-checkbox.incomplete:hover {
          background-color: #fff5f5;
          border-color: #ff6b6b;
        }

        .todo-text {
          flex: 1;
          min-width: 0;
        }

        .todo-title {
          margin: 0 0 8px 0;
          font-size: 1.2rem;
          font-weight: 700;
          color: #2d3748;
          line-height: 1.4;
          word-break: break-word;
        }

        .todo-title.completed {
          text-decoration: line-through;
          color: #718096;
          opacity: 0.8;
        }

        .todo-description {
          margin: 0 0 8px 0;
          color: #4a5568;
          font-size: 1rem;
          line-height: 1.5;
          word-break: break-word;
        }

        .todo-description.completed {
          text-decoration: line-through;
          color: #a0aec0;
        }

        .todo-meta {
          display: flex;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
          margin-top: 4px;
        }

        .todo-due-date {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
        }

        .todo-due-date.completed {
          background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }

        .todo-created {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
          color: #2d3748;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
        }

        .todo-completed-badge {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
          color: white;
          border-radius: 20px;
          font-size: 0.85rem;
          font-weight: 600;
        }

        .todo-actions {
          display: flex;
          gap: 10px;
          margin-left: 16px;
          flex-shrink: 0;
        }

        .btn-primary, .btn-secondary, .btn-danger {
          border: none;
          border-radius: 10px;
          cursor: pointer;
          font-size: 0.9rem;
          padding: 10px 14px;
          transition: all 0.3s ease;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          font-weight: 600;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .btn-primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .btn-primary:hover {
          background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .btn-secondary {
          background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
          color: white;
        }

        .btn-secondary:hover {
          background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
        }

        .btn-danger {
          background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
          color: #2d3748;
        }

        .btn-danger:hover {
          background: linear-gradient(135deg, #fecfef 0%, #ff9a9e 100%);
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(255, 154, 158, 0.3);
        }

        .edit-form {
          flex: 1;
          width: 100%;
        }

        .edit-header {
          display: flex;
          align-items: flex-start;
          gap: 16px;
          margin-bottom: 16px;
        }

        .edit-checkbox {
          width: 28px;
          height: 28px;
          cursor: pointer;
          border: 2px solid #d1d5da;
          border-radius: 8px;
          background-color: white;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 14px;
          font-weight: bold;
          transition: all 0.3s ease;
          flex-shrink: 0;
          margin-right: 16px;
          margin-top: 2px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }

        .edit-checkbox.completed {
          background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
          border-color: #4facfe;
          color: white;
        }

        .edit-checkbox.incomplete {
          background-color: white;
          border-color: #e2e8f0;
          color: #ff6b6b;
        }

        .edit-checkbox:hover {
          transform: scale(1.1);
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .edit-checkbox.completed:hover {
          background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        }

        .edit-checkbox.incomplete:hover {
          background-color: #fff5f5;
          border-color: #ff6b6b;
        }

        .edit-title {
          flex: 1;
          padding: 12px 16px;
          border: 2px solid #e2e8f0;
          border-radius: 10px;
          font-size: 1.05rem;
          font-weight: 600;
          transition: all 0.3s ease;
          background: white;
        }

        .edit-title:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }

        .edit-description {
          width: 100%;
          padding: 12px 16px;
          margin-bottom: 16px;
          border: 2px solid #e2e8f0;
          border-radius: 10px;
          height: 100px;
          resize: vertical;
          font-size: 1rem;
          transition: all 0.3s ease;
          background: white;
        }

        .edit-description:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }

        .edit-date {
          width: 100%;
          padding: 12px 16px;
          margin-bottom: 16px;
          border: 2px solid #e2e8f0;
          border-radius: 10px;
          font-size: 1rem;
          transition: all 0.3s ease;
          background: white;
        }

        .edit-date:focus {
          outline: none;
          border-color: #667eea;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        }

        .edit-buttons {
          display: flex;
          gap: 10px;
        }

        @media (max-width: 768px) {
          .todo-content {
            flex-direction: column;
            gap: 16px;
          }

          .todo-actions {
            margin-top: 8px;
            justify-content: flex-end;
          }

          .todo-meta {
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
          }

          .todo-checkbox {
            margin-right: 12px;
          }

          .todo-actions {
            margin-left: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoItem;