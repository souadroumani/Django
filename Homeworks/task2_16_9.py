# ---------------SRP--------------------
class TextBuilder:
    def build_text(self, items):
        return "\n".join(items)


class FileSaver:
    def save(self, filename, content):
        with open(filename, "w") as f:
            f.write(content)


data_list = ["A", "B", "C"]
text_maker = TextBuilder()
saver = FileSaver()

result_text = text_maker.build_text(data_list)
saver.save("output.txt", result_text)


# ---------------OCP-------------------
class Shape:
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


c = Circle(5)
s = Square(4)
r = Rectangle(3, 6)

print(c.area())
print(s.area())
print(r.area())


# ----------------LSP--------------------------
class Bird:
    def move(self):
        print("Flying")


class Penguin(Bird):
    def move(self):
        print("Walking on ground")


# ------ ---------ISP-----------------------
class Worker:
    def work(self):
        print("Working hard")


class Eater:
    def eat(self):
        print("Taking a meal")


class Android(Worker):
    pass


class Person(Worker, Eater):
    pass


rob = Android()
rob.work()


# ----------------DIP---------------------------
class SQLDatabase:
    def fetch(self):
        return ["rows from SQL"]


class CacheDB:
    def fetch(self):
        return ["rows from Cache"]


class DataService:
    def __init__(self, db_source):
        self.db_source = db_source

    def get_data(self):
        return self.db_source.fetch()


sql_service = DataService(SQLDatabase())
print(sql_service.get_data())

cache_service = DataService(CacheDB())
print(cache_service.get_data())


# --------------- Strategy Pattern-----------------------
class NoDiscount:
    def apply(self, total):
        return total


class PercentageDiscount:
    def __init__(self, percent):
        self.percent = percent

    def apply(self, total):
        return total * (1 - self.percent / 100)


class FlatDiscount:
    def __init__(self, cut):
        self.cut = cut

    def apply(self, total):
        return max(total - self.cut, 0)


class ShoppingCart:
    def __init__(self, discount_policy):
        self.products = []
        self.discount_policy = discount_policy

    def add_product(self, price):
        self.products.append(price)

    def total(self):
        subtotal = sum(self.products)
        return self.discount_policy.apply(subtotal)

    def set_policy(self, discount_policy):
        self.discount_policy = discount_policy


cart1 = ShoppingCart(NoDiscount())
cart1.add_product(100)

cart2 = ShoppingCart(PercentageDiscount(10))
cart2.add_product(200)
print(cart2.total())

cart1.set_policy(FlatDiscount(30))
print(cart1.total())


# -------------------Observer Pattern---------------------
class Subject:
    def __init__(self):
        self._listeners = []

    def subscribe(self, listener):
        self._listeners.append(listener)

    def unsubscribe(self, listener):
        self._listeners.remove(listener)

    def notify(self, msg):
        for obs in self._listeners:
            obs.update(msg)


class Listener:
    def update(self, msg):
        pass


class EmailListener(Listener):
    def update(self, msg):
        print(f"Email received: {msg}")


class SMSListener(Listener):
    def update(self, msg):
        print(f"SMS received: {msg}")


news_feed = Subject()

email_listener = EmailListener()
sms_listener = SMSListener()

news_feed.subscribe(email_listener)
news_feed.subscribe(sms_listener)

news_feed.notify("Breaking News!")


# -----------------------Factory Pattern------------------------
class Dog:
    def speak(self):
        print("Woof!")


class Cat:
    def speak(self):
        print("Meow!")


class AnimalCreator:
    def create(self, kind):
        if kind.lower() == "dog":
            return Dog()
        elif kind.lower() == "cat":
            return Cat()


factory = AnimalCreator()
pet = factory.create("dog")
pet.speak()


# -----------------------Adapter Pattern-------------------------------
class OldPrinter:
    def print_text(self, msg):
        print(f"OldPrinter: {msg}")


class ModernPrinter:
    def print(self, msg, style="plain"):
        print(f"ModernPrinter ({style}): {msg}")


class PrinterAdapter:
    def __init__(self, printer, style="plain"):
        self.printer = printer
        self.style = style

    def print_message(self, msg):
        if isinstance(self.printer, OldPrinter):
            self.printer.print_text(msg)
        elif isinstance(self.printer, ModernPrinter):
            self.printer.print(msg, self.style)


legacy_printer = OldPrinter()
modern_printer = ModernPrinter()

adapter1 = PrinterAdapter(legacy_printer)
adapter2 = PrinterAdapter(modern_printer, style="fancy")

adapter1.print_message("Hello World")
adapter2.print_message("Hello World")


# --------------------Singleton Pattern------------------
class Logger:
    _instance = None

    def __init__(self):
        if Logger._instance is None:
            Logger._instance = self

    def log(self, message):
        print(f"[LOG]: {message}")

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance


logger1 = Logger.get_instance()
logger2 = Logger.get_instance()

print(logger1 is logger2)
logger1.log("Hello")
logger2.log("World")
