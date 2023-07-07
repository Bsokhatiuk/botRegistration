import enum

class Role(enum.Enum):
    role = ""

class AdminRole(Role):
    role = "Admin"

class EmployeeRole(Role):
    role = "Employee"

class CustomerRole(Role):
    role = "Customer"

class ScheduleStatus(enum.Enum):
    status =''

class ScheduleStatusAvailable(ScheduleStatus):
    status ='Available'

class ScheduleStatusBook(ScheduleStatus):
    status ='Book'

class ScheduleStatusUnavailable(ScheduleStatus):
    status ='Unavailable'

class User:
    def set_phone(self, phone):
        self.phone = phone

    def set_mail(self, mail):
        self.mail = mail

    def get_phone(self):
        return self.phone

    def get_mail(self):
        return self.mail

    def get_id(self):
        return self._id

    def set_id(self, _id):
        self._id = _id

class UserAdmin(User):
    def __init__(self, _id, first_name, last_name, phone, email, role):
        self.role = role
        self.email = email
        self.phone = phone
        self.last_name = last_name
        self._id = _id
        self.first_name = first_name

    def generate_password(self):
        pass

    def set_password(self):
        pass

    def create_employee(self):
        pass

    def edit_employee(self, employee):
        pass

    def create_employee(self):
        pass

class Record():
    def __init__(self, record_id, user, employee, cr_date, book_date, service):
        self.service = service
        self.book_date = book_date
        self.cr_date = cr_date
        self.employee = employee
        self.user = user
        self.record_id = record_id


class Service():
    def __init__(self, name, price):
        self.price = price
        self.name = name



class ScheduleRecord():
    def __init__(self, date, hour, status):
        self.status = status
        self.hour = hour
        self.date = date

class Schedule():
    def __init__(self, listScheduleRecord):
        self.listScheduleRecord = listScheduleRecord

    def create_schedule(self):
        pass

    def change_scheduler_record(self):
        pass

    def book_hour(self):
        pass

    def get_scheduler_today(self):
        pass

    def get_scheduler_available(self):
        pass

    def get_scheduler_book(self):
        pass

class Report():
    pass

class Reminder():
    pass
