from apps import app
from flask import url_for, render_template, request, redirect, flash
from forms import *
from models import db, User, Professional, Customer, Service, ServiceRequest
from models import get_all, get_with_id, get_with_filter, get_all_with_filter, delete_with_id, search, all_with, get_profs_with_param, get_services_with_param, get_custs_with_param, get_requests_with_param
from sqlalchemy import select
from login import load_user
from flask_login import login_user, logout_user
from time import sleep
from datetime import datetime

# LOGIN, LOGOUT
@app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    # for POST; create form from POST data
    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            sql = select(User).filter_by(email=email, password=password)
            user = db.session.scalars(sql).first()
            if (not user):
                flash("Incorrect email or password")
            elif (user.role == "CUSTOMER"):
                login_user(user)
                return redirect(url_for("customer_home", user_id=user.id))
            elif (user.role == "PROFESSIONAL"):
                login_user(user)
                return redirect(url_for("professional_home", user_id=user.id))
            elif (user.role == "ADMIN"):
                login_user(user)
                return redirect(url_for("admin_home"))
    else:
        # for GET; create empty login form
        form = LoginForm()
    return render_template("login.html", form=form)

# LOGIN:SUCCESS
@app.route("/login/success")
def login_success():
    return render_template("login_success.html")

# LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# REGISTER:CUSTOMER
@app.route("/register/customer", methods=["GET", "POST"])
def customer_register():
    # for POST; create form from POST data
    if request.method == "POST":
        form = CustomerRegisterForm(request.form)
        if form.validate():
            user_data = {
                "fullname": form.fullname.data,
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data,
                "role": form.role.data,
            }
            customer_data = {
                "contact": form.contact.data,
                "address": form.address.data,
                "pincode": form.pincode.data,
            }

            user = User(**user_data)
            customer = Customer(**customer_data)

            if user.email_exists():
                flash("Email already exists. Please try a different Email.")
            elif user.username_exists():
                flash("Username already exists. Please try a different Username.")
            elif customer.contact_exists():
                flash("Contact already exists. Please try a different Contact.")
            else:
                # registeration successful; go to login page
                customer.user = user
                db.session.add(customer)
                db.session.commit()
                return redirect(url_for('register_success'))
    else:
         # for GET; create empty form
         # provide this empty form to template
        form = CustomerRegisterForm()
    return render_template("customer/register.html", form=form)

# REGISTER:PROFESSIONAL
@app.route("/register/professional", methods=["GET", "POST"])
def professional_register():
    # for POST; create form from POST data
    if request.method == "POST":
        form = ProfessionalRegisterForm(request.form)
        if form.validate():
            user_data = {
                "fullname": form.fullname.data,
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data,
                "role": form.role.data,
            }
            prof_data = {
                "contact": form.contact.data,
                "address": form.address.data,
                "pincode": form.pincode.data,

                "experience": form.experience.data,
                "description": form.description.data,
                "service_id": form.service_id.data,
            }
            user = User(**user_data)
            prof = Professional(**prof_data)
            if user.email_exists():
                flash("Email already exists. Please try a different Email.")
            elif user.username_exists():
                flash("Username already exists. Please try a different Username.")
            elif prof.contact_exists():
                flash("Contact already exists. Please try a different Contact.")
            else:
                # registeration successful; go to login page
                prof.user = user
                db.session.add(prof)
                db.session.commit()
                return redirect(url_for('register_success'))
    else:
        # for GET; create empty form
        # provide this empty form to template
        form = ProfessionalRegisterForm()
    return render_template("professional/register.html", form=form)

# REGISTER SUCCESS
@app.route("/register/success")
def register_success():
    return render_template("register_success.html")

# NOT FOUND
# when resource not found
@app.route("/notfound/")
def not_found():
    return render_template("not_found.html"), 404

# RESTRICTED NOTICE
# In case the professional/customer gets blocked
@app.route("/notice/blocked/<user_id>")
def notice_blocked(user_id):
    user = get_with_id(User, user_id)
    if not user:
        return redirect("not_found")
    return render_template("notice_blocked.html")
# =========================================================================================================================


# ADMIN: HOME
@app.route("/admin/home")
def admin_home():
    # home for the admin
    services = get_all(Service)
    professionals = get_all(Professional)
    requests = get_all(ServiceRequest)
    customers = get_all(Customer)
    home = "admin_home"
    return render_template("admin/home.html", home=home, services=services, professionals=professionals, requests=requests, customers=customers)

