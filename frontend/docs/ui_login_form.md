# Login Form UI

## Fields
- Email or Username (`<input type=text>`) — required
- Password (`<input type=password>`) — required
- Remember Me (`<input type=checkbox>`)

## Validation Rules
- Email: must match a basic email regex if contains '@', or must be at least 4 chars if username.
- Password: minimum 4 characters.

## Real-time Feedback
- Green border for valid inputs, red border for invalid.
- Error message shown after failed login attempt.
- "Login" button is disabled unless both fields are valid.
