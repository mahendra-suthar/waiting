import re
from starlette_wtf import StarletteForm
from wtforms import (
    SelectField,
    StringField,
    EmailField,
    TextAreaField,
    ValidationError,
    HiddenField,
    IntegerField,
    BooleanField
)

from wtforms.validators import DataRequired, Regexp, Email
from bson import ObjectId

from .queries import filter_data
from .utils import prepare_dropdown_for_forms, get_current_timestamp_utc, prepare_static_choice_dropdown
from .constants import DEFAULT_COUNTRY_CODE, gender_choices

category_collection = 'category'
business_collection = 'business'
employee_collection = 'employee'
users_collection = 'users'
queue_collection = 'queue'
service_collection = 'service'
phone_number_regex = r"^\+?\d{1,15}$"
country_code_regex = r"^\+[1-9]\d*$"


class CategoryForm(StarletteForm):
    name = StringField("name", validators=[DataRequired()])
    description = StringField("description")
    parent_category_id = SelectField(
        "parent_category_id",
        choices=prepare_dropdown_for_forms(
            collection_name=category_collection,
            label='name',
            value='_id'
        ))


class BusinessForm(StarletteForm):
    business_id = HiddenField("business_id")
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password", validators=[DataRequired()])
    country_code = StringField(
        "Country Code",
        default=DEFAULT_COUNTRY_CODE,
        validators=[DataRequired(), Regexp(country_code_regex, message="Invalid country code")]
    )
    phone_number = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(phone_number_regex, message="Invalid phone number")]
    )
    address_id = StringField("Address")
    about_business = TextAreaField("About Business")
    # email_verify = BooleanField('email_verify', default=False)
    # phone_number_verify = BooleanField('phone_number_verify', default=False)
    # description = StringField("Description")
    category_id = SelectField(
        "Category",
        choices=prepare_dropdown_for_forms(
            collection_name=category_collection,
            label='name',
            value='_id'
        ))
    # status = SelectField(
    #     "Status",
    #     choices=prepare_static_choice_dropdown(business_status_choices)
    # )

    def validate_name(self, field):
        item_id = self.data.get("business_id")
        filter_dict = {'name': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': item_id}
        if filter_data(business_collection, filter_dict):
            raise ValidationError("Business Name already exists")

    def validate_phone_number(self, field):
        # if not re.match(r"^\+?[1-9]\d{1,14}$", field.data):
        #     raise ValidationError("Invalid mobile number format")

        item_id = self.data.get("business_id")
        filter_dict = {'phone_number': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': item_id}
        print("------filter_dict------", filter_dict)
        if filter_data(business_collection, filter_dict):
            raise ValidationError("Phone number already exists")

    # def validate_country_code(self, field):
    #     if not re.match(r"^\+[1-9]\d*$", field.data):
    #         raise ValidationError("Invalid country code format")

    def validate_email(self, field):
        item_id = self.data.get("business_id")
        filter_dict = {'email': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': item_id}
        if filter_data(business_collection, filter_dict):
            raise ValidationError("Email already exists")


class EmployeeForm(StarletteForm):
    employee_id = HiddenField("employee_id")
    merchant_id = SelectField(
        "Business",
        choices=prepare_dropdown_for_forms(business_collection, 'name', '_id')
    )
    email = EmailField("Email", validators=[DataRequired(), Email()])
    country_code = StringField(
        "Country Code",
        default=DEFAULT_COUNTRY_CODE,
        validators=[DataRequired(), Regexp(country_code_regex, message="Invalid country code")]
    )
    phone_number = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(phone_number_regex, message="Invalid phone number")]
    )
    joined_date = IntegerField(
        "Joined Date",
        default=get_current_timestamp_utc(),
        validators=[DataRequired()]
    )
    department_id = StringField("Department", validators=[DataRequired()])
    employee_number = IntegerField("Employee Number")

    def validate_employee_number(self, field):
        item_id = self.data.get("employee_id")
        filter_dict = {'employee_number': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': ObjectId(item_id)}
        if filter_data(employee_collection, filter_dict):
            raise ValidationError("Employee Number already exists")

    def validate_phone_number(self, field):
        if not re.match(r"^\+?[1-9]\d{1,14}$", field.data):
            raise ValidationError("Invalid mobile number format")

        item_id = self.data.get("employee_id")
        filter_dict = {'phone_number': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': ObjectId(item_id)}
        if filter_data(employee_collection, filter_dict):
            raise ValidationError("Phone number already exists")

    def validate_country_code(self, field):
        if not re.match(r"^\+[1-9]\d*$", field.data):
            raise ValidationError("Invalid country code format")

    def validate_email(self, field):
        item_id = self.data.get("employee_id")
        filter_dict = {'email': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': ObjectId(item_id)}
        if filter_data(employee_collection, filter_dict):
            raise ValidationError("Email already exists")


class UsersForm(StarletteForm):
    user_id = HiddenField("user_id")
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    full_name = StringField("Full Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    country_code = StringField(
        "Country Code",
        default=DEFAULT_COUNTRY_CODE,
        validators=[DataRequired(), Regexp(country_code_regex, message="Invalid country code")]
    )
    phone_number = StringField(
        "Phone Number",
        validators=[DataRequired(), Regexp(phone_number_regex, message="Invalid phone number")]
    )
    date_of_birth = IntegerField("Date Of Birth")
    # gender = SelectField(
    #     "Gender",
    #     choices=prepare_static_choice_dropdown(gender_choices)
    # )

    def validate_phone_number(self, field):
        if not re.match(r"^\+?[1-9]\d{1,14}$", field.data):
            raise ValidationError("Invalid mobile number format")

        item_id = self.data.get("user_id")
        filter_dict = {'phone_number': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': ObjectId(item_id)}
        if filter_data(employee_collection, filter_dict):
            raise ValidationError("Phone number already exists")

    def validate_country_code(self, field):
        if not re.match(r"^\+[1-9]\d*$", field.data):
            raise ValidationError("Invalid country code format")

    def validate_email(self, field):
        item_id = self.data.get("user_id")
        filter_dict = {'email': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': ObjectId(item_id)}
        if filter_data(employee_collection, filter_dict):
            raise ValidationError("Email already exists")


class QueueForm(StarletteForm):
    queue_id = HiddenField("queue_id")
    name = StringField("Name", validators=[DataRequired()])
    merchant_id = SelectField(
        "Business",
        validators=[DataRequired()],
        choices=prepare_dropdown_for_forms(
            collection_name=business_collection,
            label='name',
            value='_id'
        ))
    employee_id = SelectField(
        "Employee",
        validators=[DataRequired()],
        choices=prepare_dropdown_for_forms(
            collection_name=employee_collection,
            label='email',
            value='_id'
        ))
    limit = IntegerField("Limit", validators=[DataRequired()])
    start_time = IntegerField("Start Time")
    end_time = IntegerField("End Time")


class QueueUserForm(StarletteForm):
    queue_user_id = HiddenField("queue_user_id")
    user_id = SelectField(
        "User",
        validators=[DataRequired()],
        choices=prepare_dropdown_for_forms(
            collection_name=users_collection,
            label='full_name',
            value='_id'
        ))
    queue_id = SelectField(
        "Queue",
        validators=[DataRequired()],
        choices=prepare_dropdown_for_forms(
            collection_name=queue_collection,
            label='name',
            value='_id'
        ))
    priority = BooleanField("Priority")
    enqueue_time = IntegerField("Enqueue Time")
    dequeue_time = IntegerField("Dequeue Time")


class ServiceForm(StarletteForm):
    service_id = HiddenField("service_id")
    name = StringField("Name", validators=[DataRequired()])
    merchant_id = SelectField(
        "Business",
        validators=[DataRequired()],
        choices=prepare_dropdown_for_forms(
            collection_name=business_collection,
            label='name',
            value='_id'
        ))
    description = StringField("Description")

    def validate_name(self, field):
        item_id = self.data.get("user_id")
        filter_dict = {'name': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': ObjectId(item_id)}
        if filter_data(service_collection, filter_dict):
            raise ValidationError("Service Name already exists")
