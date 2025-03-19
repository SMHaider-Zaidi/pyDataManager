import json
import os

file_path = "databases.json"  # Define the relative path for the databases file

# Load existing databases from file if it exists, or create an empty list to store new databases
databases = [] 

if os.path.exists(file_path):  # Check whether the file exists
    with open(file_path, "r") as file: 
        databases = json.load(file)  # Convert JSON string (data) into a Python list

# -------------------------------------------------------------------------
# User input for name
# -------------------------------------------------------------------------
name_ = input('What is your name? ')

while True:
    # ---------------------------------------------------------------------
    # Main Menu
    # ---------------------------------------------------------------------
    print("------------------------------------------------")
    print(f"👋 HELLO! {name_} Welcome to Simple Database Program|")
    print("------------------------------------------------")
    print("1. 🆕 Create a new database                     |")
    print("------------------------------------------------")
    print("2. 📂 Open an existing database                 |")
    print("------------------------------------------------")
    print("3. 📜 Display all databases                     |")
    print("------------------------------------------------")
    print("4. ✏️ Edit an existing database                  |")
    print("------------------------------------------------")
    print("5. 🚪 Exit                                      |")
    print("------------------------------------------------")

    # ---------------------------------------------------------------------
    # User selects an option
    # ---------------------------------------------------------------------
    choice = input("Select an option (1-5): ")

    # ---------------------------------------------------------------------
    # Option 1: Create a new database
    # ---------------------------------------------------------------------
    if choice == '1':
        db_name = input("Enter name of the new database: ")  # Ask for name of the new database
        system_file = f"{db_name}_system.json"  # Create db_name's system_file
        data_file = f"{db_name}_data.json"  # Create db_name's data_file

        # Check if the database name already exists
        if os.path.exists(system_file):
            print("A database with that name already exists.")
        else:  
            # If the database doesn't exist, input the number of fields to create one
            num_fields = int(input("Enter the number of fields: "))
            fields = []  # List of field names
            field_properties = {}  # Dictionary for field names and their max lengths

            for i in range(num_fields):  # Iterate (num_fields) times
                while True:  # Keep asking for valid input
                    max_length = int(input(f"Enter the maximum length for field {i+1}: "))
                    field_name = input(f"Enter name of field {i+1} (Max {max_length} characters): ")

                    if len(field_name) > max_length:
                        print(f"Field name exceeds {max_length} characters. Please try again.")
                    else:
                        fields.append(field_name)  # Add field name to the list
                        field_properties[field_name] = max_length  # Store field and max length in dictionary
                        break  # Exit the inner loop after valid input

            # Save structure to the system file
            filename_maxlen = {
                "fields": fields,
                "field_properties": field_properties
            }

            with open(system_file, "w") as file:
                json.dump(filename_maxlen, file, indent=4)

            with open(data_file, "w") as file:
                json.dump([], file, indent=4)  # Initialize empty records in data_file

            # Add the new database name to the databases list
            databases.append(db_name)

            # Save the updated list of databases to the databases.json file
            with open(file_path, "w") as file:
                json.dump(databases, file, indent=4)

            print(f"Database '{db_name}' created successfully! 🎉")

    # ---------------------------------------------------------------------
    # Option 2: Open an existing database
    # ---------------------------------------------------------------------
    elif choice == '2':
        db_name = input("Enter the name of the database to open: ")
        system_file = f"{db_name}_system.json"
        data_file = f"{db_name}_data.json"

        if not os.path.exists(system_file):
            print("Database does not exist. ❌")
        else:
            with open(system_file, "r") as file:
                filename_maxlen = json.load(file)
                fields = filename_maxlen["fields"]
                field_properties = filename_maxlen["field_properties"]

            with open(data_file, "r") as file:
                records = json.load(file)

            while True:
                print("\nDatabase Management Options")
                print("-------------------------------")
                print("a. ➕ Add record")
                print("-------------------------------")
                print("b. ❌ Delete record")
                print("-------------------------------")
                print("c. 🔍 Search record")
                print("-------------------------------")
                print("d. 📊 Display all records")
                print("-------------------------------")
                print("e. 🔙 Return to main menu")
                print("-------------------------------")

                option = input("Select an option (a-e): ").lower()

                if option == 'a':
                    record = {}
                    for field in fields:
                        while True:
                            value = input(f"Enter value for {field} (Max {field_properties[field]} characters): ")

                            if len(value) > field_properties[field]:
                                print(f"Value exceeds {field_properties[field]} characters. Please try again.")
                            else:
                                record[field] = value
                                break

                    records.append(record)

                    with open(data_file, "w") as file:
                        json.dump(records, file, indent=4)

                    print("Record added successfully! ✔️")

                elif option == 'b':
                    field_name = input("Enter field name to delete by: ")
                    value = input(f"Enter the value to delete records with {field_name} = ")
                    confirm = input(f"Are you sure you want to delete records with {field_name} = {value}? (yes/no): ").lower()

                    if confirm == 'yes':
                        records = [record for record in records if record.get(field_name) != value]

                        with open(data_file, "w") as file:
                            json.dump(records, file, indent=4)

                        print("Record(s) deleted successfully! 🗑️")

                elif option == 'c':
                    field_name = input("Enter field name to search by: ")
                    value = input(f"Enter the value to search for {field_name}: ")

                    for record in records:
                        if record.get(field_name) == value:
                            print("Record found:", record)
                            break
                    else:
                        print("No matching record found. 🚫")

                elif option == 'd':
                    if not records:
                        print("No records in the database. 📭")
                    else:
                        print("\nAll Records:")
                        for record in records:
                            print(record)

                elif option == 'e':
                    break

                else:
                    print("Invalid option selected. Please try again. ❌")

    # ---------------------------------------------------------------------
    # Option 3: Display all databases
    # ---------------------------------------------------------------------
    elif choice == '3':
        if not databases:
            print("No databases have been created yet. 📄")
        else:
            print("\nList of Databases:")
            for db_name in databases:
                print(f"- {db_name} 🗃️")

    # ---------------------------------------------------------------------
    # Option 4: Edit records in an existing database
    # ---------------------------------------------------------------------
    elif choice == '4':
        db_name = input("Enter the name of the database to edit: ")
        data_file = f"{db_name}_data.json"

        if not os.path.exists(data_file):
            print("🚫 Database does not exist.")
        else:
            with open(data_file, "r") as file:
                records = json.load(file)

            if not records:
                print("📭 No records to edit.")
            else:
                print("\n📋 Existing Records:")
                for i, record in enumerate(records, start=1):
                    print(f"{i}. {record}")

    # ---------------------------------------------------------------------
    # Option 5: Exit program
    # ---------------------------------------------------------------------
    elif choice == '5':
        print(f"Exiting program. Goodbye! {name_} 👋")
        break

    else:
        print("Invalid option. Please try again. ❌")
