import abc


# Implement all methods where `NotImplementedError` is raised


ENGINEER_SALARY = 10
MANAGER_SALARY = 12


class Company(object):
    """Represents a company"""

    reward = 5

    def __init__(self, name: str, address: str = None):
        self.name = name
        self.address = address
        self.employees: list["Employee"] = list()
        self.__money = 1000

    def add_employee(self, employee: "Employee"):
        # make sure employee is an instance of Engineer or Manager
        # make sure he is not employed already
        if self.is_bankrupt:
            raise CompanyIsBankruptException("Company is bankrupt")

        if not isinstance(employee, (Engineer, Manager)):
            raise WrongEmployeeTypeException("Employee is not qualified for employment")

        if employee.is_employed:
            raise EmployeeAlreadyHiredException("Employee is already hired")

        self.employees.append(employee)

    def dismiss_employee(self, employee: "Employee", should_remove: bool = True):
        """
        Dismisses an employee. Employee must be a company member.
        Company should notify employee that he/she was dismissed
        """
        if employee in self.employees:
            employee.notify_dismissed()
            if should_remove:
                self.employees.remove(employee)
        else:
            raise EmployeeNotFoundException("There is no such employee hired")

    def notify_im_leaving(self, employee: "Employee"):
        """An employee should call this method when leaving a company"""
        try:
            self.dismiss_employee(employee)
            employee.company = None
        except EmployeeNotFoundException as e:
            print(str(e))

    # added this method to remove code duplication in do_tasks and write_reports
    def _pay_employee(self, employee: "Employee", amount: int):
        """Method is called when company gives any kind of compensation to employee"""
        if not self.is_bankrupt:
            self.__money -= amount
            employee.put_money_into_my_wallet(amount)
        if self.is_bankrupt:
            self.go_bankrupt()

    def do_tasks(self, employee: "Employee"):
        """
        Engineer should call this method when he is working.
        Company should withdraw 10 money from a personal account and return
        them to engineer. That will be a payment
        :rtype: int
        """

        self.submit_work_results(employee, Engineer, ENGINEER_SALARY)

    def write_reports(self, employee: "Employee"):
        """
        Manager should call this method when he is working.
        Company should withdraw 12 money from a personal account and return
        them to manager. That will be a payment
        :rtype: int
        """

        self.submit_work_results(employee, Manager, MANAGER_SALARY)

    def submit_work_results(
        self, employee: "Employee", employee_role: "Employee", salary: int
    ):
        # make sure engineer is employed to this company
        # check employee is qualified for the job
        if employee not in self.employees:
            raise EmployeeNotFoundException("There is no such employee hired")
        if not isinstance(employee, employee_role):
            raise WrongEmployeeTypeException("Employee is not qualified for employment")
        self._pay_employee(employee, salary)

    def make_a_party(self):
        """Party time! All employees get 5 money"""
        # make sure a company is not a bankrupt before and after the party
        # call employee.bonus_to_salary()
        if not self.is_bankrupt:
            for employee in self.employees:
                employee.bonus_to_salary(self, Company.reward)
                self.__money -= Company.reward
        if self.is_bankrupt:
            self.go_bankrupt()

    def show_money(self):
        """Displays amount of money that company has"""
        print(f"{self.name} got {self.__money} currency unit(s)")

    def go_bankrupt(self):
        """
        Declare bankruptcy. Company money are drop to 0.
        All employees become unemployed.
        """
        self.__money = 0
        for employee in self.employees:
            self.dismiss_employee(employee, should_remove=False)
        self.employees.clear()

    @property
    def is_bankrupt(self):
        """returns True or False"""
        return self.__money <= 0

    def __repr__(self):
        return "Company (%s)" % self.name


class Person(object):
    """Represents any person"""

    def __init__(self, name: str, age: int, sex: str = None, address: str = None):
        self.name = name
        self.age = age
        self.sex = sex if sex is not None else "<not specified>"
        self.address = address

    def __repr__(self):
        return "%s, %s years old" % (self.name, self.age)