# ADMIN: SEARCH
@app.route("/admin/search", methods=["GET", "POST"])
def admin_search():
    profs = None
    services = None
    customers = None
    requests = None

    if request.method == "POST":
        form = AdminSearchForm(request.form)
        if form.validate():
            param = form.parameter.data
            query = form.search.data
            if (param in ["prof_name", "prof_email", "prof_contact"]):
                if query == "":
                    profs = get_all(Professional)
                else:
                    profs = get_profs_with_param(param, query)
            elif (param in ["cust_name", "cust_email", "cust_contact"]):
                if query == "":
                    customers = get_all(Customer)
                else:
                    customers = get_custs_with_param(param, query)
            elif (param in ["service_name", "service_price"]):
                if query == "":
                    services = get_all(Service)
                else:
                    services = get_services_with_param(param, query)
            elif (param in ["request_service", "request_customer", "request_prof"]):
                if query == "":
                    requests = get_all(ServiceRequest)
                else:
                    requests = get_requests_with_param(param, query)
    else:
        form = AdminSearchForm()
    return render_template(
        "admin/search.html",
        form=form, 
        professionals=profs, 
        customers=customers, 
        services=services,
        requests=requests
    )

# ADMIN: SERVICE CREATE
@app.route("/admin/service/create", methods=["GET", "POST"])
def service_create():
    if request.method == "POST":
        form = ServiceCreateForm(request.form)
        if form.validate():
            service_data = {
                "name": form.name.data,
                "price": form.price.data,
                "timereq": form.timereq.data,
                "description": form.description.data,
            }
            service = Service(**service_data)
            if service.service_exists():
                flash("Service with same name already exists")
            else:
                db.session.add(service)
                db.session.commit()
                flash(f"Service Created Successfully: {service.name}")
    else:
        form = ServiceCreateForm()
    return render_template("admin/service/create.html", form=form)

# ADMIN: SERVICE EDIT
@app.route("/admin/service/edit/<service_id>", methods=["GET", "POST"])
def service_edit(service_id):
    service = get_with_id(Service, service_id)
    if not service:
        return redirect(url_for('not_found'))

    if request.method == "POST":
        form = ServiceEditForm(request.form)
        if form.validate():
            if service:
                service.name = form.name.data
                service.description = form.description.data
                service.price = form.price.data
                service.timereq = form.timereq.data
                db.session.commit()
                flash(f"Service Edited Successfully: {service.name}")
    else:
        form = ServiceEditForm()
    return render_template("admin/service/edit.html", form=form, service=service)

# ADMIN: SERVICE DELETE
@app.route("/admin/service/delete/<service_id>", methods=["GET", "POST"])
def service_delete(service_id):
    service = get_with_id(Service, service_id)
    if not service:
        return redirect(url_for('not_found'))
    if request.method == "POST":
        delete_with_id(Service, service_id)
        return redirect(url_for("admin_home"))
    else:
        form = ServiceDeleteForm()
    return render_template("admin/service/delete.html", form=form, service=service)

# ADMIN: SERVICE DETAILS
@app.route("/admin/service/details/<service_id>")
def service_details(service_id):
    service = get_with_id(Service, service_id)
    if not service:
        return redirect(url_for('not_found'))
    return render_template("admin/service/details.html", service=service)

# ADMIN: PROFESSIONAL APPROVE
@app.route("/admin/professional/approve/<prof_id>", methods=["GET", "POST"])
def prof_approve(prof_id):
    form = ProfApproveForm()
    prof = get_with_id(Professional, prof_id)
    if not prof:
        return redirect(url_for('not_found'))
    if request.method == "POST":
        prof.approval = "APPROVED"
        db.session.commit()
        flash(f"Professional Successfully Approved: {prof.user.fullname}")
    return render_template("admin/professional/approve.html", prof=prof, form=form)

# ADMIN: PROFESSIONAL REJECT
@app.route("/admin/professional/reject/<prof_id>", methods=["GET", "POST"])
def prof_reject(prof_id):
    form = ProfRejectForm()
    prof = get_with_id(Professional, prof_id)
    if not prof:
        return redirect(url_for('not_found'))
    if request.method == "POST":
        if prof:
            prof.approval = "REJECTED"
            db.session.commit()
        flash(f"Professional Successfully Rejected: {prof.user.fullname}")
    return render_template("admin/professional/reject.html", prof=prof, form=form)

# ADMIN: PROFESSIONAL DETAILS
@app.route("/admin/professional/details/<prof_id>")
def prof_details(prof_id):
    prof = get_with_id(Professional, prof_id)
    if not prof:
        return redirect(url_for('not_found'))
    return render_template("admin/professional/details.html", prof=prof)

