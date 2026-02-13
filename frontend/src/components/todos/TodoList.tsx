import React from 'react';
import { Todo, TodoUpdate } from '../../types';
import { Task, TaskUpdate } from '../../services/api';
import TodoItem from './TodoItem';

// Define a unified type for both todos and tasks
type UnifiedItem = Todo & {
  type: 'todo' | 'task';
  originalId: string | number;
};

interface TodoListProps {
  todos: UnifiedItem[];
  onToggle: (id: string | number, completed: boolean) => void;
  onUpdate: (id: string | number, updates: TodoUpdate | TaskUpdate) => void;
  onDelete: (id: string | number) => void;
  emptyState?: React.ReactNode;
}

const TodoList = ({ todos, onToggle, onUpdate, onDelete, emptyState }: TodoListProps) => {
  if (todos.length === 0) {
    return emptyState || <div className="empty-state">No tasks yet. Add one to get started!</div>;
  }

  return (
    <div className="todo-list">
      <div className="list-header">
        <h2>My Tasks</h2>
        <span className="task-count">{todos.length} {todos.length === 1 ? 'task' : 'tasks'}</span>
      </div>

      {todos.map((item) => (
        <TodoItem
          key={item.originalId}
          todo={item}
          onToggle={(id, completed) => onToggle(item.originalId, completed)}
          onUpdate={(id, updates) => onUpdate(item.originalId, updates)}
          onDelete={(id) => onDelete(item.originalId)}
        />
      ))}

      {todos.length === 0 && (
        <div className="empty-state">
          <div className="empty-state-content">
            <div className="empty-state-icon">📋</div>
            <h3>No tasks yet</h3>
            <p>Add a new task to get started organizing your work</p>
          </div>
        </div>
      )}

      <style jsx>{`
        .todo-list {
          display: flex;
          flex-direction: column;
          background: white;
          border-radius: 12px;
          padding: 25px;
          box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
          margin-top: 20px;
        }

        .list-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 20px;
          padding-bottom: 15px;
          border-bottom: 2px solid #e2e8f0;
          background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
          border-radius: 8px 8px 0 0;
          padding: 15px 20px;
        }

        .list-header h2 {
          margin: 0;
          font-size: 1.6rem;
          font-weight: 700;
          color: #2d3748;
          background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .task-count {
          background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
          color: white;
          padding: 6px 15px;
          border-radius: 20px;
          font-size: 0.95rem;
          font-weight: 600;
          box-shadow: 0 2px 8px rgba(66, 153, 225, 0.2);
        }

        .empty-state {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 300px;
          padding: 40px 20px;
          background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 100%);
          border-radius: 10px;
          margin-top: 20px;
        }

        .empty-state-content {
          text-align: center;
          color: #4a5568;
        }

        .empty-state-icon {
          font-size: 4rem;
          margin-bottom: 20px;
          filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
        }

        .empty-state h3 {
          margin: 0 0 12px 0;
          font-size: 1.5rem;
          font-weight: 600;
          color: #2d3748;
        }

        .empty-state p {
          margin: 0;
          font-size: 1rem;
          color: #718096;
        }

        @media (max-width: 768px) {
          .list-header {
            flex-direction: column;
            gap: 12px;
            align-items: center;
            text-align: center;
          }

          .task-count {
            align-self: center;
          }

          .todo-list {
            margin: 0 10px;
            padding: 20px 15px;
          }

          .empty-state {
            min-height: 250px;
            padding: 30px 15px;
          }

          .empty-state h3 {
            font-size: 1.3rem;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoList;