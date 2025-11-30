export default function NavigationBar({ activeSection, onSelect }) {
  const navItems = [
    { label: 'Dashboard', key: 'dashboard' },
    { label: 'Tasks', key: 'tasks' },
    { label: 'Habits', key: 'habits' },
    { label: 'Budget', key: 'budget' },
    { label: 'Recipe Box', key: 'recipes' },
    { label: 'Store', key: 'store' }
  ];
  return (
    <nav
      className="navigation-bar"
      role="navigation"
      aria-label="Main navigation"
      style={{
        display: 'flex',
        justifyContent: 'space-around',
        width: '100%',
        position: 'fixed',
        bottom: 0,
        background: '#fff',
        zIndex: 100,
        borderTop: '2px solid #a259bc'
      }}
    >
      {navItems.map((item, idx) => (
        <button
          key={item.key}
          tabIndex={idx + 1}
          aria-label={item.label}
          aria-current={activeSection === item.key ? 'page' : undefined}
          style={{
            fontSize: '2.3rem',
            fontWeight: activeSection === item.key ? 900 : 700,
            padding: '1.1rem 0',
            background: activeSection === item.key ? '#f3c7db' : 'none', // highlight active tab
            border: 'none',
            color: activeSection === item.key ? '#d72660' : '#6b21a8',
            cursor: 'pointer',
            flex: 1,
            textAlign: 'center',
            borderRight: idx !== navItems.length - 1 ? '2px solid #a259bc' : 'none',
            borderTop: 'none',
            outline: 'none'
          }}
          className="nav-btn"
          onClick={() => onSelect(item.key)}
        >
          {item.label}
        </button>
      ))}
    </nav>
  );
}
