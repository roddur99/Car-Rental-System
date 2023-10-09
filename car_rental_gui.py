from tkinter import *
import sqlite3

root = Tk()
root.title('CarRental2019')
root.geometry("900x900")


# Function for adding new customer
def add_new_cust():
    add_new_cust_con = sqlite3.connect('CarRental.db')
    add_new_cust_cur = add_new_cust_con.cursor()

    add_new_cust_cur.execute("INSERT INTO Customer VALUES (:cust_id, :cust_name, :phone_number)",
                             {
                                 'cust_id': None,
                                 'cust_name': customer_name.get(),
                                 'phone_number': phone_number.get()
                             })

    add_new_cust_con.commit()
    add_new_cust_con.close()

# Function for seeing customer records
def see_cust():
    sc_con = sqlite3.connect('CarRental.db')
    sc_cur = sc_con.cursor()

    sc_window = Tk()
    sc_window.title('Customers in Database')
    sc_window.geometry("450x750")

    sc_cur.execute("SELECT CustID, Name, Phone FROM Customer")

    output_records = sc_cur.fetchall()
    row_count = 0
    print_record = "CustomerID".ljust(30) + "CustomerName".ljust(30) + "Phone".ljust(30) + "\n\n"

    for output_record in output_records:
        print_record += str(output_record[0]).ljust(30) + str(output_record[1]).ljust(30) + str(output_record[2]).ljust(
            30) + "\n"
        row_count += 1

    iq_label = Label(sc_window, text=print_record)

    iq_label.grid(row=1, column=0, columnspan=3)

    rc = "Row(s) returned: " + str(row_count)
    rc_label = Label(sc_window, text=rc.ljust(20))
    rc_label.grid(row=2, column=0)

    sc_con.commit()
    sc_con.close()


# Function for adding new vehicle
def add_new_vehicle():
    add_new_vehicle_con = sqlite3.connect('CarRental.db')
    add_new_vehicle_cur = add_new_vehicle_con.cursor()

    add_new_vehicle_cur.execute("INSERT INTO Vehicle VALUES (:vehicle_id, :desc, :year, :type, :category)",
                                {
                                    'vehicle_id': get_vehicle_id.get(),
                                    'desc': get_vehicle_desc.get(),
                                    'year': get_vehicle_year.get(),
                                    'type': get_vehicle_type.get(),
                                    'category': get_vehicle_category.get()
                                })

    add_new_vehicle_con.commit()
    add_new_vehicle_con.close()

# Function for seeing vehicle records
def see_vehicle():
    sv_con = sqlite3.connect('CarRental.db')
    sv_cur = sv_con.cursor()

    sv_window = Tk()
    sv_window.title('Vehicles in Database')
    sv_window.geometry("650x1000")

    # scroll = Scrollbar(sv_window, orient="vertical")
    # scroll.pack(side="right", fill="y")

    sv_cur.execute("SELECT VehicleID, Description, Year, Type, Category FROM Vehicle")

    output_records = sv_cur.fetchall()
    row_count = 0
    print_record = "VehicleID".ljust(30) + "Description".ljust(30) + "Year".ljust(30) + "Type".ljust(
        30) + "Category".ljust(30) + "\n\n"

    for output_record in output_records:
        print_record += str(output_record[0]).ljust(30) + str(output_record[1]).ljust(30) + str(output_record[2]).ljust(
            30) + str(output_record[3]).ljust(30) + str(output_record[4]).ljust(30) + "\n"
        row_count += 1

    iq_label = Label(sv_window, text=print_record)

    iq_label.grid(row=1, column=0, columnspan=3)

    rc = "Row(s) returned: " + str(row_count)
    rc_label = Label(sv_window, text=rc.ljust(20))
    rc_label.grid(row=2, column=0)

    sv_con.commit()
    sv_con.close()


