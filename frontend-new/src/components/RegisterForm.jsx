import React, { useState } from 'react';
import logo from '../assets/logo.jpeg';

function validateEmail(email) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
}

export default function RegisterForm({ onRegisterSuccess, onCancel }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirm, setConfirm] = useState('');
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  function handleSubmit(e) {
    e.preventDefault();
    let errs = {};
    if (username.length < 4) errs.username = "Username must be at least 4 characters.";
    if (!validateEmail(email)) errs.email = "Invalid email.";
    if (password.length < 4) errs.password = "Password too short.";
    if (password !== confirm) errs.confirm = "Passwords do not match.";
    setErrors(errs);
    if (Object.keys(errs).length > 0) return;

    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      alert("Registration successful! You may sign in now.");
      if (onRegisterSuccess) onRegisterSuccess();
    }, 1200);
  }

  // Adjust spacing and fit for all screens
  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: '#ffe2ed',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        minWidth: '100vw',
        zIndex: 1000,
        overflow: 'hidden' // disables scrollbars!
      }}
    >
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '18px',
          maxHeight: '92vh'
        }}
      >
        <img
          src={logo}
          alt="Arcadia Planner Logo"
          style={{
            width: 110,       // smaller to always fit!
            height: 110,
            borderRadius: '50%',
            objectFit: 'cover',
            background: '#fff',
            boxShadow: '0 4px 22px #0002',
            marginBottom: 7
          }}
        />
        <form
          onSubmit={handleSubmit}
          style={{
            minWidth: 320,     // slightly less wide
            maxWidth: 370,
            padding: '1.6rem 1.2rem', // less padding
            background: '#fff',
            borderRadius: 16,
            boxShadow: '0 4px 22px #0002',
            textAlign: 'center',
            margin: 0,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            maxHeight: '72vh', // box never gets taller than viewport minus logo!
            overflow: 'hidden'
          }}
        >
          <h2 style={{
            marginBottom: 19,
            color: '#6b21a8',
            letterSpacing: '0.05em',
            fontSize: 24,
            fontWeight: 800
          }}>
            Register for Arcadia Planner
          </h2>
          <label style={{ fontWeight: 600, fontSize: 15 }}>Username:</label>
          <input
            value={username}
            onChange={e => setUsername(e.target.value)}
            style={{
              width: "100%",
              fontSize: 15,
              padding: '7px 11px',
              marginBottom: 9,
              borderRadius: 6,
              border: errors.username ? '2px solid #dc3545' : '2px solid #eee',
              background: '#f7f7f7'
            }}
            autoComplete="username"
          />
          {errors.username && <div style={{ color: '#d32f2f', fontSize: 13 }}>{errors.username}</div>}

          <label style={{ fontWeight: 600, fontSize: 15 }}>Email:</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            style={{
              width: "100%",
              fontSize: 15,
              padding: '7px 11px',
              marginBottom: 9,
              borderRadius: 6,
              border: errors.email ? '2px solid #dc3545' : '2px solid #eee',
              background: '#f7f7f7'
            }}
            autoComplete="email"
          />
          {errors.email && <div style={{ color: '#d32f2f', fontSize: 13 }}>{errors.email}</div>}

          <label style={{ fontWeight: 600, fontSize: 15 }}>Password:</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{
              width: "100%",
              fontSize: 15,
              padding: '7px 11px',
              marginBottom: 9,
              borderRadius: 6,
              border: errors.password ? '2px solid #dc3545' : '2px solid #eee',
              background: '#f7f7f7'
            }}
            autoComplete="new-password"
          />
          {errors.password && <div style={{ color: '#d32f2f', fontSize: 13 }}>{errors.password}</div>}

          <label style={{ fontWeight: 600, fontSize: 15 }}>Confirm Password:</label>
          <input
            type="password"
            value={confirm}
            onChange={e => setConfirm(e.target.value)}
            style={{
              width: "100%",
              fontSize: 15,
              padding: '7px 11px',
              marginBottom: 9,
              borderRadius: 6,
              border: errors.confirm ? '2px solid #dc3545' : '2px solid #eee',
              background: '#f7f7f7'
            }}
            autoComplete="new-password"
          />
          {errors.confirm && <div style={{ color: '#d32f2f', fontSize: 13 }}>{errors.confirm}</div>}

          <button
            type="submit"
            disabled={loading}
            style={{
              background: loading ? '#ccc' : 'linear-gradient(90deg, #6b21a8, #d72660)',
              color: '#fff',
              fontWeight: 700,
              padding: '8px 22px',
              border: 'none',
              borderRadius: 10,
              marginTop: 8,
              cursor: loading ? 'wait' : 'pointer',
              fontSize: 16,
              letterSpacing: 1,
              boxShadow: '0 2px 6px #d7266044'
            }}
          >
            {loading ? 'Registering...' : 'Register'}
          </button>
          <div style={{
            marginTop: 12,
            display: 'flex',
            justifyContent: 'flex-end',
            fontSize: 15
          }}>
            <button
              type="button"
              style={{
                background: 'none',
                border: 'none',
                color: '#d72660',
                textDecoration: 'underline',
                cursor: 'pointer',
                fontSize: 15
              }}
              onClick={onCancel}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
