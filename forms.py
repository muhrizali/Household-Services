from models import db
from models import Service, Professional
from sqlalchemy import select
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, EmailField, PasswordField, TextAreaField, IntegerField, SelectField, HiddenField, SubmitField, SearchField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, NumberRange, Disabled

# use 'form.csrf_token' and 'form.errors'
# use 'form.field(class_="classes")'

# getting all the available services
def get_current_services():
    # main code
    sql = select(Service).order_by(Service.name)
    results = db.session.scalars(sql).all()
    choices = [(row.id, row.name) for row in results]
    return choices

# def prof_service_id():
#     sql = select(Professional):


# Define your forms here...

# login form
class LoginForm(FlaskForm):
    email = EmailField("Email", [DataRequired(), InputRequired()])
    password = PasswordField("Password", [DataRequired(), InputRequired(), Length(min=8, max=40)])
    # ADMIN, CUSTOMER, PROFESSIONAL
    # role = HiddenField(validators=[DataRequired(), InputRequired()])
    

# base register form
class BaseRegisterForm(FlaskForm):
    # fullname, username, email, password, confirm_password
    fullname = StringField("Full Name", [DataRequired(), InputRequired(), Length(min=2, max=200)])
    username = StringField("Username", [DataRequired(), InputRequired(), Length(min=2, max=30)])
    email = EmailField("Email", [DataRequired(), InputRequired()])
    password = PasswordField("Password", [DataRequired(), InputRequired(), Length(min=8, max=40)])
    confirm = PasswordField("Confirm Password", [DataRequired(), InputRequired(), EqualTo("password", message="Passwords must match")])

    # roles:
    role = HiddenField(validators=[DataRequired(), InputRequired()])

# customer register form
class CustomerRegisterForm(BaseRegisterForm):
    # contact, address, pincode
    contact = StringField("Contact No.", [DataRequired(), InputRequired(), Length(min=10, max=10)])
    address = TextAreaField("Address", [DataRequired(), InputRequired()])
    pincode = StringField("Pin Code", [DataRequired(), InputRequired(), Length(min=6, max=6)])

# professional register form
class ProfessionalRegisterForm(BaseRegisterForm):
    # contact, address, pincode, experience, description, service
    contact = StringField("Contact Number", [DataRequired(), InputRequired(), Length(min=10, max=10)])
    address = TextAreaField("Address", [DataRequired(), InputRequired()])
    pincode = StringField("Pin Code", [DataRequired(), InputRequired(), Length(min=6, max=6)])

    # documents for verification; in PDF only
    docs = FileField("Documents (PDFs)", [FileRequired(), FileAllowed(["pdf"], "PDF Files Only")])


    experience = IntegerField("Experience (In Years)", [DataRequired(), InputRequired(), NumberRange(min=0)])
    description = TextAreaField("Description", [DataRequired(), InputRequired()])

    # getting services
    available_services = get_current_services()
    service_id = SelectField("Specialised Service", [DataRequired(), InputRequired()], choices=available_services)

# create service form
class ServiceCreateForm(FlaskForm):
    # name, price, timereq, description
    name = StringField("Name", [DataRequired(), InputRequired(), Length(min=2, max=200)])
    price = IntegerField("Price (In Rupees)", [DataRequired(), InputRequired(), NumberRange(min=0)])
    timereq = IntegerField("Time Required (In Hours)", [DataRequired(), InputRequired(), NumberRange(min=1)])
    description = TextAreaField("Description", [DataRequired(), InputRequired()])

# edit service form
class ServiceEditForm(FlaskForm):
    # name, price, timereq, description
    name = StringField("Name", [DataRequired(), InputRequired(), Length(min=2, max=200)])
    price = IntegerField("Price (In Rupees)", [DataRequired(), InputRequired(), NumberRange(min=0)])
    timereq = IntegerField("Time Required (In Hours)", [DataRequired(), InputRequired(), NumberRange(min=1)])
    description = TextAreaField("Description", [DataRequired(), InputRequired()])

# delete service form
class ServiceDeleteForm(FlaskForm):
    # delete, cancel
    delete = SubmitField("Delete")

# approve professional form
class ProfApproveForm(FlaskForm):
    # delete, cancel
    approve = SubmitField("Approve")

# reject professional form
class ProfRejectForm(FlaskForm):
    # delete, cancel
    reject = SubmitField("Reject")