# Function for adding a new rental record
def add_new_rental():
    add_new_rental_con = sqlite3.connect("CarRental.db")
    add_new_rental_cur = add_new_rental_con.cursor()

    rental_VIN = get_rental_vehicle_id.get()
    # get list of unavailable cars
    add_new_rental_cur.execute(
        "SELECT Rental.VehicleID FROM Rental JOIN Vehicle ON Rental.VehicleID = Vehicle.VehicleID WHERE Rental.Returned = 0")
    unavaible_cars = add_new_rental_cur.fetchall()

    if rental_VIN != "":

        # compare user's VIN to unavailable cars
        for each_record in unavaible_cars:
            if rental_VIN == str(each_record[0]):
                print("Car is unavailable")
                return

        add_new_rental_cur.execute(
            "INSERT INTO Rental VALUES(:cust_id, :vin, :start_date, :order_date, :rental_type, :qty, :return_date, :total_amount, :payment_date, :return_status)",
            {
                'cust_id': get_rental_custid.get(),
                'vin': rental_VIN,
                'start_date': get_rental_start_date.get(),
                'order_date': get_rental_order_date.get(),
                'rental_type': get_rental_rental_type.get(),
                'qty': get_rental_qty.get(),
                'return_date': get_rental_return_date.get(),
                'total_amount': get_rental_total_amount.get(),
                'payment_date': get_rental_payment_date.get(),
                'return_status': 0
            })
        print("Added Successfully!")
    else:
        print("Please enter VIN")

    add_new_rental_con.commit()
    add_new_rental_con.close()

# Function for seeing available cars for rental
def available_cars():
    ac_con = sqlite3.connect("CarRental.db")
    ac_cur = ac_con.cursor()

    ac_cur.execute("DROP VIEW Unavailable_Cars")
    ac_cur.execute(
        "CREATE VIEW Unavailable_Cars AS SELECT Rental.VehicleID FROM Rental JOIN Vehicle ON Rental.VehicleID = Vehicle.VehicleID WHERE Rental.Returned = 0")
    ac_cur.execute(
        "SELECT Vehicle.VehicleID FROM Vehicle WHERE Vehicle.VehicleID NOT IN (SELECT Unavailable_Cars.VehicleID FROM Unavailable_Cars)")
    unavailable_cars_vin = ac_cur.fetchall()
    ac_cur.execute(
        "SELECT Vehicle.Description FROM Vehicle WHERE Vehicle.VehicleID NOT IN (SELECT Unavailable_Cars.VehicleID FROM Unavailable_Cars)")
    unavailable_cars_desc = ac_cur.fetchall()
    ac_cur.execute(
        "SELECT  Vehicle.Type FROM Vehicle WHERE Vehicle.VehicleID NOT IN (SELECT Unavailable_Cars.VehicleID FROM Unavailable_Cars)")
    unavailable_cars_type = ac_cur.fetchall()
    ac_cur.execute(
        "SELECT Vehicle.Category FROM Vehicle WHERE Vehicle.VehicleID NOT IN (SELECT Unavailable_Cars.VehicleID FROM Unavailable_Cars)")
    unavailable_cars_category = ac_cur.fetchall()

    ac_window = Tk()
    ac_window.title("Cars Available for Rental")
    ac_window.geometry("450x450")

    # VIN
    print = ''
    for a in unavailable_cars_vin:
        print += str(a[0]) + "\n"
    print_all = Label(ac_window, text=print)
    print_all.grid(row=0, column=0)

    # Descriptions
    print = ''
    for a in unavailable_cars_desc:
        print += str(a[0]) + "\n"
    print_all = Label(ac_window, text=print)
    print_all.grid(row=0, column=1)

    # Type
    print = ''
    for a in unavailable_cars_type:
        print += str(a[0]) + "\n"
    print_all = Label(ac_window, text=print)
    print_all.grid(row=0, column=2, padx=20)

    # Category
    print = ''
    for a in unavailable_cars_category:
        print += str(a[0]) + "\n"
    print_all = Label(ac_window, text=print)
    print_all.grid(row=0, column=3, padx=20)

    ac_con.commit()
    ac_con.close()


# Function that calculates amount owed and updates returned rentals
def rental_return():
    rental_return_con = sqlite3.connect("CarRental.db")
    rental_return_cur = rental_return_con.cursor()

    return_window = Tk()
    return_window.title('Return Information')
    return_window.geometry("400x400")

    returnDate = getReturnByDate.get()
    custName = getReturnByName.get()
    vehicleVIN = getReturnByVIN.get()
    vehicle = getReturnByVehicle.get()
    type = getReturnByType.get()
    category = getReturnByCategory.get()

    if returnDate != "":
        rental_return_cur.execute("SELECT SUM(RentalBalance) FROM vRentalInfo WHERE ReturnDate = ?", (returnDate,))
    elif custName != "":
        rental_return_cur.execute("SELECT SUM(RentalBalance) FROM vRentalInfo WHERE CustomerName = ?", (custName,))
    elif vehicleVIN != "":
        rental_return_cur.execute("SELECT SUM(RentalBalance) FROM vRentalInfo WHERE VIN = ?", (vehicleVIN,))
    elif vehicle != "":
        rental_return_cur.execute("SELECT SUM(RentalBalance) FROM vRentalInfo WHERE Vehicle = ?", (vehicle,))
    elif type != "":
        rental_return_cur.execute("SELECT SUM(RentalBalance) FROM vRentalInfo WHERE Type = ?", (type,))
    elif category != "":
        rental_return_cur.execute("SELECT SUM(RentalBalance) FROM vRentalInfo WHERE Category = ?", (category,))

    rental_return_con.commit()
    rental_return_con.close()

