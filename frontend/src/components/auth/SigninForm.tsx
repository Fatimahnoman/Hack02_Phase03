import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useRouter } from 'next/router';

const SigninForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(''); // Clear previous errors

    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      // Extract error message from server response if available
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.response?.status === 401) {
        setError('Incorrect email or password. Please try again.');
      } else {
        setError('Login failed. Please try again.');
      }
      console.error('Login error:', err);
    }
  };

  return (
    <div className="auth-form">
      <h2>Sign In</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Sign In</button>
      </form>
    </div>
  );
};

export default SigninForm;

<style jsx>{`
  .auth-form {
    background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    padding: 40px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    width: 100%;
    max-width: 400px;
  }

  .auth-form h2 {
    margin-bottom: 30px;
    text-align: center;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    background: linear-gradient(135deg, #f0f0f0 0%, #ffffff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .auth-form div {
    margin-bottom: 25px;
  }

  .auth-form label {
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
    color: #e0e0e0;
    font-size: 1rem;
  }

  .auth-form input {
    width: 100%;
    padding: 16px 20px;
    border: 2px solid #444;
    border-radius: 12px;
    font-size: 16px;
    transition: all 0.3s ease;
    background: rgba(0, 0, 0, 0.3);
    color: #fff;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .auth-form input:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3), inset 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .auth-form input::placeholder {
    color: #aaa;
  }

  .auth-form button {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  }

  .auth-form button:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  .error {
    color: #ffffff;
    background: linear-gradient(135deg, #fa5252 0%, #f5365c 100%);
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(250, 82, 82, 0.3);
    text-align: center;
  }
`}</style>