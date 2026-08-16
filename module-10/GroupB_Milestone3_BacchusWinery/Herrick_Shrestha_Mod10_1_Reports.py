"""
===============================================================================
Course:         CSD310-T301 Database Development and Use
Assignment:     Module 10.1 - Case Study Milestone #3
Group:          Group B - Rakesh Shrestha, Josh Herrick
Case Study:     Bacchus Winery
Date:           August 16, 2026
Description:    Connects to the bacchus_winery MySQL database and generate 
                reports to support business decisions.
===============================================================================
"""


# --------------------------------------------------
# Import required libraries
# --------------------------------------------------

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# --------------------------------------------------
# Load database configuration from .env
# --------------------------------------------------

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

# --------------------------------------------------
# Connect to the Bacchus Winery database
# --------------------------------------------------

try:
    db = mysql.connector.connect(**DB_CONFIG)

    if db.is_connected():
        print("\nConnected to the Bacchus Winery database successfully.")

        cursor = db.cursor()

        # --------------------------------------------------
        # Report 1: Supplier Delivery Performance
        # --------------------------------------------------

        print("\n==============================================")
        print("       SUPPLIER DELIVERY PERFORMANCE")
        print("==============================================")

        query = """
        SELECT
            supplier.SupplierName,
            supply_shipment.ShipmentID,
            supply_shipment.ExpectedDeliveryDate,
            supply_shipment.ActualDeliveryDate,

            DATEDIFF(
                supply_shipment.ActualDeliveryDate,
                supply_shipment.ExpectedDeliveryDate
            ) AS DaysLate,

            CASE
                WHEN supply_shipment.ActualDeliveryDate
                     <= supply_shipment.ExpectedDeliveryDate
                THEN 'ON TIME'
                ELSE 'LATE'
            END AS DeliveryStatus

        FROM supplier
        INNER JOIN supply_shipment
            ON supplier.SupplierID = supply_shipment.SupplierID
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(f"\nSupplier: {row[0]}")
            print(f"Shipment ID: {row[1]}")
            print(f"Expected Delivery: {row[2]}")
            print(f"Actual Delivery: {row[3]}")
            print(f"Days Late: {row[4]}")
            print(f"Status: {row[5]}")

        # --------------------------------------------------
        # Report 2: Wine Distribution Performance
        # --------------------------------------------------

        print("\n==============================================")
        print("        WINE DISTRIBUTION PERFORMANCE")
        print("==============================================")

        query = """
        SELECT
            wine.WineName,
            wine.WineType,
            distributor.DistributorName,
            SUM(wine_shipment.Quantity) AS DistributorQuantity,
            SUM(SUM(wine_shipment.Quantity)) OVER (
                PARTITION BY wine.WineID
            ) AS WineTotalQuantity
        FROM wine
        INNER JOIN wine_shipment
            ON wine.WineID = wine_shipment.WineID
        INNER JOIN distributor
            ON wine_shipment.DistributorID = distributor.DistributorID
        GROUP BY
            wine.WineID,
            wine.WineName,
            wine.WineType,
            distributor.DistributorID,
            distributor.DistributorName
        ORDER BY
            wine.WineName,
            DistributorQuantity DESC;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(f"\nWine: {row[0]}")
            print(f"Wine Type: {row[1]}")
            print(f"Distributor: {row[2]}")
            print(f"Distributor Quantity: {row[3]}")
            print(f"Total Wine Quantity: {row[4]}")

        # --------------------------------------------------
        # Report 3: Employee Hours
        # --------------------------------------------------

        print("\n==============================================")
        print("              EMPLOYEE HOURS REPORT")
        print("==============================================")

        query = """
        SELECT
            employee.FirstName,
            employee.LastName,
            department.DepartmentName,

            SUM(CASE
                WHEN employee_hours.Quarter = 1
                THEN employee_hours.HoursWorked
                ELSE 0
            END) AS Q1Hours,

            SUM(CASE
                WHEN employee_hours.Quarter = 2
                THEN employee_hours.HoursWorked
                ELSE 0
            END) AS Q2Hours,

            SUM(CASE
                WHEN employee_hours.Quarter = 3
                THEN employee_hours.HoursWorked
                ELSE 0
            END) AS Q3Hours,

            SUM(CASE
                WHEN employee_hours.Quarter = 4
                THEN employee_hours.HoursWorked
                ELSE 0
            END) AS Q4Hours,

            SUM(employee_hours.HoursWorked) AS FourQuarterTotal

        FROM employee

        INNER JOIN department
            ON employee.DepartmentID = department.DepartmentID

        INNER JOIN employee_hours
            ON employee.EmployeeID = employee_hours.EmployeeID

        WHERE employee_hours.HoursYear = 2025

        GROUP BY
            employee.EmployeeID,
            employee.FirstName,
            employee.LastName,
            department.DepartmentName

        ORDER BY
            employee.LastName,
            employee.FirstName;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(f"\nEmployee: {row[0]} {row[1]}")
            print(f"Department: {row[2]}")
            print(f"Q1 Hours: {row[3]}")
            print(f"Q2 Hours: {row[4]}")
            print(f"Q3 Hours: {row[5]}")
            print(f"Q4 Hours: {row[6]}")
            print(f"Four-Quarter Total: {row[7]}")

        # --------------------------------------------------
        # Report 4: Sales Revenue by Wine
        # --------------------------------------------------

        print("\n==============================================")
        print("           SALES REVENUE BY WINE")
        print("==============================================")

        query = """
        SELECT
            wine.WineName,
            wine.WineType,
            SUM(sales.QuantitySold) AS TotalUnitsSold,
            SUM(sales.QuantitySold * sales.UnitPrice) AS TotalRevenue

        FROM wine
        INNER JOIN sales
            ON wine.WineID = sales.WineID

        GROUP BY
            wine.WineID,
            wine.WineName,
            wine.WineType

        ORDER BY
            TotalRevenue DESC;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(f"\nWine: {row[0]}")
            print(f"Wine Type: {row[1]}")
            print(f"Total Units Sold: {row[2]}")
            print(f"Total Revenue: ${row[3]:,.2f}")

        # --------------------------------------------------
        # Report 5: Inventory & Open Purchase Orders
        # --------------------------------------------------

        print("\n==============================================")
        print("      INVENTORY & OPEN PURCHASE ORDERS")
        print("==============================================")

        print("\n--- Finished Wine Inventory ---")

        query = """
        SELECT
            wine.WineName,
            wine_inventory.QuantityOnHand,
            wine_inventory.ReorderLevel,

            CASE
                WHEN wine_inventory.QuantityOnHand
                     <= wine_inventory.ReorderLevel
                THEN 'REORDER'
                ELSE 'OK'
            END AS StockStatus

        FROM wine_inventory
        INNER JOIN wine
            ON wine_inventory.WineID = wine.WineID

        ORDER BY
            wine.WineName;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(f"\nWine: {row[0]}")
            print(f"Quantity On Hand: {row[1]}")
            print(f"Reorder Level: {row[2]}")
            print(f"Stock Status: {row[3]}")

        print("\n--- Raw Material Inventory ---")

        query = """
        SELECT
            supplier.SupplierName,
            supplier.ComponentType,
            supply_inventory.QuantityOnHand,
            supply_inventory.ReorderLevel,

            CASE
                WHEN supply_inventory.QuantityOnHand
                     <= supply_inventory.ReorderLevel
                THEN 'REORDER'
                ELSE 'OK'
            END AS StockStatus

        FROM supply_inventory
        INNER JOIN supplier
            ON supply_inventory.SupplierID = supplier.SupplierID

        ORDER BY
            supplier.SupplierName;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(f"\nSupplier: {row[0]}")
            print(f"Component Type: {row[1]}")
            print(f"Quantity On Hand: {row[2]}")
            print(f"Reorder Level: {row[3]}")
            print(f"Stock Status: {row[4]}")

        print("\n--- Open Purchase Orders ---")

        query = """
        SELECT
            supplier.SupplierName,
            purchase_order.PurchaseOrderID,
            purchase_order.OrderDate,
            purchase_order.ExpectedDeliveryDate,
            purchase_order.QuantityOrdered

        FROM purchase_order
        INNER JOIN supplier
            ON purchase_order.SupplierID = supplier.SupplierID

        WHERE purchase_order.OrderStatus = 'Open'

        ORDER BY
            purchase_order.ExpectedDeliveryDate;
        """

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(f"\nSupplier: {row[0]}")
            print(f"Purchase Order ID: {row[1]}")
            print(f"Order Date: {row[2]}")
            print(f"Expected Delivery: {row[3]}")
            print(f"Quantity Ordered: {row[4]}")

except Error as err:
    print(f"\nError connecting to MySQL: {err}")

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
        print("\nDatabase connection closed.")
