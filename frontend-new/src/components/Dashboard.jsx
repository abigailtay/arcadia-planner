import React from 'react';
import logo from '../assets/logo.jpeg';
import format from 'date-fns/format';
import parseISO from 'date-fns/parseISO';
import isSameDay from 'date-fns/isSameDay';
import startOfWeek from 'date-fns/startOfWeek';
import endOfWeek from 'date-fns/endOfWeek';
import isWithinInterval from 'date-fns/isWithinInterval';


const WEEKDAYS = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];


function getHabitsProgress(habits) {
  return habits.map(habit => {
    const completed = Array.isArray(habit.daysChecked)
      ? habit.daysChecked.filter(Boolean).length
      : 0;
    const percent = Math.round((completed / 7) * 100);
    return {
      name: habit.name,
      percent,
      color: habit.color || "#ffd700"
    };
  });
}


export default function Dashboard({
  user,
  setActiveSection,
  tasks,
  habits = [],
  onOpenRecipeBox // Add this prop to support section switching
}) {
  const navItems = [
    { label: 'Dashboard', key: 'dashboard' },
    { label: 'Tasks', key: 'tasks' },
    { label: 'Habits', key: 'habits' },
    { label: 'Budget', key: 'budget' },
    { label: 'Recipe Box', key: 'recipebox' }, // Section key matches your mainframe
    { label: 'Store', key: 'store' }
  ];


  const today = new Date();
  const todayTasks = tasks.filter(t =>
    t.status === 'Overdue' ||
    t.status === 'Due Today' ||
    (t.due && isSameDay(parseISO(t.due), today))
  );
  const weekStart = startOfWeek(today, { weekStartsOn: 0 });
  const weekEnd = endOfWeek(today, { weekStartsOn: 0 });
  const upcomingTasks = tasks.filter(t =>
    t.due &&
    isWithinInterval(parseISO(t.due), { start: weekStart, end: weekEnd })
  );


  const habitsProgress = getHabitsProgress(habits);


  return (
    <div
      style={{
        minHeight: '100vh',
        width: '100vw',
        background: '#ffe2ed',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'flex-start',
        overflow: 'hidden'
      }}
    >
      <div style={{ marginTop: 44 }}>
        <img
          src={logo}
          alt="Arcadia Planner Logo"
          style={{
            width: 110,
            height: 110,
            borderRadius: '50%',
            objectFit: 'cover',
            background: '#fff',
            boxShadow: '0 4px 22px #0002'
          }}
        />
      </div>
      <h1 style={{
        marginTop: 36,
        color: '#d72660',
        fontSize: 48,
        fontWeight: 800,
        letterSpacing: '0.04em',
        textAlign: 'center'
      }}>
        Welcome to Arcadia Planner{user ? `, ${user}` : ''}!
      </h1>
      {/* NAVIGATION BUTTONS */}
      <div style={{
        margin: '48px auto 18px auto',
        display: 'flex',
        gap: 40,
        justifyContent: 'center',
        flexWrap: 'wrap'
      }}>
        {navItems.map(item => (
          <button
            key={item.key}
            style={{
              background: 'linear-gradient(90deg, #d72660, #6b21a8)',
              color: '#fff',
              fontWeight: 700,
              fontSize: 22,
              border: 'none',
              borderRadius: 16,
              boxShadow: '0 2px 8px #6b21a855',
              margin: '0 12px',
              padding: '24px 46px',
              cursor: 'pointer',
              letterSpacing: '0.08em',
              minWidth: 160,
              minHeight: 68
            }}
            onClick={
              item.key === 'recipebox'
                ? onOpenRecipeBox // Only Recipe Box uses the section switch prop from MainFrame
                : () => setActiveSection(item.key)
            }
          >
            {item.label}
          </button>
        ))}
      </div>
      {/* SUMMARY/PROGRESS BOXES */}
      <div style={{
        marginTop: 60,
        display: 'flex',
        gap: 40,
        justifyContent: 'center',
        flexWrap: 'wrap'
      }}>
        {/* Today's Tasks */}
        <div style={{
          background: '#fff',
          borderRadius: 18,
          boxShadow: '0 2px 16px #6b21a830',
          width: 300,
          minHeight: 120,
          padding: '32px 34px',
          textAlign: 'center',
          fontSize: 22,
          color: '#6b21a8',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center'
        }}>
          <div style={{ fontWeight: 800, marginBottom: 10 }}>
            Today's Tasks
          </div>
          {todayTasks.length === 0 ? (
            <span>No tasks</span>
          ) : (
            <ul style={{ textAlign: 'left', fontSize: 16, margin: "8px 0 0 12px", color: "#444" }}>
              {todayTasks.map(t => (
                <li key={t.id}>{t.title} ({t.due ? format(parseISO(t.due), 'MMM d, EEE') : "No due date"})</li>
              ))}
            </ul>
          )}
        </div>

        {/* Upcoming Tasks: all this Sunday–Saturday */}
        <div style={{
          background: '#fff',
          borderRadius: 18,
          boxShadow: '0 2px 16px #d7266030',
          width: 300,
          minHeight: 120,
          padding: '32px 34px',
          textAlign: 'center',
          fontSize: 22,
          color: '#d72660',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center'
        }}>
          <div style={{ fontWeight: 800, marginBottom: 10 }}>
            Upcoming Tasks <span style={{ fontWeight: 400, fontSize: "14px" }}>(Sun–Sat)</span>
          </div>
          {upcomingTasks.length === 0 ? (
            <span>No tasks</span>
          ) : (
            <ul style={{ textAlign: 'left', fontSize: 16, margin: "8px 0 0 12px", color: "#444" }}>
              {upcomingTasks
                .sort((a, b) =>
                  (a.due && b.due) ? parseISO(a.due) - parseISO(b.due) : 0
                )
                .map(t => (
                  <li key={t.id}>
                    {t.title} ({t.due ? format(parseISO(t.due), 'MMM d, EEE') : "No due date"})
                  </li>
                ))}
            </ul>
          )}
        </div>

        {/* Habits Progress */}
        <div style={{
          background: '#fff',
          borderRadius: 18,
          boxShadow: '0 2px 16px #ffd70030',
          width: 300,
          minHeight: 120,
          padding: '32px 34px',
          textAlign: 'center',
          fontSize: 22,
          color: '#ffd700',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center'
        }}>
          <div style={{ fontWeight: 800, marginBottom: 10 }}>
            Habits Progress
          </div>
          {habitsProgress.length === 0 ? (
            <div style={{ fontSize: 18, color: "#aaa" }}>No data</div>
          ) : (
            <ul style={{ textAlign: 'left', fontSize: 16, margin: "8px 0 0 12px", color: "#444" }}>
              {habitsProgress.map(habit => (
                <li key={habit.name}>
                  {habit.name}: {habit.percent}%
                  <div style={{
                    height: 6, width: "85%",
                    background: "#f6e5a1", borderRadius: 8, margin: "2px 0 10px 0"
                  }}>
                    <div style={{
                      height: 6,
                      width: `${habit.percent}%`,
                      background: habit.color || "#ffd700",
                      borderRadius: 8
                    }} />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
