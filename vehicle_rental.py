vehicles = []
rentals = []


def add_vehicle():
    vehicle_id = input("Enter Vehicle ID: ").strip()
    vehicle_name = input("Enter Vehicle Name: ").strip()
    vehicle_type = input("Enter Vehicle Type (Bike/Car/SUV): ").strip()
    rental_price = float(input("Enter Rental Price Per Day: "))

    if not vehicle_id or not vehicle_name or not vehicle_type:
        raise ValueError("Inputs cannot be empty")

    if vehicle_type not in ["Bike", "Car", "SUV"]:
        raise ValueError("Invalid vehicle type")

    if rental_price <= 0:
        raise ValueError("Vehicle price must be greater than 0")

    for vehicle in vehicles:
        if vehicle["vehicle_id"] == vehicle_id:
            raise ValueError("Duplicate Vehicle ID")

    vehicle = {
        "vehicle_id": vehicle_id,
        "vehicle_name": vehicle_name,
        "vehicle_type": vehicle_type,
        "rental_price": rental_price,
        "available": True,
    }

    vehicles.append(vehicle)

    print("Vehicle added successfully!")

def view_available_vehicles():
    print("\nAvailable Vehicles:")

    for vehicle in vehicles:
        if vehicle["available"]:
            print(vehicle)

def rent_vehicle():
    customer_id = input("Enter Customer ID: ").strip()
    customer_name = input("Enter Customer Name: ").strip()
    vehicle_id = input("Enter Vehicle ID: ").strip()
    rental_days = int(input("Enter Number of Rental Days: "))

    if not customer_id or not customer_name or not vehicle_id:
        raise ValueError("Inputs cannot be empty")

    if rental_days <= 0:
        raise ValueError("Rental days must be greater than 0")

    for rental in rentals:
        if rental["customer_id"] == customer_id:
            raise ValueError("Customer ID already has an active rental")

    vehicle = None

    for item in vehicles:
        if item["vehicle_id"] == vehicle_id:
            vehicle = item
            break

    if vehicle is None:
        raise ValueError("Invalid Vehicle ID")

    if not vehicle["available"]:
        raise ValueError("Vehicle not available")

    total_amount = vehicle["rental_price"] * rental_days

    if rental_days >= 7:
        total_amount = total_amount * 0.90

    rental = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "vehicle_id": vehicle_id,
        "rental_days": rental_days,
        "total_amount": total_amount,
    }

    rentals.append(rental)
    vehicle["available"] = False

    print("Vehicle rented successfully!")
    print("Total Rental Amount:", total_amount)

def return_vehicle():
    customer_id = input("Enter Customer ID: ").strip()

    for rental in rentals:
        if rental["customer_id"] == customer_id:
            vehicle_id = rental["vehicle_id"]

            for vehicle in vehicles:
                if vehicle["vehicle_id"] == vehicle_id:
                    vehicle["available"] = True
                    break

            rentals.remove(rental)

            print("Vehicle returned successfully!")
            return

    raise ValueError("Invalid Customer ID")

def search_rental():
    customer_id = input("Enter Customer ID: ").strip()

    for rental in rentals:
        if rental["customer_id"] == customer_id:
            print("Rental Details:")
            print(rental)
            return

    raise ValueError("Invalid Customer ID")

def display_rented_vehicles():
    print("\nRented Vehicles:")

    if not rentals:
        print("No vehicles are currently rented.")
        return

    for rental in rentals:
        print(rental)

def rental_summary():
    print("\nRental Summary Report")

    if not rentals:
        print("No active rentals.")
        return

    total_revenue = 0

    for rental in rentals:
        print(rental)
        total_revenue += rental["total_amount"]

    print("Total Active Rentals:", len(rentals))
    print("Total Rental Amount:", total_revenue)       

try:
    add_vehicle()
    view_available_vehicles()
    rent_vehicle()
    search_rental()
    display_rented_vehicles()
    rental_summary()
    return_vehicle()
    view_available_vehicles()
except ValueError as error:
    print("Error:", error)