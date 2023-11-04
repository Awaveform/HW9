contacts = dict()
mandatory_data = {
    "name": ["add", "change", "phone"],
    "phone": ["add", "change"],
}


def input_error(func) -> callable:
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            return f"Entered name '{args[0]}' was not found. "\
                   f"Type help() for details."
        except ValueError:
            return f"Entered phone is not valid, only digits without any "\
                   f"separators allowed, entered phone: "\
                   f"'{args[0].split()[2]}'. "\
                   f"Type help() for details."
        except (IndexError, TypeError):
            return f"Missing command part, entered data: '{args[0]}', type "\
                   f"'help' to see supported commands or exit to stop the bot."
        else:
            return result
    return wrapper


def hello_command() -> str:
    return "How can I help you?"


def add_command(name: str, phone: int) -> str:
    contacts.update({name: phone})
    return f"Contact was added.\n" \
           f"| {name:<20} | {contacts[name]:<20} |"


@input_error
def change_command(name: str, new_phone: int) -> str:
    contacts[name] = new_phone
    return f"Contact was changed.\n" \
           f"| {name:<20} | {contacts[name]:<20} |"


@input_error
def phone_command(name: str) -> str:
    return f"| {'Name':^20} | {'Phone':^20} |\n" \
           f"{'':-^47}\n" \
           f"| {name:<20} | {contacts[name]:<20} |"


def show_all_command() -> str:
    existing_contacts = f"| {'Name':^20} | {'Phone':^20} |\n" \
                        f"{'':-^47}\n"
    for name, phone in contacts.items():
        existing_contacts += f"| {name:<20} | {phone:<20} |\n"
    return existing_contacts


def exit_command() -> str:
    return "Exit..."


def help_command() -> str:
    return """List of supported commands:\n
           1 - 'hello' to greeting the bot;\n
           2 - 'add' to add a contact, e.g. 'add John 380995057766';\n
           3 - 'change' to change an existing contact's phone,\n
           e.g. 'change John 380995051919';\n
           4 - 'phone' to see a contact, e.g. 'phone John';\n
           5 - 'show all' to show all contacts which were add during the 
           session with the bot:\n
           6 - 'good bye', 'close' or 'exit' to stop the bot;\n
           7 - 'help' to see description and supported commands.\n\n
           Each command, name or phone should be separated by a 
           space like ' '.
           Each command should be entered in order like 'command name 
           phone'.\n
           Each contact's name has to be unique.\n
           Each contact's name should be entered like a single word, if\n
           desired name is first name and last name, separate them with\n
           underscore, e.g. John_Wick.\n
           You can add only one phone to the name.\n
           Purpose of the bot to create, modify and save contacts during\n
           a single session. All data will be deleted after exit from the\n
           session."""


def unknown_command(command: str) -> str:
    return f"Unsupported command: '{command}'. " \
           f"Type 'help' to see supported commands."


@input_error
def parse_command(input_data: str) -> dict:
    command_parts = input_data.split()
    return {
        "command": " ".join(command_parts[0:2]).lower() if any(
            map(input_data.lower().startswith, {"show all", "good bye"})
        ) else command_parts[0].lower(),
        "name": command_parts[1] if command_parts[0].lower() in {
            "add", "change", "phone"} else None,
        "phone": int(command_parts[2]) if command_parts[0].lower() in {
            "add", "change"} else None,
    }


@input_error
def main() -> callable:
    while True:
        command = input(
            "\n"
            "Enter a command. \n"
            "Type 'help' to see list of supported commands. \n"
            "Type 'exit' to stop the bot. \n\n"
        )

        parsed_data = parse_command(command)

        if not parsed_data:
            continue

        match parsed_data["command"]:
            case "hello":
                result = hello_command()
            case "add":
                result = add_command(parsed_data["name"], parsed_data["phone"])
            case "change":
                result = change_command(
                    parsed_data["name"], parsed_data["phone"]
                )
            case "phone":
                result = phone_command(parsed_data["name"])
            case "show all":
                result = show_all_command()
            case "help":
                result = help_command()
            case command if command in {"good bye", "close", "exit"}:
                result = exit_command()
            case _:
                result = unknown_command(command)

        print(result)

        if result == "Exit...":
            break


if __name__ == '__main__':
    main()
