import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import ForgotPasswordForm from './components/ForgotPasswordForm';
import MainFrame from './components/MainFrame';


export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [showForgot, setShowForgot] = useState(false);

  // Show only one thing at a time: login, register, forgot, or main app
  if (!loggedIn) {
    if (showRegister)
      return (
        <RegisterForm
          onRegisterSuccess={() => setShowRegister(false)}
          onCancel={() => setShowRegister(false)}
        />
      );
    if (showForgot)
      return (
        <ForgotPasswordForm
          onSuccess={() => setShowForgot(false)}
          onCancel={() => setShowForgot(false)}
        />
      );
    return (
      <LoginForm
        onLoginSuccess={() => setLoggedIn(true)}
        onRegisterClick={() => setShowRegister(true)}
        onForgotClick={() => setShowForgot(true)}
      />
    );
  }

  // Main app UI after login (only shown after login, never overlaps forms)
  return <MainFrame />;
}
