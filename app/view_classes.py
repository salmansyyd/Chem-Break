class ViewRecord:

    def __init__(self, date, roll_no, class_, section, apparatus, quantity, price, total_ammount):
        self.date = date
        self.roll_no = roll_no
        self.class_ = class_
        self.section = section
        self.apparatus = apparatus
        self.quantity = quantity
        self.price = price
        self.total_ammount = total_ammount

    def __repr__(self) -> str:
        return f"ViewRecord('{self.date}', '{self.roll_no}', '{self.class_}', '{self.section}', '{self.apparatus}', '{self.quantity}', '{self.price}', '{self.total_ammount}')"


class CollectMoney:
    def __init__(self, rollno, total_cash):
        self.rollno = rollno
        self.total_cash = total_cash
