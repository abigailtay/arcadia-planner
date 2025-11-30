import React, { useState } from 'react';
import logo from '../assets/logo.jpeg';

function validateEmail(email) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}

export default function ForgotPasswordForm({ onSuccess, onCancel }) {
  const [email, setEmail] = useState('');
  const [touched, setTouched] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const emailValid = validateEmail(email);

  function handleSubmit(e) {
    e.preventDefault();
    setTouched(true);
    if (!emailValid) return;
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setSubmitted(true);
      if (onSuccess) onSuccess();
    }, 1200);
  }

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: '#ffe2ed',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        minHeight: '100vh',
        minWidth: '100vw',
        flexDirection: 'column'
      }}
    >
      <img
        src={logo}
        alt="Arcadia Planner Logo"
        style={{
          display: 'block',
          margin: '0 auto 36px auto',
          width: 130,
          height: 130,
          borderRadius: '50%',
          objectFit: 'cover',
          background: '#fff',
          boxShadow: '0 4px 22px #0002'
        }}
      />
      <form
        onSubmit={handleSubmit}
        style={{
          minWidth: 340,
          maxWidth: 380,
          padding: '2.5rem 2rem',
          background: '#fff',
          borderRadius: 18,
          boxShadow: '0 4px 22px #0002',
          textAlign: 'center',
          margin: '0 auto'
        }}
      >
        <h2 style={{
          marginBottom: 30,
          color: '#d72660',
          letterSpacing: '0.05em',
          fontSize: 28,
          fontWeight: 800
        }}>
          Forgot your password?
        </h2>
        {!submitted ? (
          <>
            <label htmlFor="forgot-email" style={{ fontWeight: 600, fontSize: 16 }}>
              Enter your email address:
            </label>
            <input
              id="forgot-email"
              name="forgot-email"
              type="email"
              value={email}
              autoComplete="email"
              style={{
                width: '100%',
                fontSize: 16,
                padding: '8px 13px',
                marginBottom: 14,
                borderRadius: 7,
                border: touched && !emailValid ? '2px solid #dc3545' : '2px solid #eee',
                background: '#f7f7f7'
              }}
              onBlur={() => setTouched(true)}
              onChange={e => setEmail(e.target.value)}
              aria-invalid={touched && !emailValid}
              required
              tabIndex={1}
            />
            {!emailValid && touched &&
              <div style={{ color: '#d32f2f', marginBottom: 10, fontSize: 15 }}>
                Please enter a valid email.
              </div>
            }
            <button
              type="submit"
              disabled={loading}
              tabIndex={2}
              aria-disabled={loading}
              style={{
                background: loading ? '#ccc' : 'linear-gradient(90deg, #6b21a8, #d72660)',
                color: '#fff',
                fontWeight: 700,
                padding: '10px 34px',
                border: 'none',
                borderRadius: 12,
                marginTop: 10,
                cursor: loading ? 'wait' : 'pointer',
                fontSize: 18,
                letterSpacing: 1,
                boxShadow: '0 2px 6px #d7266044'
              }}
            >
              {loading ? 'Sending...' : 'Send Reset Link'}
            </button>
            <div style={{
              marginTop: 18,
              display: 'flex',
              justifyContent: 'flex-end',
              fontSize: 16
            }}>
              <button
                type="button"
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#d72660',
                  textDecoration: 'underline',
                  cursor: 'pointer',
                  fontSize: 16
                }}
                onClick={onCancel}
              >
                Cancel
              </button>
            </div>
          </>
        ) : (
          <div style={{ fontSize: 20, color: '#333', marginTop: 40 }}>
            If you entered a valid email, a password reset link has been sent.<br />
            Please check your inbox.
            <div style={{
              marginTop: 18,
              display: 'flex',
              justifyContent: 'center',
              fontSize: 16
            }}>
              <button
                type="button"
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#d72660',
                  textDecoration: 'underline',
                  cursor: 'pointer',
                  fontSize: 16
                }}
                onClick={onCancel}
              >
                Return
              </button>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
