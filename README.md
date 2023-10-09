# Car Rental System
The project consists of a GUI interface using Python's Tkinter library that connects to a sqlite3 database of a hypothetical car rental system using sqlite3 library. The user can then view the current records of the database and add new records in different tables of the database.

## Overview of CarRental.db
The database consists of 4 tables and 2 views.
Tables:
- Customer: CustID (primary key), Name, Phone
- Rate: Type, Category, Weekly, Daily
- Rental: CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate, Returned (int)
- Vehicle: VehicleID (primary key), Description, Year, Type, Category

Views:
- Unavailable_cars:
  ```
  SELECT Rental.VehicleID
  FROM Rental JOIN Vehicle
  ON Rental.VehicleID = Vehicle.VehicleID
  WHERE Rental.Returned = 0
  ```
- vRentalInfo:
  ```
  SELECT R.OrderDate, R.StartDate, R.ReturnDate, (JULIANDAY(R.ReturnDate) - JULIANDAY(R.StartDate)) AS TotalDays, R.VehicleID as 'VIN', V.Description AS 'Vehicle', 
  CASE WHEN V.Type = 1 THEN 'Compact'  
      WHEN V.Type = 2 THEN 'Medium' 
      WHEN V.Type = 3 THEN 'Large' 
      WHEN V.Type = 4 THEN 'SUV'  
      WHEN V.Type = 5 THEN 'Truck' 
      WHEN V.Type = 6 THEN 'Van' END AS 'Type', 
  IIF(V.Category = 0, 'Basic', 'Luxury') AS 'Category', C.CustID AS 'CustomerID', C.Name AS 'CustomerName', R.TotalAmount AS 'OrderAmount', IIF(R.Returned = 1, '0', R.TotalAmount) AS 'RentalBalance'
  FROM rental AS R JOIN vehicle AS V ON R.VehicleID = V.VehicleID JOIN customer AS C ON R.CustID = C.CustID
  ORDER BY R.StartDate ASC
  ```

## Functions of the GUI

