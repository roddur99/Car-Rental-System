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
  - Executes an INSERT INTO SQL statement into the 'Vehicle' table
- see_vehicle():
  - Function for viewing all vehicle records in the database
  - Executes a SELECT statement from the 'Vehicle' table.
- add_new_rental():
  - Function adds a new rental record.
  - Checks whether the vehicle asked by the user is available or not using Vehicle ID. If available, a new record is added and a confirmation message is printed on-screen.
- available_cars():

This function is used to display a list of available cars for rental.
It connects to the 'CarRental.db' SQLite database.
It uses a SQL view named 'Unavailable_Cars' to find unavailable cars and displays the available ones in a Tkinter window.
rental_return():

This function is used to calculate and display the total amount due for rentals based on various search criteria.
It connects to the 'CarRental.db' SQLite database.
It calculates the total amount due for rentals based on the specified search criteria (return date, customer name, VIN, vehicle, type, category) and updates the 'Rental' table by setting the return status to 1 for the returned rentals.
search_cust():

This function is used to search for customers in the 'vRentalInfo' view based on customer ID and name.
It connects to the 'CarRental.db' SQLite database.
It constructs a SQL query based on the provided customer ID and name, retrieves the results, and displays them in a Tkinter window.
search_vehicle():

This function is used to search for vehicles in the 'vRentalInfo' view based on VIN and vehicle description.
It connects to the 'CarRental.db' SQLite database.
It constructs a SQL query based on the provided VIN and description, retrieves the results, and displays them in a Tkinter window.