class Employee(Person):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name: str, age: int, sex: str = None, address: str = None):
        super(Employee, self).__init__(name, age, sex, address)
        self.company = None
        self.__money = 0

    def join_company(self, company: Company):
        # make sure that this person is not employed already
        try:
            company.add_employee(self)
            self.company = company
        except (WrongEmployeeTypeException, EmployeeAlreadyHiredException) as e:
            print(f"{self.name}: " + str(e))
        except CompanyIsBankruptException as err:
            print(f"{company.name}: " + str(err))

    def become_unemployed(self):
        """Leave current company"""
        try:
            self.company.notify_im_leaving(self)
        except AttributeError:
            print(f"{self.name} is not employed")

    def notify_dismissed(self):
        """Company should call this method when dismissing an employee"""
        self.company = None

    def bonus_to_salary(self, company: Company, reward=5):
        """
        Company should call this method on each employee when having a party
        """
        # make sure person is employed to same company
        # money + 5
        if self.company == company:
            self.put_money_into_my_wallet(reward)

    @property
    def is_employed(self):
        """returns True or False"""
        return self.company is not None

    def put_money_into_my_wallet(self, amount: int):
        """Adds the indicated amount of money to persons budget"""
        # Engineer and Manager will have to use this method to store their
        # salary, because __money is a private attribute
        self.__money += amount

    def show_money(self):
        """Shows how much money person has earned"""
        print(f"{self.name} got {self.__money} currency unit(s)")

    @abc.abstractmethod
    def do_work(self):
        """This method requires re-implementation"""
        raise NotImplemented("This method requires re-implementation")

    def __repr__(self):
        if self.is_employed:
            return "%s works at %s" % (self.name, self.company)
        return "%s, unemployed"


class Engineer(Employee):
    def do_work(self):
        try:
            self.company.do_tasks(self)
        except AttributeError:
            print(f"{self.name} is not employed")


class Manager(Employee):
    def do_work(self):
        try:
            self.company.write_reports(self)
        except AttributeError:
            print(f"{self.name} is not employed")


class EmployeeAlreadyHiredException(Exception):
    pass


class WrongEmployeeTypeException(Exception):
    pass


class EmployeeNotFoundException(Exception):
    pass


class CompanyIsBankruptException(Exception):
    pass


def check_yourself():
    """Now let's operate on objects"""

    # create first company
    fruits_company = Company("Fruits", address="Ocean street, 1")
    print(fruits_company)

    # add some employees
    alex = Engineer("Alex", 55)
    alex.join_company(fruits_company)
    alex.do_work()
    alex.show_money()

    # add second company
    doors_company = Company("Windows and doors", address="Mountain ave. 10")
    print(doors_company)

    # Alex wants to work for doors
    alex.join_company(doors_company)
    # ups, already haired
    alex.become_unemployed()
    alex.join_company(doors_company)
    alex.do_work()

    # Bill also wants to work for doors
    bill = Engineer("Bill", 20)
    bill.join_company(doors_company)
    bill.do_work()

    # Jane is a very good manager. She wants to work for fruits
    jane = Manager("Jane", 30)
    jane.join_company(fruits_company)
    # Jane works pretty hard. She writes lots of reports
    jane.do_work()
    jane.do_work()

    # Bill wants Jane to be his manager, he leaves doors and joins fruits
    bill.become_unemployed()
    bill.join_company(fruits_company)

    # doors becomes a bankrupt
    doors_company.go_bankrupt()

    # alex becomes unemployed and goes to fruits
    alex.join_company(fruits_company)

    # fruits company has a celebration party
    fruits_company.make_a_party()

    # results
    fruits_company.show_money()
    doors_company.show_money()
    alex.show_money()
    bill.show_money()
    jane.show_money()


if __name__ == "__main__":
    check_yourself()
