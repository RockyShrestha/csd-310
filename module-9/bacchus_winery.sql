-- =============================================================================
-- Course:      CSD310-T301 Database Development and Use
-- Assignment:  Module 9.1 - Case Study Milestone #2
-- Group:       Group B - Rakesh Shrestha, Josh Herrick
-- Case Study:  Bacchus Winery
-- Date:        08/08/2026
-- Description: Creates and populates the eight 3NF tables for the Bacchus
--              Winery database, based on the business rules and initial ERD
--              from Milestone #1.
-- =============================================================================
DROP DATABASE IF EXISTS bacchus_winery;
CREATE DATABASE bacchus_winery;
USE bacchus_winery;
-- -----------------------------------------------------------------------------
-- DEPARTMENT
-- Only 4 departments exist per the case study (Finance/Payroll, Marketing,
-- Production, Distribution), so only 4 rows are populated.
-- -----------------------------------------------------------------------------
CREATE TABLE DEPARTMENT (
    DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
    DepartmentName VARCHAR(50) NOT NULL UNIQUE
);
INSERT INTO DEPARTMENT (DepartmentName)
VALUES ('Finance/Payroll'),
    ('Marketing'),
    ('Production'),
    ('Distribution');
-- -----------------------------------------------------------------------------
-- EMPLOYEE
-- Self-referencing SupervisorID captures the reporting hierarchy described in
-- the Milestone #1 business rules (e.g., Ivy Brook supervises Bob Smith,
-- Lewis Walker oversees the production staff).
-- -----------------------------------------------------------------------------
CREATE TABLE EMPLOYEE (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    JobTitle VARCHAR(75) NOT NULL,
    HireDate DATE NOT NULL,
    DepartmentID INT NOT NULL,
    SupervisorID INT NULL,
    FOREIGN KEY (DepartmentID) REFERENCES DEPARTMENT(DepartmentID),
    FOREIGN KEY (SupervisorID) REFERENCES EMPLOYEE(EmployeeID)
);
INSERT INTO EMPLOYEE (
        EmployeeID,
        FirstName,
        LastName,
        JobTitle,
        HireDate,
        DepartmentID,
        SupervisorID
    )
VALUES (
        1,
        'Janet',
        'Collins',
        'Finance & Payroll Manager',
        '2015-03-10',
        1,
        NULL
    ),
    (
        2,
        'Roz',
        'Murphy',
        'Marketing Manager',
        '2016-06-01',
        2,
        NULL
    ),
    (
        3,
        'Bob',
        'Ulrich',
        'Marketing Assistant',
        '2019-09-15',
        2,
        2
    ),
    (
        4,
        'Henry',
        'Doyle',
        'Production Manager',
        '2014-01-20',
        3,
        NULL
    ),
    (
        5,
        'Maria',
        'Costanza',
        'Distribution Manager',
        '2017-11-05',
        4,
        NULL
    ),
    (
        6,
        'Lewis',
        'Walker',
        'Production Supervisor',
        '2018-04-12',
        3,
        4
    ),
    (
        7,
        'Ivy',
        'Brook',
        'Production Line Lead',
        '2020-02-18',
        3,
        6
    ),
    (
        8,
        'Bob',
        'Smith',
        'Production Line Worker',
        '2021-07-22',
        3,
        7
    );
-- -----------------------------------------------------------------------------
-- EMPLOYEE_HOURS
-- Junction/tracking table resolving the one-employee-to-many-quarterly-hours
-- need described in business rule #3. One row per employee per quarter.
-- -----------------------------------------------------------------------------
CREATE TABLE EMPLOYEE_HOURS (
    HoursRecordID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT NOT NULL,
    Quarter TINYINT NOT NULL,
    HoursYear YEAR NOT NULL,
    HoursWorked DECIMAL(6, 2) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES EMPLOYEE(EmployeeID),
    CONSTRAINT chk_quarter CHECK (
        Quarter BETWEEN 1 AND 4
    )
);
INSERT INTO EMPLOYEE_HOURS (EmployeeID, Quarter, HoursYear, HoursWorked)
VALUES (1, 1, 2025, 480.00),
    (1, 2, 2025, 472.50),
    (1, 3, 2025, 488.00),
    (1, 4, 2025, 465.00),
    (2, 1, 2025, 475.00),
    (2, 2, 2025, 480.00),
    (2, 3, 2025, 470.00),
    (2, 4, 2025, 478.50),
    (3, 1, 2025, 460.00),
    (3, 2, 2025, 455.50),
    (3, 3, 2025, 462.00),
    (3, 4, 2025, 458.00),
    (4, 1, 2025, 490.00),
    (4, 2, 2025, 485.00),
    (4, 3, 2025, 492.50),
    (4, 4, 2025, 480.00),
    (5, 1, 2025, 470.00),
    (5, 2, 2025, 468.00),
    (5, 3, 2025, 474.50),
    (5, 4, 2025, 471.00),
    (6, 1, 2025, 500.00),
    (6, 2, 2025, 495.00),
    (6, 3, 2025, 505.00),
    (6, 4, 2025, 498.50),
    (7, 1, 2025, 510.00),
    (7, 2, 2025, 502.00),
    (7, 3, 2025, 508.00),
    (7, 4, 2025, 512.50),
    (8, 1, 2025, 520.00),
    (8, 2, 2025, 515.50),
    (8, 3, 2025, 522.00),
    (8, 4, 2025, 518.00);
