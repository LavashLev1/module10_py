from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.phones.append(Phone(phone))

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = Phone(new_phone)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]

    def edit_record(self, name, new_record):
        if name in self.data:
            self.data[name] = new_record

    def search(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Введіть ім'я користувача"
        except (ValueError, IndexError):
            return "Введіть ім'я та номер телефону, будь ласка"
    return wrapper

def handle_hello():
    return "Як я можу вам допомогти?"

@input_error
def handle_add(data, contacts):
    name, phone = data.split(" ")
    record = Record(name, phone)
    contacts.add_record(record)
    return f"Контакт {name} додано."

@input_error
def handle_change(data, contacts):
    name, phone = data.split(" ")
    record = contacts.search(name)
    if record:
        record.edit_phone(record.phones[0], phone)
        return f"Телефон для контакту {name} змінено."
    else:
        return "Такого контакту немає"

@input_error
def handle_phone(name, contacts):
    record = contacts.search(name)
    if record:
        return record.phones[0].value
    else:
        return "Такого контакту немає"

def handle_show_all(contacts):
    if not contacts.data:
        return "Список контактів порожній."
    contact_list = "\n".join([f"{name}: {record.phones[0].value}" for name, record in contacts.data.items()])
    return contact_list

def main():
    contacts = AddressBook()
    
    while True:
        command = input("Введіть команду: ").lower()
        
        if command == "hello":
            response = handle_hello()
        elif command.startswith("add"):
            data = command[len("add"):].strip()
            response = handle_add(data, contacts)
        elif command.startswith("change"):
            data = command[len("change"):].strip()
            response = handle_change(data, contacts)
        elif command.startswith("phone"):
            name = command[len("phone"):].strip()
            response = handle_phone(name, contacts)
        elif command == "show all":
            response = handle_show_all(contacts)
        elif command in ["good bye", "close", "exit"]:
            print("До побачення!")
            break
        else:
            response = "Невідома команда. Спробуйте ще раз."
        
        print(response)

if __name__ == "__main__":
    main()
