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
  - Function for adding new customer using provided customer name and phone number. Customer ID is generated through increment from the last entry.
- see_cust():

This function is used to view all customers in the database.
It connects to the 'CarRental.db' SQLite database.
It retrieves customer data from the 'Customer' table and displays it in a new window using Tkinter.
add_new_vehicle():

This function is used to add a new vehicle to the database.
It connects to the 'CarRental.db' SQLite database.
It inserts a new vehicle into the 'Vehicle' table with the provided vehicle ID, description, year, type, and category.
see_vehicle():

This function is used to view all vehicles in the database.
It connects to the 'CarRental.db' SQLite database.
It retrieves vehicle data from the 'Vehicle' table and displays it in a new window using Tkinter.
add_new_rental():

This function is used to add a new rental record to the database.
It connects to the 'CarRental.db' SQLite database.
It checks if the specified vehicle is available for rental by querying the 'Rental' and 'Vehicle' tables.
If the vehicle is available, it inserts a new rental record into the 'Rental' table with the provided customer ID, vehicle ID, rental start date, order date, rental type, quantity, return date, total amount, payment date, and sets the return status to 0.
available_cars():

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
