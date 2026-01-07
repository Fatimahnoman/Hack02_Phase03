import React from 'react';
import Layout from '../components/layout/Layout';
import Link from 'next/link';

const HomePage = () => {
  return (
    <Layout>
      <div className="container">
        <div className="hero">
          <h1 className="evolution-text">Evolution of Todo</h1>
          <p><strong>Welcome To Our Task Manager</strong></p>
          <p>Would you like to Sign In? If yes then click on <Link href="/signin" legacyBehavior><a className="signin-link">Sign In</a></Link></p>
        </div>
      </div>
      <style jsx>{`
        .hero {
          text-align: center;
          padding: 60px 20px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          min-height: 80vh;
        }

        .evolution-text {
          font-size: 1.5rem;
          margin: 10px 0 20px 0;
          color: #0070f3; /* Blue color */
          text-decoration: underline; /* Underline */
          text-decoration-color: #000; /* Black underline */
          font-weight: bold;
        }

        .hero p {
          font-size: 1.2rem;
          color: #666;
          margin-bottom: 30px;
        }

        .signin-link {
          color: #0070f3;
          text-decoration: underline;
          font-weight: bold;
          cursor: pointer;
        }

        .signin-link:hover {
          color: #0060e0;
        }

        @media (max-width: 768px) {
          .evolution-text {
            font-size: 1.2rem;
          }

          .hero p {
            font-size: 1rem;
          }
        }
      `}</style>
    </Layout>
  );
};

export default HomePage;