# ADMIN: CUSTOMER DETAILS
@app.route("/admin/customer/details/<cust_id>")
def customer_details(cust_id):
    customer = get_with_id(Customer, cust_id)
    if not customer:
        return redirect(url_for('not_found'))
    return render_template("admin/customer/details.html", customer=customer)

# ADMIN: CUSTOMER BLOCK
@app.route("/admin/customer/block/<cust_id>", methods=["GET", "POST"])
def customer_block(cust_id):
    form = CustomerBlockForm()
    customer = get_with_id(Customer, cust_id)
    if not customer:
        return redirect(url_for('not_found'))
    if request.method == "POST":
        customer.status = "BLOCKED"
        db.session.commit()
        flash(f"Customer Successfully Blocked: {customer.user.fullname}")
    return render_template("admin/customer/block.html", form=form, customer=customer)

# ADMIN: CUSTOMER ACTIVATE
@app.route("/admin/customer/activate/<cust_id>", methods=["GET", "POST"])
def customer_activate(cust_id):
    form = CustomerActivateForm()
    customer = get_with_id(Customer, cust_id)
    if not customer:
        return redirect(url_for('not_found'))
    if request.method == "POST":
        customer.status = "ACTIVE"
        db.session.commit()
        flash(f"Customer Successfully Activated: {customer.user.fullname}")
    return render_template("admin/customer/activate.html", form=form, customer=customer)

# ADMIN: REQUESTS DETAILS
@app.route("/admin/request/details/<request_id>")
def request_details(request_id):
    service_request = get_with_id(ServiceRequest, request_id)
    if not service_request:
        return redirect(url_for('not_found'))
    return render_template("admin/service/request_details.html", service_request=service_request)

# =========================================================================================================================


# PROFESSIONAL: HOME
@app.route("/professional/home/<user_id>")
def professional_home(user_id):
    user = get_with_id(User, user_id)
    if not user:
        return redirect(url_for('not_found'))
    prof = user.get_prof()
    if prof.approval == "REJECTED":
        return redirect(url_for("notice_blocked", user_id=user.id))
    new_requests = prof.get_new_requests(status="REQUESTED")
    closed_requests = prof.get_requests(status="CLOSED")
    accepted_requests = prof.get_requests(status="ASSIGNED")
    return render_template(
        "professional/home.html", 
        professional=prof, 
        accepted_requests=accepted_requests, 
        new_requests=new_requests, 
        closed_requests=closed_requests
    )

# PROFESSIONAL: REQUEST DETAILS
@app.route("/professional/request_details/<request_id>")
def professional_request_details(request_id):
    service_request = get_with_id(ServiceRequest, request_id)
    if not service_request:
        return redirect(url_for('not_found'))
    return render_template("professional/service/request_details.html", service_request=service_request)

# PROFESSIONAL: ACCEPT
@app.route("/professional/<prof_id>/accept/<req_id>", methods=["GET", "POST"])
def request_accept(prof_id, req_id):
    form = RequestAcceptForm()
    service_request = get_with_id(ServiceRequest, req_id)
    professional = get_with_id(Professional, prof_id)
    if not (service_request and professional):
        return redirect(url_for('not_found'))
    if request.method == "POST":
        service_request.status = "ASSIGNED"
        service_request.professional_id = professional.id
        db.session.commit()
        flash(f"Request Successfully Accepted: {service_request.id}")
    return render_template("professional/service/accept.html", form=form, service_request=service_request, professional=professional)

# PROFESSIONAL: REJECT
@app.route("/professional/<prof_id>/reject/<req_id>", methods=["GET", "POST"])
def request_reject(prof_id, req_id):
    form = RequestRejectForm()
    service_request = get_with_id(ServiceRequest, req_id)
    professional = get_with_id(Professional, prof_id)
    if not (service_request and professional):
        return redirect(url_for('not_found'))
    if request.method == "POST":
        service_request.status = "REQUESTED"
        service_request.professional_id = professional.id
        db.session.commit()
        flash(f"Request Successfully Rejected: {service_request.id}")
    return render_template("professional/service/reject.html", form=form, service_request=service_request, professional=professional)

