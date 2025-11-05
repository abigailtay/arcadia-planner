# Database Migration Notes

## v1.0 - Sprint 1
- Initial schema created: users, tasks, user_currency tables and indexes.
- If upgrading schema, use:
    1. Backup arcadia.db
    2. For new columns, use ALTER TABLE.
    3. To reset, delete arcadia.db and run python3 database/db_manager.py
- If adding a column (example):
    ALTER TABLE users ADD COLUMN bio TEXT DEFAULT '';

