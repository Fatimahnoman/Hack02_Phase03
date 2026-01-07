import React from 'react';
import SignupForm from '../components/auth/SignupForm';
import Layout from '../components/layout/Layout';
import { useRouter } from 'next/router';

const SignupPage = () => {
  const router = useRouter();

  const handleGoToSignIn = () => {
    router.push('/signin');
  };

  return (
    <Layout>
      <div className="container">
        <div className="welcome-section">
          <h1>Welcome to Our Task Manager!</h1>
          <p>Join our community to organize your tasks efficiently. Create an account to get started.</p>
          <button className="welcome-button" onClick={handleGoToSignIn}>
            Already have an account? Sign In
          </button>
          <div className="divider">OR</div>
        </div>
        <SignupForm />
      </div>

      <style jsx>{`
        .container {
          max-width: 400px;
          margin: 0 auto;
          padding: 20px;
        }

        .welcome-section {
          text-align: center;
          margin-bottom: 30px;
        }

        .welcome-section h1 {
          color: #111;
          font-size: 1.8rem;
          margin-bottom: 12px;
          font-weight: 600;
        }

        .welcome-section p {
          color: #666;
          font-size: 1rem;
          margin-bottom: 20px;
          line-height: 1.5;
        }

        .welcome-button {
          background-color: #f0f7ff;
          color: #0066cc;
          border: 1px solid #c6e0ff;
          padding: 12px 24px;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
          margin-bottom: 16px;
        }

        .welcome-button:hover {
          background-color: #e6f2ff;
        }

        .divider {
          margin: 20px 0;
          position: relative;
          text-align: center;
          color: #999;
          font-size: 0.9rem;
        }

        .divider::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 0;
          right: 0;
          height: 1px;
          background-color: #e1e5e9;
          z-index: 1;
        }

        .divider::after {
          content: 'OR';
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background: white;
          padding: 0 12px;
          color: #999;
        }
      `}</style>
    </Layout>
  );
};

export default SignupPage;