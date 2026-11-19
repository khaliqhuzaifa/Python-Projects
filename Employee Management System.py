## Employee Management System

from functools import wraps

class InvalidAgeError(ValueError):
    '''Raised when an employee's age is outside the allowed range (18-65).'''

class InvalidSalaryError(ValueError):
    '''Raised when an employee's salary is zero or negative.'''

class DuplicateEmployeeError(ValueError):
    '''Raised when an employee with the same name already exists in the company.'''

def check_empty(func):
    '''Runs the function if company has employees'''
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        if len(company) == 0:
            print("No employees yet!")
            return None
        return func(*args, **kwargs)
    return wrapper_function

def log_action(label):
    '''Decorator factory: logs when the decorated function starts and finishes,
    using the given label, e.g. [Raise] started / [Raise] done.'''
    def decorator(func):
        @wraps(func)
        def wrapper_function(*args, **kwargs):
            print(f"[{label}] started")
            result = func(*args, **kwargs)
            print(f"[{label}] done")
            return result
        return wrapper_function
    return decorator

class Employee:
    '''Represents a company employee.

    Attributes:
        name (str): Full name, title-cased.
        age (int): Validated to be between 18 and 65.
        department (str): Department name.
        salary (float): Monthly salary, must be positive.
        skills (set): Unique skills, lowercase.
        info (dict): Extra details such as city.
    Class attributes:
        count (int): Number of employees created, used to generate IDs.'''

    count = 0

    def __init__(self, name, age, department, salary):
        self.name = name.strip().title()
        self.age = age
        self.department = department
        self.salary = salary

        Employee.count += 1
        self.__emp_id = f"E{Employee.count:03}"

        self.skills = set()
        self.info = {}

    @staticmethod
    def is_valid_age(age):
        '''Returns True if age is between 18 & 65'''
        return 18<= age <= 65

    @property
    def age(self):
        '''Returns the age as a property'''
        return self._age

    @age.setter
    def age(self, new_age):
        if Employee.is_valid_age(new_age):
            self._age = new_age
        else:
            raise InvalidAgeError("Age must be between 18 & 65!")

    @property
    def salary(self):
        '''Returns the salary as a property'''
        return self._salary

    @salary.setter
    def salary(self, new_salary):
        if new_salary > 0:
            self._salary = new_salary
        else:
            raise InvalidSalaryError("Salary must be greater than 0!")

    @property
    def emp_id(self):
        '''Returns employee ID as a property'''
        return self.__emp_id

    @property
    def initials(self):
        '''Returns the initials of the employee'''
        names_list = self.name.split()
        initial_list = [i[0] for i in names_list]
        initials_str = ".".join(initial_list) + "."
        return initials_str

    @property
    def annual_salary(self):
        '''Returns the annual salary of the employee'''
        return self.salary*12

    def add_skills(self, *skills):
        '''Records the skills of the emmployee in a set'''
        for skill in skills:
            self.skills.add(skill.strip().lower())

    def update_info(self, **kwargs):
        '''Records the extra info of the employee in a dictionary'''
        self.info.update(kwargs)

    def __str__(self):
        return f"{self.emp_id} | {self.name} ({self.initials}) | {self.department} | {self.salary}"

    @classmethod
    def from_string(cls, s):
        '''Creates an isntance from a string input'''
        name, age, department, salary = s.split(",")
        return cls(name, int(age), department, int(salary))

    def __repr__(self):
        return f"Employee(\'{self.name}\', {self.age}, \'{self.department}\', {self.salary})"

    def __gt__(self, other):
        return self.salary > other.salary

    def __add__(self, other):
        return self.salary + other.salary

class Manager(Employee):
    '''An Employee who also receives a yearly bonus.
    Overrides annual_salary to include the bonus.'''
    def __init__(self, name, age, department, salary, bonus):
        super().__init__(name, age, department, salary)
        self.bonus = bonus

    @property
    def annual_salary(self):
        return super().annual_salary + self.bonus

    def __str__(self):
        return super().__str__() + " | Manager"

class Company:
    '''Manages a collection of Employee objects: adding, searching and reporting.'''
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add(self, emp):
        '''Populates the employee list'''
        if not isinstance(emp, Employee):
            raise TypeError("Only Employee objects can be added!")
        if any(e.name == emp.name for e in self.employees):
            raise DuplicateEmployeeError(f"{emp.name} already exists!")
        self.employees.append(emp)

    def __len__(self):
        return len(self.employees)

    def high_earners(self, min_salary):
        '''Yeilds high earners of the company'''
        for e in self.employees:
            if e.salary >= min_salary:
                yield e

    @property
    def departments(self):
        '''Returns a set of all departments'''
        return {e.department for e in self.employees}

    def by_department(self):
        '''Returns a dict of departments: [employee names]'''
        return {
            dept: [e.name for e in self.employees if e.department == dept]
            for dept in self.departments
        }

