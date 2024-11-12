from models import Service, db, Professional, Customer, User, ServiceRequest
from models import get_all, get_with_id, delete_with_id
from sqlalchemy import insert, select, delete
from datetime import datetime

def create_dummy_services():
    services = [
        {
            "name": "Service A (db)",
            "price": 1000,
            "timereq": 10,
            "description": "Description for Service A (db)"
        },
        {
            "name": "Service B (db)",
            "price": 1200,
            "timereq": 20,
            "description": "Description for Service B (db)"
        },
        {
            "name": "Service C (db)",
            "price": 1400,
            "timereq": 30,
            "description": "Description for Service C (db)"
        },
        {
            "name": "Service D (db)",
            "price": 1600,
            "timereq": 40,
            "description": "Description for Service D (db)"
        },
        {
            "name": "Service E (db)",
            "price": 1800,
            "timereq": 50,
            "description": "Description for Service E (db)"
        },
        {
            "name": "Service F (db)",
            "price": 2000,
            "timereq": 60,
            "description": "Description for Service F (db)"
        },
    ]
    print()
    print("Creating Services:")

    for kw in services:
        service = Service(**kw)
        db.session.add(service)
    db.session.commit()


def create_dummy_profs():
    profs = [
        {
            "user": {
                "fullname": "Professional A",
                "username": "profA",
                "email": "profa@gmail.com",
                "password": "97532468",
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543211",
                "address": "Address for A",
                "pincode": "110025",
                "experience": 5,
                "description": "Description for A",
                "service_id": 1
            }
        },
        {
            "user": {
                "fullname": "Professional B",
                "username": "profB",
                "email": "profb@gmail.com",
                "password": "97532468",
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543212",
                "address": "Address for B",
                "pincode": "110026",
                "experience": 6,
                "description": "Description for B",
                "service_id": 2,
            }
        },
        {
            "user": {
                "fullname": "Professional C",
                "username": "profC",
                "email": "profc@gmail.com",
                "password": "97532468",
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543213",
                "address": "Address for C",
                "pincode": "110027",
                "experience": 7,
                "description": "Description for C",
                "service_id": 3,
                "approval": "APPROVED",
            }
        },
        {
            "user": {
                "fullname": "Professional D",
                "username": "profD",
                "email": "profd@gmail.com",
                "password": "97532468",
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543214",
                "address": "Address for D",
                "pincode": "110028",
                "experience": 8,
                "description": "Description for D",
                "service_id": 4,
                "approval": "APPROVED",
            }
        },
        {
            "user": {
                "fullname": "Professional E",
                "username": "profE",
                "email": "profe@gmail.com",
                "password": "97532468",
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543215",
                "address": "Address for E",
                "pincode": "110029",
                "experience": 9,
                "description": "Description for E",
                "service_id": 5,
                "approval": "REJECTED",
            }
        },
        {
            "user": {
                "fullname": "Professional F",
                "username": "profF",
                "email": "proff@gmail.com",
                "password": "97532468",
                "role": "PROFESSIONAL",
            },
            "prof": {
                "contact": "9876543216",
                "address": "Address for F",
                "pincode": "110030",
                "experience": 10,
                "description": "Description for F",
                "service_id": 6,
                "approval": "REJECTED",
            }
        }
    ]
    print()
    print("Creating Professionals:")

    for kw in profs:
        user = User(**kw['user'])
        prof = Professional(**kw['prof'])
        prof.user = user
        db.session.add(prof)
    db.session.commit()


def create_dummy_custs():
    custs = [
        {
            "user": {
                "fullname": "Customer A",
                "username": "custA",
                "email": "custa@gmail.com",
                "password": "97532468",
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543210",
                "address": "Address for Customer A",
                "pincode": "110025",
            }
        },
        {
            "user": {
                "fullname": "Customer B",
                "username": "custB",
                "email": "custb@gmail.com",
                "password": "97532468",
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543220",
                "address": "Address for Customer B",
                "pincode": "110026",
            }
        },
        {
            "user": {
                "fullname": "Customer C",
                "username": "custC",
                "email": "custc@gmail.com",
                "password": "97532468",
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543230",
                "address": "Address for Customer C",
                "pincode": "110027",
            }
        },
        {
            "user": {
                "fullname": "Customer D",
                "username": "custD",
                "email": "custd@gmail.com",
                "password": "97532468",
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543240",
                "address": "Address for Customer D",
                "pincode": "110028",
            }
        },
        {
            "user": {
                "fullname": "Customer E",
                "username": "custE",
                "email": "custe@gmail.com",
                "password": "97532468",
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543250",
                "address": "Address for Customer E",
                "pincode": "110029",
                "status": "BLOCKED",
            }
        },
        {
            "user": {
                "fullname": "Customer F",
                "username": "custF",
                "email": "custf@gmail.com",
                "password": "97532468",
                "role": "CUSTOMER",
            },
            "cust": {
                "contact": "9876543260",
                "address": "Address for Customer F",
                "pincode": "110030",
                "status": "BLOCKED",
            }
        },
    ]
    print()
    print("Creating Customers:")

    for kw in custs:
        user = User(**kw['user'])
        cust = Customer(**kw['cust'])
        cust.user = user
        db.session.add(cust)
    db.session.commit()

