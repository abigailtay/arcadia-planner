# UI Form Architecture

## Directory Organization
- `/frontend/src/components/`: All reusable React UI components (NavigationBar, MainFrame, LoginForm).
- `/frontend/docs/`: All UI and accessibility documentation.

## Code Conventions
- Functional React components using hooks.
- Validation and feedback logic contained within component state.
- ARIA and accessibility attributes used on all relevant elements.
- CSS-in-JS or inline styles for form feedback; extracted stylesheets for larger apps.