# Function for searching customer in vRentalInfo view
def search_cust():
    search_cust_con = sqlite3.connect('CarRental.db')
    search_cust_cur = search_cust_con.cursor()
    ID = search_ID.get()
    name = search_name.get()

    search_cust_window = Tk()
    search_cust_window.title("Customer Search in vRentalInfo")
    search_cust_window.geometry("450x450")

    if name == "" and ID == "":
        search_cust_cur.execute(
            "SELECT CustomerID, CustomerName, SUM(RentalBalance) as 'Rental Balance' FROM vRentalInfo GROUP BY CustomerID, CustomerName")
    elif name != "" and ID == "":
        search_cust_cur.execute(
            "SELECT CustomerID, CustomerName, SUM(RentalBalance) as 'Rental Balance' FROM vRentalInfo WHERE CustomerName LIKE ? GROUP BY CustomerID, CustomerName",
            ('%' + name + '%',))
    elif name == "" and ID != "":
        search_cust_cur.execute(
            "SELECT CustomerID, CustomerName, SUM(RentalBalance) as 'Rental Balance' FROM vRentalInfo WHERE CustomerID = ? GROUP BY CustomerID, CustomerName",
            (ID,))
    else:
        search_cust_cur.execute(
            "SELECT CustomerID, CustomerName, SUM(RentalBalance) as 'Rental Balance' FROM vRentalInfo WHERE CustomerID = ? AND CustomerName LIKE ? GROUP BY CustomerID, CustomerName",
            (ID, '%' + name + '%',))
    output_records = search_cust_cur.fetchall()
    row_count = 0
    print_record = "CustomerID".ljust(30) + "CustomerName".ljust(30) + "Rental Balance".ljust(30) + "\n\n"

    for output_record in output_records:
        print_record += str(output_record[0]).ljust(30) + str(output_record[1]).ljust(30) + "$" + str(
            output_record[2]).ljust(30) + "\n"
        row_count += 1

    iq_label = Label(search_cust_window, text=print_record)

    iq_label.grid(row=1, column=0, columnspan=3)

    rc = "Row(s) returned: " + str(row_count)
    rc_label = Label(search_cust_window, text=rc.ljust(20))
    rc_label.grid(row=2, column=0)

    search_cust_con.commit()
    search_cust_con.close()


# Function for searching vehicle in vRentalInfo view
def search_vehicle():
    search_vehicle_con = sqlite3.connect('CarRental.db')
    search_vehicle_cur = search_vehicle_con.cursor()
    VIN = search_VIN.get()
    desc = search_desc.get()

    search_vehicle_window = Tk()
    search_vehicle_window.title("Vehicle Search in vRentalInfo")
    search_vehicle_window.geometry("450x450")

    if VIN == "" and desc == "":
        search_vehicle_cur.execute(
            "SELECT VIN, Vehicle, round(AVG(OrderAmount/TotalDays), 2)  as 'AVG Daily Price' FROM vRentalInfo GROUP BY VIN, Vehicle")
    elif desc != "" and VIN == "":
        search_vehicle_cur.execute(
            "SELECT VIN, Vehicle, round(AVG(OrderAmount/TotalDays), 2) as 'AVG Daily Price' FROM vRentalInfo WHERE Vehicle LIKE ? GROUP BY VIN, Vehicle",
            ('%' + desc + '%',))
    elif desc == "" and VIN != "":
        search_vehicle_cur.execute(
            "SELECT VIN, Vehicle, round(AVG(OrderAmount/TotalDays), 2) as 'AVG Daily Price' FROM vRentalInfo WHERE VIN = ? GROUP BY VIN, Vehicle",
            (VIN,))
    else:
        search_vehicle_cur.execute(
            "SELECT VIN, Vehicle, round(AVG(OrderAmount/TotalDays), 2) as 'AVG Daily Price' FROM vRentalInfo WHERE Vehicle LIKE ? AND VIN = ? GROUP BY VIN, Vehicle",
            (VIN, '%' + desc + '%',))
    output_records = search_vehicle_cur.fetchall()
    row_count = 0

    print_record = "VIN".ljust(40) + "Vehicle Description".ljust(40) + "AVG Daily Price".ljust(40) + "\n\n"

    for output_record in output_records:
        print_record += str(output_record[0]).strip().ljust(40) + str(output_record[1]).strip().ljust(40) + "$" + str(
            output_record[2]).strip().ljust(40) + "\n"
        row_count += 1

    iq_label = Label(search_vehicle_window, text=print_record)
    iq_label.grid(row=1, column=0, columnspan=3)

    rc = "Row(s) returned: " + str(row_count)
    rc_label = Label(search_vehicle_window, text=rc.ljust(20))
    rc_label.grid(row=2, column=0)

    search_vehicle_con.commit()
    search_vehicle_con.close()


