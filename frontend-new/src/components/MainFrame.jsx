import React, { useState, useEffect } from 'react';
import Dashboard from './Dashboard';
import Tasks from './Tasks';
import Habits from './Habits';
import Budgets from './Budgets';     // ✅ use the correct filename
import RecipeBox from './RecipeBox';
import Store from './Store';         // ✅ import Store

export default function MainFrame() {
  const [activeSection, setActiveSection] = useState('dashboard');
  const [tasks, setTasks] = useState([]);
  const [habits, setHabits] = useState([]);
  const [user, setUser] = useState(null);

  useEffect(() => {
    // your existing data-loading logic...
  }, []);

  return (
    <>
      {activeSection === 'dashboard' && (
        <Dashboard
          user={user}
          setActiveSection={setActiveSection}
          tasks={tasks}
          habits={habits}
          onOpenRecipeBox={() => setActiveSection('recipebox')}
        />
      )}

      {activeSection === 'tasks' && (
        <Tasks
          tasks={tasks}
          setTasks={setTasks}
          onBackToDashboard={() => setActiveSection('dashboard')}
        />
      )}

      {activeSection === 'habits' && (
        <Habits
          habits={habits}
          setHabits={setHabits}
          onBackToDashboard={() => setActiveSection('dashboard')}
        />
      )}

      {activeSection === 'budget' && (
        <Budgets
          onBackToDashboard={() => setActiveSection('dashboard')}
        />
      )}

      {activeSection === 'recipebox' && (
        <RecipeBox
          onBackToDashboard={() => setActiveSection('dashboard')}
        />
      )}

      {activeSection === 'store' && (
        <Store
          onBackToDashboard={() => setActiveSection('dashboard')}
        />
      )}
    </>
  );
}
