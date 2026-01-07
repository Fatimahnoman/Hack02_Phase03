import React from 'react';
import SigninForm from '../components/auth/SigninForm';
import Layout from '../components/layout/Layout';

const SigninPage = () => {
  return (
    <Layout>
      <div className="container">
        <SigninForm />
      </div>

      <style jsx>{`
        .container {
          max-width: 400px;
          margin: 0 auto;
          padding: 20px;
        }
      `}</style>
    </Layout>
  );
};

export default SigninPage;