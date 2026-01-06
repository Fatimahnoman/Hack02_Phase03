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

  const handleToggle = () => {
    onToggle(todo.id, !todo.completed);
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
  };

  const handleSave = () => {
    onUpdate(todo.id, {
      title: editTitle,
      description: editDescription,
      due_date: editDueDate || undefined
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditDueDate(todo.due_date || '');
  };

  const handleDelete = () => {
    onDelete(todo.id);
  };

  return (
    <div className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <div className="todo-content">
        {isEditing ? (
          <div className="edit-form">
            <input
              type="text"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              className="edit-title"
            />
            <textarea
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              className="edit-description"
            />
            <input
              type="date"
              value={editDueDate}
              onChange={(e) => setEditDueDate(e.target.value)}
              className="edit-date"
            />
            <div className="edit-buttons">
              <button onClick={handleSave} className="save-btn">Save</button>
              <button onClick={handleCancel} className="cancel-btn">Cancel</button>
            </div>
          </div>
        ) : (
          <>
            <div className="todo-header">
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={handleToggle}
                className="todo-checkbox"
              />
              <div className="todo-text">
                <h3 className={`todo-title ${todo.completed ? 'completed' : ''}`}>{todo.title}</h3>
                {todo.description && (
                  <p className={`todo-description ${todo.completed ? 'completed' : ''}`}>{todo.description}</p>
                )}
                {todo.due_date && (
                  <p className={`todo-due-date ${todo.completed ? 'completed' : ''}`}>
                    Due: {new Date(todo.due_date).toLocaleDateString()}
                  </p>
                )}
              </div>
            </div>
            <div className="todo-actions">
              <button onClick={handleEdit} className="edit-btn">Edit</button>
              <button onClick={handleDelete} className="delete-btn">Delete</button>
            </div>
          </>
        )}
      </div>
      <style jsx>{`
        .todo-item {
          background: white;
          border: 1px solid #eaeaea;
          border-radius: 8px;
          padding: 15px;
          margin-bottom: 10px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .todo-item.completed {
          opacity: 0.7;
        }

        .todo-content {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }

        .todo-header {
          display: flex;
          align-items: flex-start;
          flex: 1;
        }

        .todo-checkbox {
          margin-right: 10px;
          margin-top: 4px;
        }

        .todo-text {
          flex: 1;
        }

        .todo-title {
          margin: 0 0 5px 0;
          font-size: 1.1rem;
        }

        .todo-title.completed {
          text-decoration: line-through;
          color: #888;
        }

        .todo-description {
          margin: 0;
          color: #666;
          font-size: 0.9rem;
        }

        .todo-description.completed {
          text-decoration: line-through;
          color: #aaa;
        }

        .todo-due-date {
          margin: 5px 0 0 0;
          color: #666;
          font-size: 0.8rem;
          font-weight: bold;
        }

        .todo-due-date.completed {
          color: #aaa;
        }

        .todo-actions {
          display: flex;
          gap: 5px;
          margin-left: 10px;
        }

        .edit-btn, .delete-btn, .save-btn, .cancel-btn {
          padding: 5px 10px;
          border: 1px solid #ddd;
          background: white;
          border-radius: 4px;
          cursor: pointer;
          font-size: 0.8rem;
        }

        .edit-btn:hover, .delete-btn:hover {
          background: #f0f0f0;
        }

        .delete-btn {
          background: #ffecec;
          border-color: #f88;
        }

        .delete-btn:hover {
          background: #fdd;
        }

        .edit-form {
          flex: 1;
        }

        .edit-title {
          width: 100%;
          padding: 8px;
          margin-bottom: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 1rem;
        }

        .edit-description {
          width: 100%;
          padding: 8px;
          margin-bottom: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          height: 60px;
          resize: vertical;
          font-size: 0.9rem;
        }

        .edit-date {
          width: 100%;
          padding: 8px;
          margin-bottom: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 0.9rem;
        }

        .edit-buttons {
          display: flex;
          gap: 10px;
        }

        @media (max-width: 768px) {
          .todo-content {
            flex-direction: column;
          }

          .todo-actions {
            margin-top: 10px;
            justify-content: flex-end;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoItem;