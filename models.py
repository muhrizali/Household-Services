from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func, or_, and_
from sqlalchemy import select, delete, func, Integer, String, DateTime, Text, ForeignKey, extract
from typing import List, Optional
from datetime import datetime
from flask_login import UserMixin
from apps import app

# initializing sqlalchemy with flask

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# configure the database, initialize app with the extension
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)


# Define your models here...

# User model; contains all users; admin, professionals and customers
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement="auto")
    fullname: Mapped[str] = mapped_column(String(200))
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    password: Mapped[str] = mapped_column(String(40))

    # roles: "ADMIN", "CUSTOMER", "PROFESSIONAL"
    role: Mapped[str] = mapped_column(String(200))

    def get_prof(self):
        sql = select(Professional).join(User).where(
            Professional.user_id == self.id)
        result = db.session.scalars(sql).first()
        return result

    def get_customer(self):
        sql = select(Customer).join(User).where(Customer.user_id == self.id)
        result = db.session.scalars(sql).first()
        return result

    def username_exists(self):
        sql = select(User).filter_by(username=self.username)
        results = db.session.scalars(sql)
        if len(list(results)):
            return True
        else:
            return False

    def email_exists(self):
        sql = select(User).filter_by(email=self.email)
        results = db.session.scalars(sql)
        if len(list(results)):
            return True
        else:
            return False


class Professional(db.Model):
    __tablename__ = 'professional'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement="auto")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(cascade="all,delete")

    # professional specific fields
    contact: Mapped[str] = mapped_column(String(10), unique=True)
    address: Mapped[str] = mapped_column(Text)
    pincode: Mapped[str] = mapped_column(String(6))
    experience: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)

    # approval status: "PENDING", "APPROVED", "REJECTED"
    approval: Mapped[Optional[str]] = mapped_column(String, default="PENDING")

    # relations (service: required)
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    service: Mapped["Service"] = relationship(back_populates="professionals")

    # date and time related
    created: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now())
    updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())
    
    def get_avg_rating(self):
        sql = select(func.avg(ServiceRequest.rating), func.count()).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.professional_id == self.id,
            ServiceRequest.status == "CLOSED"
        ).group_by(ServiceRequest.service_id)
        result = db.session.execute(sql).first()
        if not result:
            return "No Ratings"
        avg, count = result
        return f"{round(avg, 2)} ({count} ratings)"
    
    def get_avg_float(self):
        sql = select(func.avg(ServiceRequest.rating)).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.professional_id == self.id,
            ServiceRequest.status == "CLOSED"
        ).group_by(ServiceRequest.service_id)
        result = db.session.execute(sql).first()
        print(result)
        if not result:
            return 0
        return result[0]

    def get_new_requests_with_year(self, year):
        sql = select(ServiceRequest).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.status == "REQUESTED",
            extract('year', ServiceRequest.created) == year,
        )
        results = db.session.scalars(sql)
        return results

    def get_new_requests_with_month(self, month):
        sql = select(ServiceRequest).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.status == "REQUESTED",
            extract('month', ServiceRequest.created) == month,
        )
        results = db.session.scalars(sql)
        return results

    def get_new_requests_with_day(self, day):
        sql = select(ServiceRequest).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.status == "REQUESTED",
            extract('day', ServiceRequest.created) == day,
        )
        results = db.session.scalars(sql)
        return results

    def get_new_requests_with_address(self, address):
        query = '%' + address + '%'
        sql = select(ServiceRequest).join(Customer).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.status == "REQUESTED",
            Customer.address.ilike(query),
        )
        results = db.session.scalars(sql)
        return results

    def get_new_requests_with_customer(self, customer):
        query = '%' + customer + '%'
        sql = select(ServiceRequest).join(Customer).join(User).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.status == "REQUESTED",
            User.fullname.ilike(query),
        )
        results = db.session.scalars(sql)
        return results

    def get_new_requests_with_pincode(self, pincode):
        sql = select(ServiceRequest).join(Customer).where(
            ServiceRequest.service_id == self.service_id,
            ServiceRequest.status == "REQUESTED",
            Customer.pincode == pincode,
        )
        results = db.session.scalars(sql)
        return results

    def get_new_requests(self, status):
        sql = select(ServiceRequest).where(ServiceRequest.service_id ==
                                           self.service_id, ServiceRequest.status == status)
        results = db.session.scalars(sql)
        return results

    def get_requests(self, status):
        sql = select(ServiceRequest).where(ServiceRequest.service_id == self.service_id,
                                           ServiceRequest.professional_id == self.id, ServiceRequest.status == status)
        results = db.session.scalars(sql)
        return results

    def contact_exists(self):
        sql = select(Professional).filter_by(contact=self.contact)
        results = db.session.scalars(sql)
        if len(list(results)):
            return True
        else:
            return False

    def is_pending(self):
        return self.approval == "PENDING"

    def is_approved(self):
        return self.approval == "APPROVED"

    def is_rejected(self):
        return self.approval == "REJECTED"