# PROFESSIONAL: SEARCH
@app.route("/professional/search/<prof_id>", methods=["GET", "POST"])
def professional_search(prof_id):
    prof = get_with_id(Professional, prof_id)
    if not prof:
        return redirect(url_for('not_found'))
    new_requests = None
    if request.method == "POST" and prof:
        form = ProfSearchForm(request.form)
        param = form.parameter.data
        query = form.search.data
        if (query == ""):
            new_requests = prof.get_new_requests("REQUESTED")
        elif param == "year":
            new_requests = prof.get_new_requests_with_year(int(query))
        elif param == "month":
            new_requests = prof.get_new_requests_with_month(int(query))
        elif param == "day":
            new_requests = prof.get_new_requests_with_day(int(query))
        elif param == "address":
            new_requests = prof.get_new_requests_with_address(query)
        elif param == "pincode":
            new_requests = prof.get_new_requests_with_pincode(query)
        elif param == "customer":
            new_requests = prof.get_new_requests_with_customer(query)
    else:
        form = ProfSearchForm()
    return render_template("professional/search.html", form=form, professional=prof, new_requests=new_requests)

# PROFESSIONAL: PROFILE
@app.route("/professional/profile/<prof_id>")
def professional_profile(prof_id):
    prof = get_with_id(Professional, prof_id)
    if not prof:
        return redirect(url_for('not_found'))
    return render_template("professional/profile.html", prof=prof)

# PROFESSIONAL: EDIT PROFILE ...
@app.route("/professional/edit/<prof_id>", methods=["GET", "POST"])
def professional_edit(prof_id):
    prof = get_with_id(Professional, prof_id)
    if not (prof):
        return redirect(url_for('not_found'))
    user = prof.user
    # for POST; create form from POST data
    if request.method == "POST":
        form = ProfessionalEditForm(request.form)
        if form.validate():
            data = {
                "fullname": form.fullname.data,
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data,
                "contact": form.contact.data,
                "address": form.address.data,
                "pincode": form.pincode.data,
                "experience": form.experience.data,
                "description": form.description.data,
                "service_id": form.service_id.data,
            }
            user.fullname = data['fullname']
            user.username = data['username']
            user.email = data['email']
            user.password = data['password']
            prof.contact = data['contact']
            prof.address = data['address']
            prof.pincode = data['pincode']
            prof.experience = data['experience']
            prof.description = data['description']
            prof.service_id = data['service_id']
            db.session.commit()
            flash(f"Profile Successfully Edited: {prof.user.fullname}")
    else:
        form = ProfessionalEditForm(service_id=prof.service_id)
    return render_template("professional/edit.html", form=form, prof=prof)

# =========================================================================================================================

# CUSTOMER: HOME
@app.route("/customer/home/<user_id>")
def customer_home(user_id):
    user = get_with_id(User, user_id)
    if not user:
        return redirect(url_for('not_found'))
    customer = user.get_customer()
    if customer.status == "BLOCKED":
        return redirect(url_for("notice_blocked", user_id=user.id))
    service_requests = customer.service_requests
    services = get_all(Service)
    return render_template(
        "customer/home.html", 
        customer=customer, 
        services=services, 
        service_requests=service_requests
    )

# CUSTOMER: REQUEST DETAILS
@app.route("/customer/<cust_id>/request_details/<req_id>")
def customer_request_details(cust_id, req_id):
    service_request = get_with_id(ServiceRequest, req_id)
    customer = get_with_id(Customer, cust_id)
    if not (service_request and customer):
        return redirect(url_for('not_found'))
    return render_template(
        "customer/service/request_details.html",
        customer=customer,
        service_request=service_request,
    )

# CUSTOMER: CANCEL REQUEST...
@app.route("/customer/<cust_id>/request_cancel/<req_id>", methods=["GET", "POST"])
def customer_request_cancel(cust_id, req_id):
    form = CustomerCancelRequestForm()
    service_request = get_with_id(ServiceRequest, req_id)
    customer = get_with_id(Customer, cust_id)
    if not (service_request and customer):
        return redirect(url_for('not_found'))
    if request.method == "POST":
        delete_with_id(ServiceRequest, req_id)
        return redirect(url_for("customer_home", user_id=customer.user.id))
    return render_template(
        "customer/service/request_cancel.html", 
        form=form,
        service_request=service_request,
        customer=customer,
    )

# CUSTOMER: CLOSE REQUEST
@app.route("/customer/<cust_id>/request_close/<req_id>", methods=["GET", "POST"])
def customer_request_close(cust_id, req_id):
    form = CustomerCloseRequestForm()
    service_request = get_with_id(ServiceRequest, req_id)
    customer = get_with_id(Customer, cust_id)
    if not (service_request and customer):
        return redirect(url_for('not_found'))
    professional = service_request.prof()
    if request.method == "POST":
        form = CustomerCloseRequestForm(request.form)
        service_request.status = "CLOSED"
        service_request.completed = datetime.now()
        service_request.rating = form.rating.data
        service_request.remarks = form.remarks.data
        db.session.commit()
        flash(f"Request Successfully Closed: {service_request.id}")
    return render_template(
        "customer/service/request_close.html",
        service_request=service_request,
        customer=customer,
        professional=professional,
        form=form
    )