-- -----------------------------------------------------------------------------
-- WINE
-- Only 4 wines exist per the case study, so only 4 rows are populated.
-- -----------------------------------------------------------------------------
CREATE TABLE WINE (
    WineID INT AUTO_INCREMENT PRIMARY KEY,
    WineName VARCHAR(50) NOT NULL UNIQUE,
    WineType VARCHAR(20) NOT NULL
);
INSERT INTO WINE (WineName, WineType)
VALUES ('Merlot', 'Red'),
    ('Cabernet', 'Red'),
    ('Chablis', 'White'),
    ('Chardonnay', 'White');
-- -----------------------------------------------------------------------------
-- DISTRIBUTOR
-- -----------------------------------------------------------------------------
CREATE TABLE DISTRIBUTOR (
    DistributorID INT AUTO_INCREMENT PRIMARY KEY,
    DistributorName VARCHAR(75) NOT NULL,
    ContactName VARCHAR(75) NOT NULL,
    Phone VARCHAR(20) NOT NULL,
    Email VARCHAR(100) NOT NULL
);
INSERT INTO DISTRIBUTOR (DistributorName, ContactName, Phone, Email)
VALUES (
        'Sunrise Beverage Distributors',
        'Karen Lopez',
        '402-555-0111',
        'klopez@sunrisebev.com'
    ),
    (
        'Heartland Wine Co.',
        'Dennis Farrow',
        '402-555-0122',
        'dfarrow@heartlandwine.com'
    ),
    (
        'Blue River Imports',
        'Alicia Chen',
        '402-555-0133',
        'achen@blueriverimports.com'
    ),
    (
        'Prairie Gold Distribution',
        'Marcus Webb',
        '402-555-0144',
        'mwebb@prairiegold.com'
    ),
    (
        'Northgate Beverage Group',
        'Priya Shah',
        '402-555-0155',
        'pshah@northgatebev.com'
    ),
    (
        'Cedar Valley Wine Partners',
        'Tom Bracken',
        '402-555-0166',
        'tbracken@cedarvalleywine.com'
    );
-- -----------------------------------------------------------------------------
-- WINE_SHIPMENT
-- Junction table resolving the many-to-many relationship between WINE and
-- DISTRIBUTOR (business rule #5), with ShipmentDate/Quantity per rule #6.
-- -----------------------------------------------------------------------------
CREATE TABLE WINE_SHIPMENT (
    WineShipmentID INT AUTO_INCREMENT PRIMARY KEY,
    WineID INT NOT NULL,
    DistributorID INT NOT NULL,
    ShipmentDate DATE NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (WineID) REFERENCES WINE(WineID),
    FOREIGN KEY (DistributorID) REFERENCES DISTRIBUTOR(DistributorID)
);
INSERT INTO WINE_SHIPMENT (WineID, DistributorID, ShipmentDate, Quantity)
VALUES (1, 1, '2025-10-02', 240),
    (1, 2, '2025-10-05', 180),
    (2, 1, '2025-10-02', 200),
    (2, 3, '2025-10-08', 150),
    (3, 4, '2025-10-10', 220),
    (3, 5, '2025-10-12', 175),
    (4, 5, '2025-10-12', 190),
    (4, 6, '2025-10-15', 160),
    (2, 6, '2025-10-15', 130),
    (1, 4, '2025-10-18', 210);
-- -----------------------------------------------------------------------------
-- SUPPLIER
-- Only 3 suppliers exist per the case study (bottles/corks, labels/boxes,
-- vats/tubing), so only 3 rows are populated, per business rules #7-8.
-- -----------------------------------------------------------------------------
CREATE TABLE SUPPLIER (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(75) NOT NULL,
    ComponentType VARCHAR(50) NOT NULL,
    ContactPhone VARCHAR(20) NOT NULL,
    ContactEmail VARCHAR(100) NOT NULL
);
INSERT INTO SUPPLIER (
        SupplierName,
        ComponentType,
        ContactPhone,
        ContactEmail
    )
VALUES (
        'Midwest Glass & Cork Supply',
        'Bottles and Corks',
        '402-555-0201',
        'orders@midwestglasscork.com'
    ),
    (
        'Heritage Print & Packaging',
        'Labels and Boxes',
        '402-555-0212',
        'orders@heritageprint.com'
    ),
    (
        'Summit Tank & Tubing Co.',
        'Vats and Tubing',
        '402-555-0223',
        'orders@summittank.com'
    );
-- -----------------------------------------------------------------------------
-- SUPPLY_SHIPMENT
-- Tracks expected vs. actual delivery dates per business rule #9, so the
-- winery can calculate delivery gaps and flag late suppliers.
-- -----------------------------------------------------------------------------
CREATE TABLE SUPPLY_SHIPMENT (
    ShipmentID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierID INT NOT NULL,
    ExpectedDeliveryDate DATE NOT NULL,
    ActualDeliveryDate DATE NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES SUPPLIER(SupplierID)
);
INSERT INTO SUPPLY_SHIPMENT (
        SupplierID,
        ExpectedDeliveryDate,
        ActualDeliveryDate,
        Quantity
    )
VALUES (1, '2025-08-01', '2025-08-01', 5000),
    (1, '2025-09-01', '2025-09-04', 5000),
    (1, '2025-10-01', '2025-10-01', 5200),
    (2, '2025-08-05', '2025-08-09', 3000),
    (2, '2025-09-05', '2025-09-05', 3000),
    (2, '2025-10-05', '2025-10-11', 3100),
    (3, '2025-08-15', '2025-08-15', 40),
    (3, '2025-09-15', '2025-09-20', 40),
    (3, '2025-10-15', '2025-10-16', 45);