class Customer(db.Model):
    __tablename__ = 'customer'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement="auto")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(cascade="all,delete")

    # customer specific fields
    contact: Mapped[str] = mapped_column(String(10), unique=True)
    address: Mapped[str] = mapped_column(Text)
    pincode: Mapped[str] = mapped_column(String(6))
    # status: "ACTIVE", "BLOCKED"
    status: Mapped[str] = mapped_column(String, default="ACTIVE")

    # relattions
    service_requests: Mapped[List["ServiceRequest"]] = relationship(
        back_populates="customer", cascade="all,delete")

    # date and time related
    created: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now())
    updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())

    def contact_exists(self):
        sql = select(Customer).filter_by(contact=self.contact)
        results = db.session.scalars(sql)
        if len(list(results)):
            return True
        else:
            return False


class Service(db.Model):
    __tablename__ = 'service'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column(Integer)
    timereq: Mapped[Optional[int]] = mapped_column(Integer)  # in hours
    description: Mapped[str] = mapped_column(Text)

    # relations
    professionals: Mapped[List["Professional"]
                          ] = relationship(back_populates="service")

    # date and time related
    created: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now())
    updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())

    def service_exists(self):
        sql = select(Service).filter_by(name=self.name)
        results = db.session.scalars(sql)
        if len(list(results)):
            return True
        else:
            return False


class ServiceRequest(db.Model):
    __tablename__ = 'service_request'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement="auto")

    # relations
    service_id: Mapped[int] = mapped_column(Integer, ForeignKey("service.id"))
    professional_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("professional.id"))

    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship(
        back_populates="service_requests")

    # service requests specific: "REQUESTED", "ASSIGNED", "CLOSED"
    status: Mapped[Optional[str]] = mapped_column(
        String(10), default="REQUESTED")

    rating: Mapped[Optional[int]] = mapped_column(Integer)  # from 1 to 5
    remarks: Mapped[Optional[str]] = mapped_column(Text)

    # date and time related
    completed: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created: Mapped[Optional[datetime]] = mapped_column(
        DateTime, server_default=func.now())
    updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())

    def stars(self):
        if self.rating == 1:
            stars = "⭐"
        elif self.rating == 2:
            stars = "⭐⭐"
        elif self.rating == 3:
            stars = "⭐⭐⭐"
        elif self.rating == 4:
            stars = "⭐⭐⭐⭐"
        elif self.rating == 5:
            stars = "⭐⭐⭐⭐⭐"
        else:
            stars = None
        return stars

    def completed_time(self):
        if self.completed:
            return self.completed.ctime()
        else:
            return None

    def service(self):
        return get_with_id(Service, self.service_id)

    def prof(self):
        return get_with_id(Professional, self.professional_id)


# helpful functions
def get_all(model):
    sql = select(model).order_by(model.id)
    results = db.session.scalars(sql)
    return results


def get_with_id(model, pkid):
    sql = select(model).where(model.id == pkid)
    result = db.session.scalars(sql).first()
    return result


def get_with_filter(model, filter):
    sql = select(model).filter_by(**filter)
    result = db.session.scalars(sql).first()
    return result


def get_all_with_filter(model, filter):
    sql = select(model).filter_by(**filter)
    results = db.session.scalars(sql)
    return results


def delete_with_id(model, id):
    sql = delete(model).filter_by(id=id)
    db.session.execute(sql)
    db.session.commit()


def professional_search(query):
    query = '%' + query + '%'
    sql = select(Professional).join(User).filter(
        or_(
            User.fullname.ilike(query),
            User.email.ilike(query),
            User.username.ilike(query),
            Professional.pincode.ilike(query),
            Professional.approval.ilike(query),
        )
    )
    results = db.session.scalars(sql)
    return results


def customer_search(query):
    query = '%' + query + '%'
    sql = select(Customer).join(User).filter(
        or_(
            User.fullname.ilike(query),
            User.email.ilike(query),
            User.username.ilike(query),
            Customer.pincode.ilike(query),
            Customer.status.ilike(query),
        )
    )
    results = db.session.scalars(sql)
    return results


def service_search(query):
    query = '%' + query + '%'
    sql = select(Service).filter(
        or_(
            Service.name.ilike(query),
            Service.description.ilike(query),
        )
    )
    results = db.session.scalars(sql)
    return results


def request_search(query):
    query = '%' + query + '%'
    sql = select(ServiceRequest).join(Service).filter(
        or_(
            Service.name.ilike(query),
            ServiceRequest.status.ilike(query),
        )
    )
    results = db.session.scalars(sql)
    return results
    # pass


def search(param, query):
    if param == "service":
        results = service_search(query)
    elif param == "professional":
        results = professional_search(query)
    elif param == "customer":
        results = customer_search(query)
    elif param == "request":
        results = request_search(query)
    else:
        results = None
    return results


def all_with(param):
    if param == "service":
        results = get_all(Service)
    elif param == "professional":
        results = get_all(Professional)
    elif param == "customer":
        results = get_all(Customer)
    elif param == "request":
        results = get_all(ServiceRequest)
    else:
        results = None
    return results


# Getting Professionals with parameters

def get_profs_with_param(param, query):
    query = '%' + query + '%'
    results = None
    if param == "prof_name":
        sql = select(Professional).join(User).where(User.fullname.ilike(query))
        results = db.session.scalars(sql)
    elif param == "prof_email":
        sql = select(Professional).join(User).where(User.email.ilike(query))
        results = db.session.scalars(sql)
    elif param == "prof_contact":
        sql = select(Professional).where(Professional.contact.ilike(query))
        results = db.session.scalars(sql)
    elif param == "prof_address":
        sql = select(Professional).where(Professional.address.ilike(query))
        results = db.session.scalars(sql)
    elif param == "prof_pincode":
        sql = select(Professional).where(Professional.pincode.ilike(query))
        results = db.session.scalars(sql)
    return results


# Getting Customers with parameters

def get_custs_with_param(param, query):
    query = '%' + query + '%'
    results = None
    if param == "cust_name":
        sql = select(Customer).join(User).where(User.fullname.ilike(query))
        results = db.session.scalars(sql)
    elif param == "cust_email":
        sql = select(Customer).join(User).where(User.email.ilike(query))
        results = db.session.scalars(sql)
    elif param == "cust_contact":
        sql = select(Customer).where(Customer.contact.ilike(query))
        results = db.session.scalars(sql)
    return results

# Getting Services with parameters
def get_services_with_param(param, query):
    results = None
    if param == "service_name":
        query = '%' + query + '%'
        sql = select(Service).where(Service.name.ilike(query))
        results = db.session.scalars(sql)
    elif param == "service_price":
        sql = select(Service).where(Service.price == query)
        results = db.session.scalars(sql)
    return results

# Getting Service Requests with parameters
def get_requests_with_param(param, query):
    results = None
    query = '%' + query + '%'
    if param == "request_service":
        sql = select(ServiceRequest).join(Service).where(Service.name.ilike(query))
        results = db.session.scalars(sql)
    elif param == "request_customer":
        sql = select(ServiceRequest).join(Customer, ServiceRequest.customer_id == Customer.id).join(User, Customer.user_id == User.id).filter(User.fullname.ilike(query))
        results = db.session.scalars(sql)
    elif param == "request_prof":
        sql = select(ServiceRequest).join(Professional, ServiceRequest.professional_id == Professional.id).join(User, Professional.user_id == User.id).where(User.fullname.ilike(query))
        results = db.session.scalars(sql)
    return results


# create schemas
# with app.app_context():
#     db.create_all()
app.app_context().push()
db.create_all()