def make_raise_calculator(percentage):
    '''Returns a function calculating the new salary with raise'''
    def calc(current_salary):
        return round(current_salary * (1+ percentage/100), 2)
    return calc

@check_empty
def view_all():
    '''Returns all employees of the company'''
    for index, employee in enumerate(sorted(company.employees, key = lambda e:e.salary, reverse=True), start = 1):
        print(f"{index}. {employee}")

@check_empty
def search():
    '''Searches for an employee in company and returns its details'''
    name = input("Enter name: ").strip().title()
    for e in company.employees:
        if e.name == name:
            print(repr(e))
            print(f"Skills: {', '.join(sorted(e.skills))}")
            for k, v in e.info.items():
                print(f"Info: {k} - {v}")
            print(f"Annual salary: {e.annual_salary}")
            break
    else:
        print("Employee not found!")

@check_empty
def department_report():
    '''Gives the complete report of the department'''
    report = company.by_department()
    for dept in sorted(report):
        names = report[dept]
        print(f"{dept}: {len(names)} employee(s) -> {', '.join(names)}")
    print(f"Total employees: {len(company)}")
    top = max(company.employees)
    print(f"Top earner: {top.name}")
    ranked = sorted(company.employees, key = lambda e: e.salary, reverse=True)
    top2 = ranked[:2]
    combined = top2[0] + top2[1]
    print(f"Top 2 combined salary: {combined}")
    payroll = sum(e.annual_salary for e in company.employees)
    print(f"Total annual payroll: {payroll}")

@check_empty
@log_action("Raise")
def give_raise(dept, percent):
    '''Gives raise to the employees of the selected department by required percentage'''
    calc = make_raise_calculator(percent)
    selected = list(filter(lambda e: e.department == dept, company.employees))
    for e in selected:
        e.salary = calc(e.salary)
    names = list(map(lambda e: e.name, selected))
    print(f"Raised: {', '.join(names)}")

@check_empty
def show_high_earners():
    '''Returns the employees earning more than the minimum salary'''
    min_salary = float(input("Minimum salary: "))
    for e in company.high_earners(min_salary):
        print(f"{e.name} - {e.salary}")
    print(f"Any above 90000: {any(e.salary > 90000 for e in company.employees)}")
    print(f"All above 40000: {all(e.salary > 40000 for e in company.employees)}")

company = Company("DevVaults")

while True:
    print("" \
    "\n1. Add employee"
    "\n2. Quick add from string"
    "\n3. View all"
    "\n4. Search by name"
    "\n5. Department report"
    "\n6. Give raise to a department"
    "\n7. High earners"
    "\n8. Exit\n"
    )

    choice = input("Enter choice: ")

    if choice == "1":
        try:
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            department = input("Enter department: ")
            salary = int(input("Enter salary: "))
            skills_list = input("Enter skills separated by comma: ").split(",")
            city = input("Enter city name: ")
            manager = input("Manager (y/n)? ")
            if manager.strip().lower() == "y":
                bonus = int(input("Enter bonus: "))
                emp = Manager(name, age, department, salary, bonus)
            else:
                emp = Employee(name, age, department, salary)
            emp.add_skills(*skills_list)
            emp.update_info(city = city)
            company.add(emp)
        except InvalidSalaryError as err:
            print(f"Error: {err}")
        except InvalidAgeError as err:
            print(f"Error: {err}")
        except DuplicateEmployeeError as err:
            print(f"Error: {err}")
        except ValueError:
            print("Error: Please enter numbers for age, salary and bonus!")
        else:
            print(f"Employee added! ID: {emp.emp_id}")
        finally:
            print("-" * 25)

    elif choice == "2":
        try:
            s = input('Enter "name,age,department,salary": ')
            emp = Employee.from_string(s)
            company.add(emp)
        except InvalidSalaryError as err:
            print(f"Error: {err}")
        except InvalidAgeError as err:
            print(f"Error: {err}")
        except DuplicateEmployeeError as err:
            print(f"Error: {err}")
        except ValueError:
            print("Error: Use the format name,age,department,salary with numbers for age and salary!")
        else:
            print(f"Employee added! ID: {emp.emp_id}")
        finally:
            print("-" * 25)

    elif choice == "3":
        view_all()
    elif choice == "4":
        search()
    elif choice == "5":
        department_report()
    elif choice == "6":
        dept = input("Department: ")
        percent = float(input("Raise percentage: "))
        give_raise(dept, percent)
    elif choice == "7":
        show_high_earners()
    elif choice == "8":
        print("Goodbye!")
        break
    else:
        print("Invalid choice!")
