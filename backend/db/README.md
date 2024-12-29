# Database Directory

## Overview
This directory contains database-related scripts for the Janus project. It handles the database schema, helpers, and seed data required for the application to function properly. The database is designed to work with SQLAlchemy and SQLite (for development purposes), with future support for more scalable databases planned.

---

## Files and their Purpose

### **db/**
- **db_setup.py**: Script for setting up the database schema. It creates the necessary tables for the application to interact with, including `images` for storing metadata. **[✅ Completed | Ticket #001, #010]**
- **db_helpers.py**: Contains common database operations, such as queries and utilities for interacting with the `images` table. **[❌ Pending | Phase 2]**
- **seed_data.py**: Script for populating the database with initial data, useful for testing or seeding the application with necessary content. **[❌ Pending | Phase 2]**

---

## Database Schema

The database schema is defined using SQLAlchemy models in `models.py`. Currently, the only table is `images`, which holds metadata about uploaded images. Future tables are planned for users, admins, logs, and analytics.

### Best Practices Considerations:
- **Normalization**: The schema follows normalization best practices with foreign key relationships.
- **Indexes**: For performance, especially with searches, indexes should be added on frequently queried columns, such as `email` in the `users` table and `timestamp` in the `logs` table.
- **Data Integrity**: All foreign key constraints are set up to ensure referential integrity between related tables.
- **Scalability**: The schema is designed to scale by adding more tables in a structured way, preparing for future database migrations (e.g., PostgreSQL or MySQL).

---

## Database Setup

1. **Initialization**: The database schema is set up by running `db_setup.py`.
2. **Database URI**: The application is configured to use SQLite by default with the URI pointing to `instance/image_processing.db`.

---

## Future Improvements
- **Support for other databases**: The current implementation uses SQLite for simplicity and development. Future plans involve migrating to more robust systems like PostgreSQL or MySQL, as outlined in the [future issues](#).
- **Data seeding**: We'll enhance the seeding script to populate the database with more comprehensive data for testing and development.

---

## Testing the Database
Database-related tests should be written to ensure that the schema is properly created and that the database performs as expected. Tests should be added to the `tests` folder, specifically for database queries and functionality.

---
