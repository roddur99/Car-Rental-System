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
- Unavailable_cars: Shows cars already rented out and not returned yet.
  ```
  SELECT Rental.VehicleID
  FROM Rental JOIN Vehicle
  ON Rental.VehicleID = Vehicle.VehicleID
  WHERE Rental.Returned = 0
  ```
- vRentalInfo: Creates a view where Vehicle Type and Category (both ints) are 'translated' to a string that's more user-friendly. Furthermore, TotalDays attribute is calculated using the start and return dates of the rentals.
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
- add_new_cust():
  - Function for adding new customers using user-provided customer name and phone number.
  - Executes an INSERT INTO SQL statement into the 'Customer' table
  - Customer ID is generated through increment from the last entry.
    
- see_cust():
  - Function for viewing all customer records in the database
  - Executes a SELECT statement from the 'Customer' table.
    
- add_new_vehicle():
  - Function for adding new vehicles using user-provided vehicle ID, description, year, type, and category.
  - Executes an INSERT INTO SQL statement into the 'Vehicle' table.
    
- see_vehicle():
  - Function for viewing all vehicle records in the database
  - Executes a SELECT statement from the 'Vehicle' table.
    
- add_new_rental():
  - Function adds a new rental record.
  - Checks whether the vehicle asked by the user is available or not using Vehicle ID. If available, a new record is added, return status is set to 0, and a confirmation message is printed on-screen.
    
- available_cars():
  - Function for seeing available cars for rental
  - SQL view 'Unavailable_cars' is used to retrieve unavailable cars and SELECT statements are used to get cars that are NOT IN 'Unavailable_cars'.
    
- rental_return():
  - Function that calculates the amount owed.
  - Updates returned rentals by setting return status to 1.
  
- search_cust():
  - Function for searching customer in 'vRentalInfo' view.
  - Search is based on Customer ID and Name

- search_vehicle():
  - Function for searching customer in 'vRentalInfo' view.
  - Search is based on Vehicle ID and Description

## How to run
- Required libraries: Tkinter, sqlite3
- Run on Anaconda Prompt or any terminal that supports running python scripts, eg:
   ```python car_rental_gui.py```
