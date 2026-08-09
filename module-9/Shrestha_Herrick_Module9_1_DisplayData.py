"""
===============================================================================
Course:         CSD310-T301 Database Development and Use
Assignment:     Module 9.1 - Case Study Milestone #2
Group:          Group B - Rakesh Shrestha, Josh Herrick
Case Study:     Bacchus Winery
Date:           08/08/2026
Description:    Connects to the bacchus_winery MySQL database and displays
                the contents of all eight tables, one query at a time,
                using credentials stored in a local .env file.
===============================================================================
"""

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load DB credentials from .env (never committed to GitHub)
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# Order tables so parent tables print before the junction/child tables
# that reference them.
TABLES = [
    "DEPARTMENT",
    "EMPLOYEE",
    "EMPLOYEE_HOURS",
    "WINE",
    "DISTRIBUTOR",
    "WINE_SHIPMENT",
    "SUPPLIER",
    "SUPPLY_SHIPMENT",
]


def print_table(cursor, table_name):
    """Run SELECT * on a table and print the column headers and rows."""
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    print(f"\n=== {table_name} ({len(rows)} rows) ===")
    print(" | ".join(columns))
    print("-" * 70)
    for row in rows:
        print(" | ".join(str(value) for value in row))


def main():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        for table in TABLES:
            print_table(cursor, table)

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    main()