##### GUI Window Designs #####

# Window for entering new customer info
req1 = Label(root, text='\tAdd New Customer:', font='Arial 10 bold')
req1.grid(row=1, column=0)
name_label = Label(root, text='Name:')
name_label.grid(row=2, column=0)
customer_name = Entry(root, width=30)
customer_name.grid(row=2, column=1)

phone_number_label = Label(root, text='Phone Number: ')
phone_number_label.grid(row=3, column=0)
phone_number = Entry(root, width=30)
phone_number.grid(row=3, column=1)

input_qry_btn = Button(root, text='Add New Customer', command=add_new_cust)
input_qry_btn.grid(row=4, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

see_customers_btn = Button(root, text='See Customers', command=see_cust)
see_customers_btn.grid(row=4, column=3, columnspan=2, padx=10, pady=10, ipadx=50)

# Window for adding new vehicle info
req2 = Label(root, text='\tAdd New Vehicle:', font='Arial 10 bold')
req2.grid(row=6, column=0)
vehicle_label = Label(root, text='Vehicle ID: ')
vehicle_label.grid(row=7, column=0)
get_vehicle_id = Entry(root, width=30)
get_vehicle_id.grid(row=7, column=1)

vehicle_desc_label = Label(root, text='Description: ')
vehicle_desc_label.grid(row=8, column=0)
get_vehicle_desc = Entry(root, width=30)
get_vehicle_desc.grid(row=8, column=1)

vehicle_year_label = Label(root, text='Year: ')
vehicle_year_label.grid(row=9, column=0)
get_vehicle_year = Entry(root, width=30)
get_vehicle_year.grid(row=9, column=1)

vehicle_type_label = Label(root, text='Type(1-6): ')
vehicle_type_label.grid(row=10, column=0)
get_vehicle_type = Entry(root, width=30)
get_vehicle_type.grid(row=10, column=1)

vehicle_category_label = Label(root, text='Category(0||1): ')
vehicle_category_label.grid(row=11, column=0)
get_vehicle_category = Entry(root, width=30)
get_vehicle_category.grid(row=11, column=1)

add_car_btn = Button(root, text='Add a new a car', command=add_new_vehicle)
add_car_btn.grid(row=12, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

see_vehicles_btn = Button(root, text='See Vehicles', command=see_vehicle)
see_vehicles_btn.grid(row=12, column=3, columnspan=2, padx=10, pady=10, ipadx=50)

# Window for adding new rental info
req3 = Label(root, text='\tAdd New Rental:', font='Arial 10 bold')
req3.grid(row=15, column=0)
rental_custid = Label(root, text='CustomerID: ')
rental_custid.grid(row=16, column=0)
get_rental_custid = Entry(root, width=30)
get_rental_custid.grid(row=16, column=1)

rental_vehicle_id = Label(root, text='Vehicle ID: ')
rental_vehicle_id.grid(row=17, column=0)
get_rental_vehicle_id = Entry(root, width=30)
get_rental_vehicle_id.grid(row=17, column=1)

rental_start_date = Label(root, text='StartDate: ')
rental_start_date.grid(row=18, column=0)
get_rental_start_date = Entry(root, width=30)
get_rental_start_date.grid(row=18, column=1)

rental_order_date = Label(root, text='OrderDate: ')
rental_order_date.grid(row=19, column=0)
get_rental_order_date = Entry(root, width=30)
get_rental_order_date.grid(row=19, column=1)

rental_rental_type = Label(root, text='Rental Type: ')
rental_rental_type.grid(row=16, column=2)
get_rental_rental_type = Entry(root, width=30)
get_rental_rental_type.grid(row=16, column=3)

rental_qty = Label(root, text='Quantity: ')
rental_qty.grid(row=17, column=2)
get_rental_qty = Entry(root, width=30)
get_rental_qty.grid(row=17, column=3)

rental_return_date = Label(root, text='Return Date: ')
rental_return_date.grid(row=18, column=2)
get_rental_return_date = Entry(root, width=30)
get_rental_return_date.grid(row=18, column=3)

rental_total_amount = Label(root, text='Total Amount: ')
rental_total_amount.grid(row=19, column=2)
get_rental_total_amount = Entry(root, width=30)
get_rental_total_amount.grid(row=19, column=3)

rental_payment_date = Label(root, text='Payment Date: ')
rental_payment_date.grid(row=20, column=0)
get_rental_payment_date = Entry(root, width=30)
get_rental_payment_date.grid(row=20, column=1)

add_rental_btn = Button(root, text='Add new rental', command=add_new_rental)
add_rental_btn.grid(row=21, column=3, columnspan=2, padx=10, pady=10, ipadx=50)

see_rental_btn = Button(root, text='See available cars', command=available_cars)
see_rental_btn.grid(row=21, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

# Window for searching customer in vRentalInfo view
req5a = Label(root, text='\tSearch Customer in vRentalInfo:', font='Arial 10 bold')
req5a.grid(row=27, column=0)
search_viewID = Label(root, text='CustID: ')
search_viewID.grid(row=28, column=0)
search_viewName = Label(root, text='Name: ')
search_viewName.grid(row=29, column=0)

search_ID = Entry(root, width=30)
search_ID.grid(row=28, column=1)
search_name = Entry(root, width=30)
search_name.grid(row=29, column=1)

search_cust_btn = Button(root, text='Search Customer in vRentalInfo', command=search_cust)
search_cust_btn.grid(row=30, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

# Window for searching vehicle in vRentalInfo view
req5b = Label(root, text='\tSearch Vehicle in vRentalInfo:', font='Arial 10 bold')
req5b.grid(row=32, column=0)
search_viewVIN = Label(root, text='VIN: ')
search_viewVIN.grid(row=33, column=0)
search_VDesc = Label(root, text='Description: ')
search_VDesc.grid(row=34, column=0)

search_VIN = Entry(root, width=30)
search_VIN.grid(row=33, column=1)
search_desc = Entry(root, width=30)
search_desc.grid(row=34, column=1)

search_vehicle_btn = Button(root, text='Search Vehicle in vRentalInfo', command=search_vehicle)
search_vehicle_btn.grid(row=35, column=1, columnspan=2, padx=10, pady=10, ipadx=50)

# Window for searching rental by return date
returnByDate = Label(root, text='Rental by return date: ')
returnByDate.grid(row=36, column=0)
getReturnByDate = Entry(root, width=30)
getReturnByDate.grid(row=36, column=1)

returnByName = Label(root, text='Rental by customer name: ')
returnByName.grid(row=36, column=2)
getReturnByName = Entry(root, width=30)
getReturnByName.grid(row=36, column=3)

returnByVIN = Label(root, text='Rental by VIN: ')
returnByVIN.grid(row=37, column=0)
getReturnByVIN = Entry(root, width=30)
getReturnByVIN.grid(row=37, column=1)

returnByVehicle = Label(root, text='Rental by Vehicle: ')
returnByVehicle.grid(row=37, column=2)
getReturnByVehicle = Entry(root, width=30)
getReturnByVehicle.grid(row=37, column=3)

returnByType = Label(root, text='Rental by Type: ')
returnByType.grid(row=38, column=0)
getReturnByType = Entry(root, width=30)
getReturnByType.grid(row=38, column=1)

returnByCategory = Label(root, text='Rental by Category: ')
returnByCategory.grid(row=38, column=2)
getReturnByCategory = Entry(root, width=30)
getReturnByCategory.grid(row=38, column=3)

rentalReturnButton = Button(root, text='Rental Return Info', command=rental_return)
rentalReturnButton.grid(row=39, column=1, columnspan=2, padx=10, pady=10, ipadx=30)

# shows the GUI
root.mainloop()
