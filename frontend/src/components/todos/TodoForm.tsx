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
      <div className="form-group">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="title-input"
          required
        />
      </div>
      <div className="form-group">
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add a description (optional)"
          className="description-input"
        />
      </div>
      <div className="form-group">
        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="date-input"
        />
      </div>
      <button type="submit" className="submit-btn">Add Todo</button>
      <style jsx>{`
        .todo-form {
          background: white;
          border: 1px solid #eaeaea;
          border-radius: 8px;
          padding: 20px;
          margin-bottom: 20px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .form-group {
          margin-bottom: 15px;
        }

        .title-input, .description-input, .date-input {
          width: 100%;
          padding: 12px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 1rem;
        }

        .description-input {
          height: 80px;
          resize: vertical;
        }

        .submit-btn {
          width: 100%;
          padding: 12px;
          background-color: #0070f3;
          color: white;
          border: none;
          border-radius: 4px;
          font-size: 1rem;
          cursor: pointer;
        }

        .submit-btn:hover {
          background-color: #0060e0;
        }

        @media (max-width: 768px) {
          .todo-form {
            padding: 15px;
          }
        }
      `}</style>
    </form>
  );
};

export default TodoForm;