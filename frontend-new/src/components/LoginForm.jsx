import React, { useState } from 'react';
import logo from '../assets/logo.jpeg'; // Adjust if needed

function validateEmail(email) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}

export default function LoginForm({ onLoginSuccess, onRegisterClick, onForgotClick }) {
  const [emailOrUser, setEmailOrUser] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [touched, setTouched] = useState({ emailOrUser: false, password: false });
  const [loading, setLoading] = useState(false);
  const [loginError, setLoginError] = useState('');

  // Validation
  const isEmail = emailOrUser.includes('@');
  const emailValid = isEmail ? validateEmail(emailOrUser) : emailOrUser.length >= 4;
  const passwordValid = password.length >= 4;

  function realTimeFieldColor(valid) {
    return valid
      ? { border: '2px solid #28a745', outline: 'none' }
      : { border: '2px solid #dc3545', outline: 'none' };
  }

  function handleSubmit(e) {
    e.preventDefault();
    setTouched({ emailOrUser: true, password: true });
    if (!emailValid || !passwordValid) return;
    setLoading(true);
    setLoginError('');
    setTimeout(() => {
      if (
        (emailOrUser === 'demo' || emailOrUser === 'demo@arcadia.com') &&
        password === '1234'
      ) {
        setLoginError('');
        setLoading(false);
        if (onLoginSuccess) onLoginSuccess();
      } else {
        setLoginError('Invalid credentials. Try again.');
        setLoading(false);
      }
    }, 1000);
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
        className="login-form"
        aria-label="Login form"
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
          Sign in to Arcadia Planner
        </h2>
        <label htmlFor="login-email" style={{ fontWeight: 600, fontSize: 16 }}>
          Email or Username:
        </label>
        <input
          id="login-email"
          name="login-email"
          type="text"
          value={emailOrUser}
          autoComplete="username"
          style={{
            width: '100%',
            fontSize: 16,
            padding: '8px 13px',
            marginBottom: 14,
            borderRadius: 7,
            ...(touched.emailOrUser ? realTimeFieldColor(emailValid) : { border: '2px solid #eee' }),
            background: '#f7f7f7'
          }}
          onBlur={() => setTouched(t => ({ ...t, emailOrUser: true }))}
          onChange={e => setEmailOrUser(e.target.value)}
          aria-invalid={touched.emailOrUser && !emailValid}
          required
          tabIndex={1}
        />
        <label htmlFor="login-password" style={{ fontWeight: 600, fontSize: 16 }}>
          Password:
        </label>
        <input
          id="login-password"
          name="login-password"
          type="password"
          value={password}
          autoComplete="current-password"
          style={{
            width: '100%',
            fontSize: 16,
            padding: '8px 13px',
            marginBottom: 14,
            borderRadius: 7,
            ...(touched.password ? realTimeFieldColor(passwordValid) : { border: '2px solid #eee' }),
            background: '#f7f7f7'
          }}
          onBlur={() => setTouched(t => ({ ...t, password: true }))}
          onChange={e => setPassword(e.target.value)}
          aria-invalid={touched.password && !passwordValid}
          required
          tabIndex={2}
        />
        <label style={{
          display: 'flex',
          alignItems: 'center',
          gap: 7,
          marginBottom: 16,
          marginTop: 6,
          fontSize: 15,
          justifyContent: 'left'
        }}>
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={e => setRememberMe(e.target.checked)}
            tabIndex={3}
            style={{ accentColor: '#d72660', width: 17, height: 17 }}
          />
          Remember me
        </label>
        {loginError && (
          <div aria-live="polite" style={{ color: '#d32f2f', marginBottom: 9, fontSize: 15 }}>
            {loginError}
          </div>
        )}
        <button
          type="submit"
          disabled={loading}
          tabIndex={4}
          aria-disabled={loading}
          style={{
            background: loading ? '#ccc' : 'linear-gradient(90deg, #d72660, #f88379)',
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
          {loading ? 'Logging in...' : 'Login'}
        </button>
        <div style={{
          marginTop: 18,
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: 16
        }}>
          <button
            type="button"
            tabIndex={5}
            style={{
              background: 'none',
              border: 'none',
              color: '#d72660',
              textDecoration: 'underline',
              cursor: 'pointer',
              fontSize: 16
            }}
            onClick={onForgotClick}
          >
            Forgot password?
          </button>
          <button
            type="button"
            tabIndex={6}
            style={{
              background: 'none',
              border: 'none',
              color: '#6b21a8',
              textDecoration: 'underline',
              cursor: 'pointer',
              marginLeft: 10,
              fontSize: 16
            }}
            onClick={onRegisterClick}
          >
            Register
          </button>
        </div>
      </form>
    </div>
  );
}
