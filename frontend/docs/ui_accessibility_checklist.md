# UI Accessibility Checklist
- All interactive elements are focusable with Tab and indicate focus visually.
- Descriptive ARIA roles/labels for navigation and buttons.
- Color contrast for text and borders meets WCAG guidelines (green/red for validation, dark font on light background).
- Real-time validation feedback provided visually (border color) and with optional messages below fields.
- Error messages use `aria-live="polite"` for screen readers.
- Logical tab order for important UI fields and navigation controls.
- All form fields have associated `<label>` for description.
