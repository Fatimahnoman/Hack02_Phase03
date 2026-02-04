#!/usr/bin/env python3
"""
Database migration script to consolidate multiple SQLite databases into one.
"""

import sqlite3
import os
from pathlib import Path


def get_table_info(db_path, table_name):
    """Get table structure from a database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        return [col[1] for col in columns]  # Return column names
    finally:
        conn.close()


def migrate_tasks(source_db, target_db, table_name="task"):
    """Migrate tasks from source database to target database."""
    print(f"Migrating tasks from {source_db} to {target_db}")

    # Connect to both databases
    source_conn = sqlite3.connect(source_db)
    target_conn = sqlite3.connect(target_db)

    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()

    try:
        # Get all tasks from source
        source_cursor.execute(f"SELECT * FROM {table_name}")
        tasks = source_cursor.fetchall()

        if not tasks:
            print("No tasks found in source database")
            return

        # Get column info to construct proper INSERT statement
        source_cursor.execute(f"PRAGMA table_info({table_name})")
        source_columns = [col[1] for col in source_cursor.fetchall()]

        target_cursor.execute(f"PRAGMA table_info({table_name})")
        target_columns = [col[1] for col in target_cursor.fetchall()]

        print(f"Source columns: {source_columns}")
        print(f"Target columns: {target_columns}")

        # Create a mapping for compatible columns
        compatible_cols = []
        for col in source_columns:
            if col in target_columns:
                compatible_cols.append(col)

        if not compatible_cols:
            print("No compatible columns found!")
            return

        # Build INSERT statement with compatible columns only
        cols_str = ", ".join(compatible_cols)
        placeholders = ", ".join(["?" for _ in compatible_cols])

        # Prepare data - only include values for compatible columns
        migrated_count = 0
        for row in tasks:
            # Map row values to compatible columns
            row_dict = dict(zip(source_columns, row))
            compatible_values = [row_dict[col] for col in compatible_cols]

            try:
                target_cursor.execute(f"INSERT OR IGNORE INTO {table_name} ({cols_str}) VALUES ({placeholders})", compatible_values)
                migrated_count += 1
            except sqlite3.Error as e:
                print(f"Error inserting row: {e}")
                continue

        target_conn.commit()
        print(f"Migrated {migrated_count} tasks successfully")

    except Exception as e:
        print(f"Error during migration: {e}")
        target_conn.rollback()
    finally:
        source_conn.close()
        target_conn.close()


def main():
    """Main function to consolidate databases."""
    project_root = Path(__file__).parent

    # Define database files
    root_db = project_root / "test.db"
    backend_db = project_root / "backend" / "test.db"

    print("Database consolidation started...")
    print(f"Root database: {root_db}")
    print(f"Backend database: {backend_db}")

    # Check if databases exist
    databases = {}
    if root_db.exists():
        databases['root'] = str(root_db)
    if backend_db.exists():
        databases['backend'] = str(backend_db)

    if not databases:
        print("No databases found to migrate!")
        return

    print(f"Databases found: {list(databases.keys())}")

    # Use root database as target (this is where we want everything)
    target_db = str(root_db)

    # Migrate from all other databases to target
    for source_name, source_path in databases.items():
        if source_path != target_db:
            print(f"\nMigrating from {source_name} ({source_path}) to root ({target_db})")
            migrate_tasks(source_path, target_db)

    print("\nDatabase consolidation completed!")


if __name__ == "__main__":
    main()