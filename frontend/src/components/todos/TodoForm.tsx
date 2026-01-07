import React, { useState } from 'react';
import { TodoCreate } from '../../types';

interface TodoFormProps {
  onSubmit: (todo: TodoCreate) => void;
}

const TodoForm = ({ onSubmit }: TodoFormProps) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    // Format the date to ISO string if provided
    let formattedDueDate: string | undefined = undefined;
    if (dueDate) {
      // Create a new Date object and set it to UTC midnight to avoid timezone issues
      const date = new Date(dueDate);
      formattedDueDate = date.toISOString();
    }

    onSubmit({
      title: title.trim(),
      description: description.trim() || undefined,
      due_date: formattedDueDate
    });
    setTitle('');
    setDescription('');
    setDueDate('');
  };

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <div className="form-header">
        <h2>Add New Task</h2>
        <p className="form-subtitle">Create a new task to stay organized</p>
      </div>

      <div className="form-group">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Task title"
          className="title-input"
          required
        />
      </div>
      <div className="form-group">
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description (optional)"
          className="description-input"
        />
      </div>
      <div className="form-group">
        <label className="date-label">Due Date</label>
        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="date-input"
        />
      </div>
      <button type="submit" className="submit-btn btn-primary">Add Task</button>
      <style jsx>{`
        .todo-form {
          background: white;
          border: 1px solid #e1e5e9;
          border-radius: 12px;
          padding: 24px;
          margin-bottom: 24px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }

        .form-header {
          margin-bottom: 20px;
        }

        .form-header h2 {
          margin: 0 0 4px 0;
          font-size: 1.4rem;
          font-weight: 600;
          color: #111;
        }

        .form-subtitle {
          margin: 0;
          color: #666;
          font-size: 0.9rem;
        }

        .form-group {
          margin-bottom: 16px;
        }

        .date-label {
          display: block;
          margin-bottom: 6px;
          font-weight: 500;
          color: #333;
          font-size: 0.9rem;
        }

        .title-input, .description-input, .date-input {
          width: 100%;
          padding: 12px 14px;
          border: 1px solid #d1d5da;
          border-radius: 8px;
          font-size: 1rem;
          transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .title-input:focus, .description-input:focus, .date-input:focus {
          outline: none;
          border-color: #0070f3;
          box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.1);
        }

        .description-input {
          height: 90px;
          resize: vertical;
          font-family: inherit;
        }

        .submit-btn {
          width: 100%;
          padding: 14px;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-primary {
          background-color: #0070f3;
          color: white;
        }

        .btn-primary:hover {
          background-color: #0060e0;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(0, 112, 243, 0.2);
        }

        .btn-primary:active {
          transform: translateY(0);
        }

        @media (max-width: 768px) {
          .todo-form {
            padding: 20px;
          }

          .form-header h2 {
            font-size: 1.25rem;
          }
        }
      `}</style>
    </form>
  );
};

export default TodoForm;