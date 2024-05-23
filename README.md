# Vendor_management_system
Django Vendor Management System
This project is a Vendor Management System built using Django and Django REST Framework. It allows users to manage vendor profiles, track purchase orders, and analyze vendor performance metrics.

Core Features
  1.	Vendor Profile Management:
    •	Create, retrieve, update, and delete vendor profiles.
    •	Store vendor information including name, contact details, address, and a unique vendor code.
    •	Calculate and track performance metrics such as on-time delivery rate, quality rating average, and fulfillment rate.

  2.	Purchase Order Tracking:
    •	Create, retrieve, update, and delete purchase orders.
    •	Track purchase order details such as PO number, vendor reference, order date, items, quantity, and status.
    •	Automatically update vendor performance metrics based on purchase order interactions.

  3.	Vendor Performance Evaluation:
    •	Calculate and analyze historical performance metrics for vendors.
    •	Metrics include on-time delivery rate, quality rating average, average response time, and fulfillment rate.
    •	Real-time updates of performance metrics triggered by purchase order actions.

Installation and Setup
1.	Clone the Repository:
   git clone https://github.com/rswarn01/Vendor_management_system.git
    cd vendor_management
3.	Create Virtual Environment:
   pipenv install (all the dependencies will be downloaded from piplock file)
4.	Activate Virtual Environment:
   pipenv shell
5.	Run Migrations:
   python manage.py migrate 
6.	Create Superuser (Optional):
   python manage.py createsuperuser 
7.	Run Development Server:
   python manage.py runserver
8. API Documentation
   http://127.0.0.1:8000/swagger/
10. run test file
   python manage.py test vendors.tests.test_api
11.	Access the Application:
  •	Open a web browser and go to http://127.0.0.1:8000/admin to access the Django admin interface.
  •	Use the superuser credentials created earlier to log in and access the admin dashboard.


API Endpoints
Vendor Endpoints
1. GET /api/vendors/: List all vendors.
2. POST /api/vendors/: Create a new vendor.
3. GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
4. PUT /api/vendors/{vendor_id}/: Update a vendor's details.
5. DELETE /api/vendors/{vendor_id}/: Delete a vendor.
6. GET /api/vendors/{vendor_id}/performance/: Retrieve a vendor's performance metrics.
  
Purchase Order Endpoints
1. GET /api/purchase_orders/: List all purchase orders.
2. POST /api/purchase_orders/: Create a new purchase order.
3. GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
4. PUT /api/purchase_orders/{po_id}/: Update a purchase order.
5. DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
6. POST /api/purchase_orders/{po_id}/acknowledge/: Acknowledge a purchase order.

Technologies Used
  •	Django
  •	Django REST Framework
  •	SQLite (default database)
  •	Python

Added postman collection for ease of use, also added swagger api documentation.