# block customer form
class CustomerBlockForm(FlaskForm):
    # delete, cancel
    block = SubmitField("Block")

# activate customer form
class CustomerActivateForm(FlaskForm):
    # delete, cancel
    activate = SubmitField("Activate")

# admin search form
class AdminSearchForm(FlaskForm):
    choices = [
        ("prof_name", "Professional: Name"),
        ("prof_email", "Professional: Email"),
        ("prof_contact", "Professional: Contact"),
        ("cust_name", "Customer: Name"),
        ("cust_email", "Customer: Email"),
        ("cust_contact", "Customer: Contact"),
        ("service_name", "Service: Name"),
        ("service_price", "Service: Price"),
        ("request_service", "Service Request: Service Name"),
        ("request_customer", "Service Request: Customer Name"),
        ("request_prof", "Service Request: Professional Name"),
    ]
    parameter = SelectField("Search Parameter", [DataRequired(), InputRequired()], choices=choices)
    search = SearchField("Search")
    submit = SubmitField("Search")

# request accept form
class RequestAcceptForm(FlaskForm):
    accept = SubmitField("Accept")

# request reject form
class RequestRejectForm(FlaskForm):
    reject = SubmitField("Reject")

# professional search form
class ProfSearchForm(FlaskForm):
    choices = [
        ("year", "Date: Year"),
        ("month", "Date: Month"),
        ("day", "Date: Day"),
        ("customer", "Customer: Name"),
        ("address", "Customer: Address"),
        ("pincode", "Customer: Pin Code"),
    ]
    parameter = SelectField("Search Parameter", [DataRequired(), InputRequired()], choices=choices)
    search = SearchField("Search")
    submit = SubmitField("Search")

# professional search form
class CustomerSearchForm(FlaskForm):
    choices = [
        ("prof_name", "Professionals: Name"),
        ("prof_address", "Professionals: Address"),
        ("prof_pincode", "Professionals: Pin Code"),
        ("service_name", "Service: Name"),
        ("service_price", "Service: Price"),
    ]
    parameter = SelectField("Search Parameter", [DataRequired(), InputRequired()], choices=choices)
    search = SearchField("Search")
    submit = SubmitField("Search")


# base edit form
class BaseEditForm(FlaskForm):
    # fullname, username, email, password, confirm_password
    fullname = StringField("FULL NAME", [DataRequired(), InputRequired(), Length(min=2, max=200)])
    username = StringField("USERNAME", [DataRequired(), InputRequired(), Length(min=2, max=30)])
    email = EmailField("EMAIL", [DataRequired(), InputRequired()])
    password = StringField("PASSWORD", [DataRequired(), InputRequired(), Length(min=8, max=40)])

# customer edit form
class CustomerEditForm(BaseEditForm):
    # contact, address, pincode
    contact = StringField("Contact No.", [DataRequired(), InputRequired(), Length(min=10, max=10)])
    address = TextAreaField("Address", [DataRequired(), InputRequired()])
    pincode = StringField("Pin Code", [DataRequired(), InputRequired(), Length(min=6, max=6)])

# professional edit form
class ProfessionalEditForm(BaseEditForm):
    # contact, address, pincode, experience, description, service
    contact = StringField("CONTACT NUMBER", [DataRequired(), InputRequired(), Length(min=10, max=10)])
    address = TextAreaField("ADDRESS", [DataRequired(), InputRequired()])
    pincode = StringField("PIN CODE", [DataRequired(), InputRequired(), Length(min=6, max=6)])

    experience = IntegerField("EXPERIENCE (IN YEARS)", [DataRequired(), InputRequired(), NumberRange(min=0)])
    description = TextAreaField("DESCRIPTION", [DataRequired(), InputRequired()])

    # getting services
    available_services = get_current_services()
    service_id = SelectField("SERVICE", [DataRequired(), InputRequired()], choices=available_services)

# customer service request cancel
class CustomerCancelRequestForm(FlaskForm):
    cancel = SubmitField("Cancel")

# customer closing request form
class CustomerCloseRequestForm(FlaskForm):
    stars = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]
    rating = SelectField("RATING:", [DataRequired(), InputRequired()], choices=stars)
    remarks = TextAreaField("REMARKS:")

# customer service book form
class CustomerServiceBookForm(FlaskForm):
    book = SubmitField("Book")






    

# TODO: EditCustomerForm, EditProfessionalForm
