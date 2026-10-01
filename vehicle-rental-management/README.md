Vehicle Rental Management System

Overview

A Python application for managing vehicles and customer rentals for a rental company.

Features

* Add a new vehicle
* View all available vehicles
* Rent a vehicle
* Return a vehicle
* Search rental details using Customer ID
* Display all rented vehicles
* Generate a rental summary report

Vehicle Details

* Vehicle ID
* Vehicle Name
* Vehicle Type
* Rental Price Per Day
* Availability Status

Supported vehicle types:

* Bike
* Car
* SUV

Rental Calculation

Total Rental Amount = Rental Price Per Day × Number of Rental Days

A 10% discount is applied when the rental period is 7 days or more.

Business Rules

* Vehicle ID must be unique.
* A rented vehicle cannot be rented again until it is returned.
* Rental days must be greater than 0.
* Customer ID must be unique for each active rental.
* Vehicle price must be greater than 0.
* Customer name cannot be empty.
* Vehicle type must be Bike, Car, or SUV.
* Vehicle must be available before renting.

Exception Handling

The application handles:

* Duplicate Vehicle ID
* Invalid Vehicle ID
* Invalid Customer ID
* Vehicle not available
* Invalid rental days
* Empty inputs

How to Run

python vehicle_rental.py

What I Learned

I learned how to build a vehicle rental management system using Python lists, dictionaries, functions, validations, business rules, exception handling, and rental calculations. I also learned how to manage vehicle availability and apply discounts based on rental duration.