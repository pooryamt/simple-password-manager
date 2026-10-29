import re
import json
import secrets
import string
credentials = []
def validate_password(password: str) -> bool:
    """Return True if the password meets the required complexity rules."""
    password_pattern = re.compile(
        r"(?=.*[a-z])"
        r"(?=.*[A-Z])"
        r"(?=.*\d)"                         
        r"(?=.*[!@#$%^&*])"
        r"[A-Za-z\d!@#$%^&*]{8,}"
    )
    if re.fullmatch(password_pattern, password):
        return True
    return False  
def validate_non_blank(argumet: str) -> bool:
    pattern = re.compile(r"\s+")
    if re.fullmatch(pattern, argumet):
        return False
    return True
def add_credential(service: str, username: str, password: str):
    """Create and store a credential record"""
    next_credential_id = (
        max((credential["id"] for credential in credentials), default=0) + 1
    )
    credential = {
        "id": next_credential_id,
        "service": service,
        "username": username,
        "password": password,
    }
    credentials.append(credential)
    return
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def save_credentials():
    """Write credentials to the JSON file."""
    with open("credentials.json", "w", encoding="utf-8") as file:
        json.dump(credentials, file, indent=4, ensure_ascii=False)
    return
def load_credentials():
    """Load credentials from the JSON file."""
    try:
        with open("credentials.json", "r", encoding="utf-8") as file:
            credentials = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        print(
            f"Error -> Credentials.json contains invalid json({error.lineno},column {error.colno})."
        )
        raise SystemExit(1)
    if not isinstance(credentials, list):
        print("Error -> Credentials.json must contain a list of tasks.")
        raise SystemExit(1)
    return credentials
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def view_credentials():
    """Display all credentials with passwords masked."""
    if not credentials:
        print("No credentials found.")
        return
    print("=== ALL CREDENTIALS ===")
    for credential in credentials:
        print(f"Credential ID = {credential['id']}")
        print(f"Service = {credential['service']}")
        print(f"User name = {credential['username']}")
        print(f"Password = ########")
        print("-" * 50)
    return
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def show_credential(credential):
    """Display a single credential"""
    print("=== CREDENTIAL ===")
    print(f"Credential ID = {credential['id']}")
    print(f"Service = {credential['service']}")
    print(f"User name = {credential['username']}")
    print(f"Password = {credential['password']}")
    print("-" * 50)
    return
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def search_credential(
    next_credential_id: int,
) -> None | dict:
    """Find a credential by its ID."""
    for credential in credentials:
        if credential["id"] == next_credential_id:
            return credential
    return None


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def edit_credential(next_credential_id: int, field, new_value: str):
    """Update one field of an existing credential."""
    credential = search_credential(next_credential_id)
    credential[field] = new_value
    return


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def delete_credential(next_credential_id: int):
    """Remove a credential by its ID."""
    credential = search_credential(next_credential_id)
    credentials.remove(credential)
    return


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def generate_password(length: int = 12) -> str:
    """Generate a password containing all required character types."""
    if length < 8:
        raise ValueError("Password length must be at least 8.")
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*"
    all_chars = lowercase + uppercase + digits + symbols
    password_chars = [secrets.choice(lowercase),secrets.choice(uppercase),secrets.choice(digits),secrets.choice(symbols)]
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(all_chars))
    secrets.SystemRandom().shuffle(password_chars) 
    return "".join(password_chars)                 
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
credentials = load_credentials()
while True:
    print("1- Add Credential")
    print("2- View Credentials")
    print("3- Search Credential")
    print("4- Edit Credential")
    print("5- Delete Credential")
    print("6- exit ")
    choice = input("Choose an option : ").strip()
    if choice not in {"1", "2", "3", "4", "5", "6"}:
        print("Error -> invalid choice. Please try again")
        continue
    if choice == "1":
        while True:
            service = input(
                "Enter a service : "
            ).strip()  
            if not validate_non_blank(service) or not service:
                print("Error -> Service name cannot be empty. Please try again.")
                continue
            break
        while True:
            username = input("Enter username : ").strip()
            if not validate_non_blank(username) or not username:
                print("Error -> Username name cannot be empty. Please try again.")
                continue
            break
        while True:
            print("1- Generate a Password ")
            print("2- Enter a password manually")
            password_choice = input("Choose an option : ").strip()
            if password_choice not in {"1", "2"}:
                print("Error -> Invalid choice. Please try again")
                continue
            if (
                password_choice == "1"
            ):  
                password = generate_password()
                print(f'Generated password : {password}')
            elif password_choice == "2":
                while True:
                    password = input(
                        "Enter a password (at least 8 characters, including lowercase,uppercase,a digit,and special character) : "
                    ).strip()
                    if not validate_password(password):
                        print("Error -> Invalid password try again")
                        continue
                    break
            break
        add_credential(service, username, password)
        save_credentials()
        print("Credential added successfully")
    elif choice == "2":
        view_credentials()
    elif choice == "3":
        while True:
            try:
                credential_id = int(input("Enter a credential ID : ").strip())
            except ValueError:
                print("Error -> Please enter a valid numeric credential ID")
                continue
            break
        credential = search_credential(credential_id)
        if credential is None:
            print("Error -> Credential not found")
            continue
        show_credential(credential)
    elif choice == "4":
        while True:
            try:
                credential_id = int(input("Enter a credential ID : ").strip())
            except ValueError:
                print("Error -> Please enter a valid numeric credential ID")
                continue
            break
        credential=search_credential(credential_id)   
        if credential is None:
            print("Error ->  Credential not found")
            continue

        while True:
            credential = search_credential(credential_id)
            show_credential(credential)  
            print("1- Edit Service")
            print("2- Edit User Name")
            print("3- Edit Password")
            print("4- Back to main menu")
            edit_choice = input("Choose an option : ")
            if edit_choice not in {"1", "2", "3", "4"}:
                print("Error -> Invalid choice. Please try again")
                continue
            if edit_choice == "1":
                while True:
                    new_service = input("Enter a service : ").strip()
                    if not validate_non_blank(new_service) or not new_service:
                        print("Error -> Service name cannot be empty. Please try again.")
                        continue
                    break
                edit_credential(credential_id, "service", new_service)
                save_credentials()
                print("Credential updated successfully.")
                continue
            elif edit_choice == "2":
                while True:
                    new_username = input("Enter a service : ").strip()
                    if not validate_non_blank(new_username) or not new_username:
                        print(
                            "Error -> Username name cannot be empty. Please try again."
                        )
                        continue
                    break
                edit_credential(credential_id, "username", new_username)
                save_credentials()
                print("Credential updated successfully.")
                continue
            elif edit_choice == "3":
                while True:
                    print("1- Generate a Password ")
                    print("2- Enter a password manually")
                    new_password_choice = input("Choose an option : ").strip()
                    if new_password_choice not in {"1", "2"}:
                        print("Error -> Invalid choice. Please try again")
                        continue
                    if new_password_choice == "1":
                        new_password = generate_password()
                        print(f'Generated password : {new_password}')
                    elif new_password_choice == "2":
                        while True:
                            new_password = input(
                                "Enter a password (at least 8 characters, including lowercase,uppercase,a digit,and special character)  : "
                            ).strip()
                            if not validate_password(new_password):
                                print("Error -> Invalid password try again")
                                continue
                            break
                    break
                edit_credential(credential_id, "password", new_password)
                save_credentials()
                print("Credential updated successfully.")
                continue
            elif edit_choice == "4":
                break
    elif choice == "5":
        while True:
            try:
                credential_id = int(input("Enter a credential ID : ").strip())
            except ValueError:
                print("Error -> Please enter a valid numeric credential ID")
                continue
            break
        credential = search_credential(credential_id)
        if credential is None:
            print("Error ->  Credential not found")
            continue
        while True:
            print("1- Yes")
            print("2- No")
            delete_choice = input(
                "do you really want to delete the credential? : "
            ).strip()
            if delete_choice not in {"1", "2"}:
                print("Error -> Invalid choice. Please try again")
                continue
            if delete_choice == "1":
                delete_credential(credential_id)
                save_credentials()
                print("Credential deleted successfully.")
                break
            if delete_choice == "2":
                break
    elif choice == "6":
        break

