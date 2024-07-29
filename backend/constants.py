DEFAULT_COUNTRY_CODE = '+91'

Rendat_order = 1
storage_order = 2

order_type_choiced = (
    (Rendat_order, "storage_order"),
    (storage_order, "storage_order")
)


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
EMPLOYEE_REQUESTED = 6
EMPLOYEE_REJECTED = 7


employee_status_choices = (
    (EMPLOYEE_REGISTERED, "Registered"),
    (EMPLOYEE_ACTIVE, "Active"),
    (EMPLOYEE_SUSPENDED, "Suspended"),
    (EMPLOYEE_INACTIVE, "Inactive"),
    (EMPLOYEE_TERMINATED, "Terminated"),
    (EMPLOYEE_REQUESTED, "Requested"),
    (EMPLOYEE_REJECTED, "Rejected"),
)

WORKING_STATUS_IN_MEETING = 1
WORKING_STATUS_COMMUTING = 2
WORKING_STATUS_ON_BREAK = 3
WORKING_STATUS_ON_PARTIAL_LEAVE = 4
WORKING_STATUS_ON_FIRST_HALF_LEAVE = 5
WORKING_STATUS_ON_SECOND_HALF_LEAVE = 6
WORKING_STATUS_ON_FULL_DAY_LEAVE = 7
WORKING_STATUS_VACATIONING = 8
WORKING_STATUS_REMOTELY = 2

working_status_choices = (
    (WORKING_STATUS_IN_MEETING, "In Meeting"),
    (WORKING_STATUS_COMMUTING, "Commuting"),
    (WORKING_STATUS_ON_BREAK, "On Break"),
    (WORKING_STATUS_ON_PARTIAL_LEAVE, "On Partial Leave"),
    (WORKING_STATUS_ON_FIRST_HALF_LEAVE, "On First Half Leave"),
    (WORKING_STATUS_ON_FIRST_HALF_LEAVE, "On Second Half Leave"),
    (WORKING_STATUS_ON_FULL_DAY_LEAVE, "On Full Day Leave"),
    (WORKING_STATUS_VACATIONING, "Vacationing"),
    (WORKING_STATUS_REMOTELY, "Working Remotely")
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
    (QUEUE_USER_REGISTERED, "Registered"),
    (QUEUE_USER_IN_PROGRESS, "In Progress"),
    (QUEUE_USER_COMPLETED, "Completed"),
    (QUEUE_USER_FAILED, "Failed"),
    (QUEUE_USER_CANCELLED, "Cancelled"),
)


QUEUE_RUNNING_START = 1
QUEUE_RUNNING_ON_HOLD = 2
QUEUE_RUNNING_STOP = 3

queue_running_status_choices = (
    (QUEUE_RUNNING_START, "Start"),
    (QUEUE_RUNNING_ON_HOLD, "On Hold"),
    (QUEUE_RUNNING_STOP, "Stop"),
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


PAID_LEAVE = 1
CASUAL_LEAVE = 2
SICK_LEAVE = 3

leave_type_choices = (
    (PAID_LEAVE, "Paid Leave"),
    (CASUAL_LEAVE, "Casual Leave"),
    (SICK_LEAVE, "Sick Leave")
)


LEAVE_PENDING = 1
LEAVE_APPROVED = 2
LEAVE_CANCELLED = 3
LEAVE_REJECTED = 4

leave_status_choices = (
    (LEAVE_PENDING, "Pending"),
    (LEAVE_APPROVED, "Approved"),
    (LEAVE_CANCELLED, "Cancelled"),
    (LEAVE_REJECTED, "Rejected")
)


POST = 1
REELS = 2
STORY = 3

post_type_choices = (
    (POST, "Post"),
    (REELS, "Reels"),
    (STORY, "Story"),
)


ATTENDANCE_CLOCK_IN = 1
ATTENDANCE_CLOCK_OUT = 2

attendance_choices = (
    (ATTENDANCE_CLOCK_IN, "Clock In"),
    (ATTENDANCE_CLOCK_OUT, "Clock Out")
)

