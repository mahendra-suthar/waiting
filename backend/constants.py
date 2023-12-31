DEFAULT_COUNTRY_CODE = '+91'


CUSTOMER = 1
MERCHANT = 2
EMPLOYEE = 3

user_type = (
    (CUSTOMER, "Customer"),
    (MERCHANT, "Merchant"),
    (EMPLOYEE, "Employee"),
)

MALE = 1
FEMALE = 2
OTHER = 3

gender_choices = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (OTHER, "Other"),
)


BUSINESS_REGISTERED = 1
BUSINESS_ACTIVE = 2
BUSINESS_SUSPENDED = 3
BUSINESS_INACTIVE = 4
BUSINESS_TERMINATED = 5

business_status_choices = (
    (BUSINESS_REGISTERED, "Registered"),
    (BUSINESS_ACTIVE, "Active"),
    (BUSINESS_SUSPENDED, "Suspended"),
    (BUSINESS_INACTIVE, "Inactive"),
    (BUSINESS_TERMINATED, "Terminated"),
)


EMPLOYEE_REGISTERED = 1
EMPLOYEE_ACTIVE = 2
EMPLOYEE_SUSPENDED = 3
EMPLOYEE_INACTIVE = 4
EMPLOYEE_TERMINATED = 5

employee_status_choices = (
    (EMPLOYEE_REGISTERED, "Registered"),
    (EMPLOYEE_ACTIVE, "Active"),
    (EMPLOYEE_SUSPENDED, "Suspended"),
    (EMPLOYEE_INACTIVE, "Inactive"),
    (EMPLOYEE_TERMINATED, "Terminated"),
)


QUEUE_REGISTERED = 1
QUEUE_ACTIVE = 2
QUEUE_SUSPENDED = 3
QUEUE_INACTIVE = 4
QUEUE_TERMINATED = 5

queue_status_choices = (
    (QUEUE_REGISTERED, "Registered"),
    (QUEUE_ACTIVE, "Active"),
    (QUEUE_SUSPENDED, "Suspended"),
    (QUEUE_INACTIVE, "Inactive"),
    (QUEUE_TERMINATED, "Terminated"),
)


QUEUE_USER_REGISTERED = 1
QUEUE_USER_IN_PROGRESS = 2
QUEUE_USER_COMPLETED = 3
QUEUE_USER_FAILED = 4
QUEUE_USER_CANCELLED = 5

queue_user_status_choices = (
    (QUEUE_REGISTERED, "Registered"),
    (QUEUE_USER_IN_PROGRESS, "In Progress"),
    (QUEUE_USER_COMPLETED, "Completed"),
    (QUEUE_USER_FAILED, "Failed"),
    (QUEUE_USER_CANCELLED, "Cancelled"),
)


SERVICE_REGISTERED = 1
SERVICE_ACTIVE = 1
SERVICE_INACTIVE = 1

service_status_choices = (
    (SERVICE_REGISTERED, "Registered"),
    (SERVICE_ACTIVE, "Active"),
    (SERVICE_INACTIVE, "In Active")
)


MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
SUNDAY = 7

days_of_week_choices = (
    (MONDAY, "Monday"),
    (TUESDAY, "Tuesday"),
    (WEDNESDAY, "Wednesday"),
    (THURSDAY, "Thursday"),
    (FRIDAY, "Friday"),
    (SATURDAY, "Saturday"),
    (SUNDAY, "Sunday")
)


FLAT_FEE = 1
HOURLY_FEE = 2

fee_type_choices = (
    (FLAT_FEE, "Flat Fee"),
    (HOURLY_FEE, "Hourly Fee"),
)