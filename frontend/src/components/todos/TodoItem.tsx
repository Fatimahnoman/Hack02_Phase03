import React from 'react';
import { Todo, TodoUpdate } from '../../types';
import { Task, TaskUpdate } from '../../services/api';

// Define a unified type for both todos and tasks
type UnifiedItem = Todo & {
  type?: 'todo' | 'task';
  originalId: string | number;
  updated_at?: string;
  completed_at?: string | null;
};

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

  // ID handling – safe way
  const actualId = todo.originalId ?? todo.id;  // ?? better than !== undefined

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
    if (todo.type === 'task') {
      onUpdate(actualId, {
        title: editTitle,
        description: editDescription,
        status: editCompleted ? 'completed' : 'pending',
      } as TaskUpdate);
    } else {
      onUpdate(actualId, {
        title: editTitle,
        description: editDescription,
        due_date: editDueDate || undefined,
        completed: editCompleted,
      } as TodoUpdate);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
    // Reset to original values
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditDueDate(todo.due_date || '');
    setEditCompleted(todo.completed);
  };

  const handleDelete = () => {
    onDelete(actualId);
  };

  // Safe date rendering
  const formatDate = (dateStr?: string) =>
    dateStr ? new Date(dateStr).toLocaleDateString() : 'No date';

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
              <button onClick={handleSave} className="save-btn btn-primary">
                Save
              </button>
              <button onClick={handleCancel} className="cancel-btn btn-secondary">
                Cancel
              </button>
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
                <h3 className={`todo-title ${todo.completed ? 'completed' : ''}`}>
                  {todo.title}
                </h3>
                {todo.description && (
                  <p className={`todo-description ${todo.completed ? 'completed' : ''}`}>
                    {todo.description}
                  </p>
                )}
                <div className="todo-meta">
                  {todo.due_date && (
                    <span className={`todo-due-date ${todo.completed ? 'completed' : ''}`}>
                      📅 {formatDate(todo.due_date)}
                    </span>
                  )}
                  {!todo.due_date && todo.created_at && (
                    <span className={`todo-created ${todo.completed ? 'completed' : ''}`}>
                      📅 Created: {formatDate(todo.created_at)}
                    </span>
                  )}
                  {todo.completed && (
                    <span className="todo-completed-badge">✓ Completed</span>
                  )}
                </div>
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

      {/* Styles same rakh sakti ho – maine sirf thoda clean kiya hai, changes nahi kiye */}
      <style jsx>{`
        /* Tumhara pura style yahan paste kar do – bilkul same rahega */
        /* ... copy your original <style jsx> content here ... */
      `}</style>
    </div>
  );
};

export default TodoItem;