def create_dummy_admin():
    admin = {
        "fullname": "Admin",
        "username": "admin",
        "email": "admin@hhs.org",
        "password": "97532468",
        "role": "ADMIN",
    }
    print()
    print("Creating Admin:")

    admin = User(**admin)
    db.session.add(admin)
    db.session.commit()

def create_dummy_requests():
    requests = [
        {
            "service_id": 1,
            "customer_id": 1,
        },
        {
            "service_id": 1,
            "customer_id": 1,
        },
        {
            "service_id": 1,
            "customer_id": 2,
        },
        {
            "service_id": 1,
            "customer_id": 3,
        },
        {
            "service_id": 1,
            "customer_id": 4,
        },
        {
            "service_id": 1,
            "customer_id": 1,
            "professional_id": 1,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "customer_id": 1,
            "professional_id": 2,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "customer_id": 3,
            "professional_id": 1,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "customer_id": 4,
            "professional_id": 1,
            "status": "ASSIGNED",
        },
        {
            "service_id": 3,
            "customer_id": 3,
            "professional_id": 3,
            "status": "ASSIGNED",
        },
        {
            "service_id": 4,
            "customer_id": 4,
            "professional_id": 4,
            "status": "ASSIGNED",
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 1,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 2,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 5,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 1,
            "professional_id": 1,
            "customer_id": 6,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 5,
            "professional_id": 5,
            "customer_id": 5,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        },
        {
            "service_id": 6,
            "professional_id": 6,
            "customer_id": 6,
            "status": "CLOSED",
            "rating": 4,
            "remarks": "Remarks for this service",
            "completed": datetime.now(),
        }
    ]
    print()
    print("Creating Service Requests:")
    for kw in requests:
        request = ServiceRequest(**kw)
        db.session.add(request)
    db.session.commit()


def get_all_services():
    services = get_all(Service)
    print()
    print("Getting All Services:")
    for service in services:
        print(f"{service.id}, {service.name}, {service.created}")

def get_all_profs():
    profs = get_all(Professional)
    print()
    print("Getting All Professionals:")
    for prof in profs:
        print(f"{prof.id}, {prof.user.fullname}, {prof.approval}, {prof.user.role}, {prof.created}")

def get_all_custs():
    custs = get_all(Customer)
    print()
    print("Getting All Customers:")
    for cust in custs:
        print(f"{cust.id}, {cust.user.fullname}, {cust.user.role}, {cust.created}")

def get_admin():
    sql = select(User).filter_by(fullname="Admin")
    admin = db.session.scalars(sql).first()
    print()
    print("Getting Admin:")
    if admin:
        print(f"{admin.id}, {admin.fullname}, {admin.email}, {admin.role}")

def get_all_users():
    users = get_all(User)
    print()
    print("Getting All Users:")
    for user in users:
        print(f"{user.id}, {user.fullname}, {user.username}, {user.email}")

def get_all_requests():
    requests = get_all(ServiceRequest)
    print()
    print("Getting All Service Requests:")
    for req in requests:
        print(f"{req.id}, {req.service_id}, {req.professional_id}, {req.status}")



def rm_all_services():
    print()
    print("Removing All Services:")
    sql = delete(Service)
    db.session.execute(sql)
    db.session.commit()


def rm_all_profs():
    print()
    print("Removing All Professionals:")
    sql = delete(Professional)
    db.session.execute(sql)
    db.session.commit()


def rm_all_custs():
    print()
    print("Removing All Customers:")
    sql = delete(Customer)
    db.session.execute(sql)
    db.session.commit()


def rm_admin():
    print()
    print("Removing Admin:")
    sql = delete(User).filter_by(username="admin")
    db.session.execute(sql)
    db.session.commit()

def rm_all_users():
    print()
    print("Removing All Users:")
    sql = delete(User)
    db.session.execute(sql)
    db.session.commit()

def rm_all_requests():
    print()
    print("Removing All Service Requests:")
    sql = delete(ServiceRequest)
    db.session.execute(sql)
    db.session.commit()

def create_dummy_data():
    create_dummy_admin()
    create_dummy_services()
    create_dummy_profs()
    create_dummy_custs()
    create_dummy_requests()

def get_data():
    get_all_services()
    get_all_profs()
    get_all_custs()
    get_admin()
    get_all_users()
    get_all_requests()

def rm_data():
    rm_all_services()
    rm_all_profs()
    rm_all_custs()
    rm_admin()
    rm_all_users()
    rm_all_requests()

# rm_data()
# create_dummy_admin()
get_data()
