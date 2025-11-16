# Navigation Bar UI

## Button/Label Text
- Dashboard
- Tasks
- Habits
- Budget
- Recipe Box
- Store

## ARIA Roles and Labels
- Navigation bar: `role="navigation"`, `aria-label="Main navigation"`
- Buttons: Each button has `aria-label` matching its text (e.g. `aria-label="Dashboard"`).
- The active page sets `aria-current="page"` on its button.

## Keyboard Navigation
- Each button is focusable via Tab key.
- The order of the buttons corresponds to their visual order (tabIndex set incrementally).
- Users can navigate and select with Enter/Spacebar as with standard buttons.