# CUSTOMER: SERVICE DETAILS
@app.route("/customer/<cust_id>/service/<service_id>")
def customer_service_details(cust_id, service_id):
    service = get_with_id(Service, service_id)
    customer = get_with_id(Customer, cust_id)
    if not (service and customer):
        return redirect(url_for("not_found"))
    profs = service.professionals
    def prof_sort(prof):
        return prof.get_avg_float()
    profs.sort(key=prof_sort, reverse=True)
    return render_template(
        "customer/service/details.html",
        service=service,
        customer=customer,
        professionals=profs,
    )

# CUSTOMER: PROFESSIONAL DETAILS
@app.route("/customer/<cust_id>/professional/<prof_id>")
def customer_prof_details(cust_id, prof_id):
    customer = get_with_id(Customer, cust_id)
    prof = get_with_id(Professional, prof_id)
    if not (prof and customer):
        return redirect(url_for('not_found'))
    return render_template(
        "customer/professional/details.html",
        customer=customer,
        prof=prof
    )

# CUSTOMER: SERVICE BOOK
@app.route("/customer/<cust_id>/service/<service_id>/book/professional/<prof_id>", methods=["GET", "POST"])
def customer_service_book(cust_id, service_id, prof_id):
    form = CustomerServiceBookForm()
    service = get_with_id(Service, service_id)
    prof = get_with_id(Professional, prof_id)
    customer = get_with_id(Customer, cust_id)
    if not (service and prof and customer):
        return redirect(url_for('not_found'))
    if request.method == "POST":
        form = CustomerServiceBookForm(request.form)
        service_request_data = {
            "customer_id": cust_id,
            "service_id": service_id,
            "professional_id": prof_id
        }
        service_request = ServiceRequest(**service_request_data)
        db.session.add(service_request)
        db.session.commit()
        flash(f"Service Successfully Booked: {service_request.id}")
    return render_template(
        "customer/service/book.html",
        form=form,
        customer=customer,
        service=service,
        prof=prof,
    )

# CUSTOMER: PROFILE DETAILS
@app.route("/customer/profile/<cust_id>")
def customer_profile(cust_id):
    customer = get_with_id(Customer, cust_id)
    if not customer:
        return redirect(url_for("not_found"))
    return render_template("customer/profile.html", customer=customer)

# CUSTOMER: PROFILE EDIT
@app.route("/customer/edit/<cust_id>", methods=["GET", "POST"])
def customer_edit(cust_id):
    form = CustomerEditForm()
    customer = get_with_id(Customer, cust_id)
    if not customer:
        return redirect(url_for('not_found'))
    user = customer.user
    # for POST; create form from POST data
    if request.method == "POST":
        form = CustomerEditForm(request.form)
        if form.validate():
            data = {
                "fullname": form.fullname.data,
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data,
                "contact": form.contact.data,
                "address": form.address.data,
                "pincode": form.pincode.data,
            }
            user.fullname = data['fullname']
            user.username = data['username']
            user.email = data['email']
            user.password = data['password']
            customer.contact = data['contact']
            customer.address = data['address']
            customer.pincode = data['pincode']
            db.session.commit()
            flash(f"Profile Successfully Edited: {customer.user.fullname}")
    return render_template("customer/edit.html", form=form, customer=customer)

# CUSTOMER: SEARCH
@app.route("/customer/search/<cust_id>", methods=["GET", "POST"])
def customer_search(cust_id):
    form = CustomerSearchForm()
    customer = get_with_id(Customer, cust_id)
    if not customer:
        return redirect(url_for('not_found'))
    profs = None
    services = None
    if request.method == "POST" and customer:
        form = CustomerSearchForm(request.form)
        param = form.parameter.data
        query = form.search.data
        if (param in ["prof_name", "prof_address", "prof_pincode"]):
            if query == "":
                profs = get_all(Professional)
            else:
                profs = get_profs_with_param(param, query)
        elif (param in ["service_name", "service_price"]):
            if query == "":
                services = get_all(Service)
            else:
                services = get_services_with_param(param, query)
    return render_template("customer/search.html", customer=customer, form=form, profs=profs, services=services)

# TESTING
@app.route("/testing")
def testing():
    return ("Hello World; This is testing")
