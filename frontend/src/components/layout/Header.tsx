import React from 'react';
import Link from 'next/link';
import { useAuth } from '../../hooks/useAuth';

const Header = () => {
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <Link href="/">
            <h1 className="logo">Task Manager</h1>
          </Link>
          <nav className="nav">
            {isAuthenticated ? (
              <>
                <Link href="/dashboard">Dashboard</Link>
                <span>Welcome, {user?.email}</span>
                <button onClick={handleLogout}>Logout</button>
              </>
            ) : (
              <>
                <Link href="/signin">Sign In</Link>
                <Link href="/signup">Sign Up</Link>
              </>
            )}
          </nav>
        </div>
      </div>
      <style jsx>{`
        .header {
          background-color: #fff;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          padding: 10px 0;
        }

        .header-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .logo {
          margin: 0;
          font-size: 1.5rem;
          color: #333; /* Changed from blue to neutral color */
        }

        .logo:hover {
          text-decoration: none;
        }

        .nav {
          display: flex;
          align-items: center;
          gap: 20px;
        }

        .nav a,
        .nav button {
          text-decoration: none;
          color: #333;
          padding: 8px 12px;
          border-radius: 4px;
          background: none;
          border: none;
          cursor: pointer;
          font-size: 1rem;
        }

        .nav a:hover,
        .nav button:hover {
          background-color: #f0f0f0;
        }

        @media (max-width: 768px) {
          .header-content {
            flex-direction: column;
            gap: 10px;
          }

          .nav {
            width: 100%;
            justify-content: center;
            flex-wrap: wrap;
          }
        }
      `}</style>
    </header>
  );
};

export default Header;