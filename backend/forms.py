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
    BooleanField,
    TimeField,
    FieldList,
    FormField,
    FloatField,
    FileField
)

from wtforms.validators import DataRequired, Regexp, Email
from bson import ObjectId

from .queries import filter_data
from .utils import prepare_dropdown_for_forms, get_current_timestamp_utc, prepare_static_choice_dropdown
from .constants import DEFAULT_COUNTRY_CODE, leave_status_choices, days_of_week_choices, leave_type_choices

category_collection = 'category'
business_collection = 'business'
employee_collection = 'employee'
users_collection = 'users'
queue_collection = 'queue'
service_collection = 'service'
business_schedule_collection = 'business_schedule'
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


class BusinessScheduleForm(StarletteForm):
    business_schedule_id = HiddenField("business_schedule_id")
    merchant_id = SelectField(
        "Business",
        validators=[DataRequired()],
        choices=prepare_dropdown_for_forms(business_collection, 'name', '_id')
    )
    day_of_week = SelectField(
        "Day Of Week",
        validators=[DataRequired()],
        choices=prepare_static_choice_dropdown(days_of_week_choices)
    )
    opening_time = TimeField("Opening Time", validators=[DataRequired()])
    closing_time = TimeField("Closing Time", validators=[DataRequired()])
    always_open = BooleanField("Is Always Open")

    def validate_day_of_week(self, field):
        item_id = self.data.get("business_schedule_id")
        filter_dict = {'day_of_week': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': item_id}
        if filter_data(business_schedule_collection, filter_dict):
            raise ValidationError("Day Of Week already exists for this business")

    def validate_always_open(self, field):
        item_id = self.data.get("business_schedule_id")
        filter_dict = {'always_open': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': item_id}
        if filter_data(business_schedule_collection, filter_dict):
            raise ValidationError("Business always opened")


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
        choices=[])
    owner_id = SelectField(
        "Owner",
        choices=prepare_dropdown_for_forms(
            collection_name=users_collection,
            label='full_name',
            value='_id'
        ))

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
        choices=[]
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
    user_id = SelectField(
        "User Details",
        choices=[]
    )
    queue_id = SelectField(
        "Queue",
        choices=[]
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


class EmployeeServiceForm(StarletteForm):
    employee_service_id = HiddenField("employee_service_id")
    service_id = SelectField(
        "Service",
        validators=[DataRequired()],
        choices=[]
    )
    employee_id = SelectField(
        "Employee",
        validators=[DataRequired()],
        choices=[]
    )
    service_fee = IntegerField("Service Fee")
    # fee_type = SelectField(
    #     "Fee Type",
    #     choices=prepare_static_choice_dropdown(fee_type_choices)
    # )
    description = TextAreaField("Description")
    start_time = TimeField("Enqueue Time")
    end_time = TimeField("Dequeue Time")
    duration = IntegerField("Duration")


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
    # merchant_id = SelectField(
    #     "Business",
    #     validators=[DataRequired()],
    #     choices=prepare_dropdown_for_forms(
    #         collection_name=business_collection,
    #         label='name',
    #         value='_id'
    #     ))
    # employee_id = SelectField(
    #     "Employee",
    #     validators=[DataRequired()],
    #     choices=prepare_dropdown_for_forms(
    #         collection_name=employee_collection,
    #         label='email',
    #         value='_id'
    #     ))
    limit = IntegerField("Limit", validators=[DataRequired()])
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])


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
        choices=[]
    )
    description = StringField("Description")

    def validate_name(self, field):
        item_id = self.data.get("user_id")
        filter_dict = {'name': field.data, "is_deleted": False}
        if item_id:
            filter_dict['_id'] = {'$ne': ObjectId(item_id)}
        if filter_data(service_collection, filter_dict):
            raise ValidationError("Service Name already exists")


class LeaveRequestForm(StarletteForm):
    leave_request_id = HiddenField("leave_request_id")
    employee_id = SelectField(
        "Employee",
        validators=[DataRequired()],
        choices=[]
    )
    start_date = IntegerField("Start Date")
    end_date = IntegerField("End Date")
    start_duration = IntegerField("Start Duration")
    end_duration = IntegerField("End Duration")
    leave_type = SelectField(
        "Leave Type",
        choices=prepare_static_choice_dropdown(leave_type_choices)
    )
    note = StringField("Note")
    duration = IntegerField("Duration")
    status = SelectField(
        "Leave Status",
        choices=prepare_static_choice_dropdown(leave_status_choices)
    )
    requested_date = IntegerField("Requested Date")

    # def validate_name(self, field):
    #     item_id = self.data.get("user_id")
    #     filter_dict = {'name': field.data, "is_deleted": False}
    #     if item_id:
    #         filter_dict['_id'] = {'$ne': ObjectId(item_id)}
    #     if filter_data(service_collection, filter_dict):
    #         raise ValidationError("Service Name already exists")


class PostForm(StarletteForm):
    post_id = HiddenField("post_id")
    business_id = SelectField(
        "Business",
        validators=[DataRequired()],
        choices=[]
    )
    title = StringField("Title")
    image = FileField("Image")
    content = StringField("Content")
    post_type = SelectField(
        "Post Type",
        validators=[DataRequired()],
        choices=[]
    )


class LeaveTypeForm(StarletteForm):
    leave_type_id = HiddenField("leave_type_id")
    business_id = SelectField(
        "Business",
        choices=[]
    )
    name = StringField("Name")
    description = StringField("Description")


class LeaveBalanceForm(StarletteForm):
    leave_balance_id = HiddenField("leave_balance_id")
    leave_type_id = SelectField(
        "Leave Type",
        choices=[]
    )
    employee_id = SelectField(
        "Employee",
        choices=[]
    )
    leave_year = StringField("Leave Year")
    entitlement = IntegerField("Entitlement")
    consumed = IntegerField("Consumed")
    available = IntegerField("Available")
