import React from 'react';
import { Todo, TodoUpdate } from '../../types';
import TodoItem from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  onToggle: (id: number, completed: boolean) => void;
  onUpdate: (id: number, updates: TodoUpdate) => void;
  onDelete: (id: number) => void;
  emptyState?: React.ReactNode;
}

const TodoList = ({ todos, onToggle, onUpdate, onDelete, emptyState }: TodoListProps) => {
  if (todos.length === 0) {
    return emptyState || <div className="empty-state">No todos yet. Add one to get started!</div>;
  }

  return (
    <div className="todo-list">
      <div className="list-header">
        <h2>My Tasks</h2>
        <span className="task-count">{todos.length} {todos.length === 1 ? 'task' : 'tasks'}</span>
      </div>

      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onUpdate={onUpdate}
          onDelete={onDelete}
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
        }

        .list-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
          padding-bottom: 12px;
          border-bottom: 1px solid #e1e5e9;
        }

        .list-header h2 {
          margin: 0;
          font-size: 1.5rem;
          font-weight: 600;
          color: #111;
        }

        .task-count {
          background-color: #f0f7ff;
          color: #0066cc;
          padding: 4px 12px;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 500;
        }

        .empty-state {
          display: flex;
          align-items: center;
          justify-content: center;
          min-height: 300px;
          padding: 20px;
        }

        .empty-state-content {
          text-align: center;
          color: #666;
        }

        .empty-state-icon {
          font-size: 3rem;
          margin-bottom: 16px;
        }

        .empty-state h3 {
          margin: 0 0 8px 0;
          font-size: 1.25rem;
          color: #333;
        }

        .empty-state p {
          margin: 0;
          font-size: 0.95rem;
          color: #666;
        }

        @media (max-width: 768px) {
          .list-header {
            flex-direction: column;
            gap: 8px;
            align-items: flex-start;
          }

          .todo-list {
            margin: 0 10px;
          }
        }
      `}</style>
    </div>
  );
};

export default TodoList;