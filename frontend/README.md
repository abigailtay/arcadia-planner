# Arcadia Planner

An XP-based planner application for students to manage academics, daily life, and finances.

## Team
- **Allyson Taylor** - Technical Author & Designer
- **Xavier Nixon** - Lead Software Engineer

## Tech Stack
- **Frontend:** PyQt6
- **Backend:** Python 3.11+
- **Database:** SQLite3
- **Testing:** pytest

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Git

### Installation

1. Clone the repository:
git clone https://github.com/your-username/arcadia-planner.git
cd arcadia-planner


2. Create virtual environment:
Mac/Linux
python3 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Initialize database:
python src/database/init_db.py

5. Run the application:
python src/main.py

## Project Structure
arcadia-planner/
├── docs/ # Documentation
├── src/ # Source code
│ ├── ui/ # PyQt UI components
│ ├── database/ # Database management
│ ├── controllers/ # Business logic
│ ├── models/ # Data models
│ └── utils/ # Utilities
├── tests/ # Unit tests
├── assets/ # Images, icons
└── README.md


## Sprint 1 Goals (Week 1)
- [ ] Environment setup
- [ ] Database schema & authentication
- [ ] UI framework & navigation
- [ ] Tasks module (CRUD)

## Development Workflow

### Daily Standup
- Time: 9:00 AM daily
- Format: What did I do? What will I do? Any blockers?

### Sprint Planning
- Weekly meeting: Thursdays 2:00-5:00 PM

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Commit: `git commit -m "Description of changes"`
4. Push: `git push origin feature/your-feature-name`
5. Create Pull Request on GitHub
6. Wait for review from team member

## UI Documentation and Accessibility
See docs in `/docs/`:
- [Navigation Bar UI](./docs/ui_navbar.md)
- [Login Form UI](./docs/ui_login_form.md)
- [Accessibility Checklist](./docs/ui_accessibility_checklist.md)
- [UI Form Architecture](./docs/ui_form_architecture.md)
