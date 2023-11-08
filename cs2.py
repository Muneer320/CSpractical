import sqlite3

# Connect to the SQLite database
def connect_to_database(database_name):
    try:
        conn = sqlite3.connect(database_name)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Create a table for a tracker if it doesn't exist
def create_tracker_table(conn, table_name, columns):
    try:
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                user TEXT,
                date DATE,
                {columns}
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating the table: {e}")

# Display data from a tracker's table
def show_tracker_data(conn, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        data = cursor.fetchall()
        if data:
            print(f"{table_name} Table:")
            for row in data:
                print(row)
        else:
            print(f"No data in the {table_name} Table.")
    except sqlite3.Error as e:
        print(f"Error displaying data: {e}")

# Reset a tracker's table
def reset_tracker_table(conn, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {table_name}')
        conn.commit()
        print(f"{table_name} Table has been reset.")
    except sqlite3.Error as e:
        print(f"Error resetting the table: {e}")

# Delete user data from all trackers
def delete_user_data(conn, user):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        for table in tables:
            if table != 'sqlite_sequence':  # Exclude system table
                cursor.execute(f'DELETE FROM {table} WHERE user = ?', (user,))
                conn.commit()

        print(f"All data for user '{user}' has been deleted from all tables.")
    except sqlite3.Error as e:
        print(f"Error deleting user data: {e}")


# Main program
def main():
    database_name = 'Trackers.db'
    conn = connect_to_database(database_name)

    if conn is not None:
        while True:
            print("\nMain Menu")
            print("1. Sleep Tracker")
            print("2. Diet Tracker")
            print("3. Expense Tracker")
            print("4. Exercise Tracker")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                table_name = 'SleepTracker'
                columns = 'duration REAL'
            elif choice == '2':
                table_name = 'DietTracker'
                columns = 'meal TEXT'
            elif choice == '3':
                table_name = 'ExpenseTracker'
                columns = 'amount REAL, description TEXT'
            elif choice == '4':
                table_name = 'ExerciseTracker'
                columns = 'exercise TEXT, duration REAL'
            elif choice == '5':
                conn.close()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            create_tracker_table(conn, table_name, columns)

            role = input("Are you an admin or a user? (admin/user): ").lower()

            if role == 'admin':
                print(f"\nAdmin Menu for {table_name}")
                print("1. Show Table")
                print("2. Reset Table")
                print("3. Delete User Data from All Trackers")
                print("4. Back to Main Menu")

                admin_choice = input("Enter your choice: ")

                if admin_choice == '1':
                    show_tracker_data(conn, table_name)
                elif admin_choice == '2':
                    reset_tracker_table(conn, table_name)
                elif admin_choice == '3':
                    user = input("Enter the user to delete data: ")
                    delete_user_data(conn, user)
                elif admin_choice == '4':
                    continue
                else:
                    print("Invalid choice. Please try again.")

            elif role == 'user':
                while True:
                    print(f"\nUser Menu for {table_name}")
                    print("1. Add Data")
                    print("2. Edit Data")
                    print("3. Delete Data")
                    print("4. Show Data")
                    print("5. Back to Main Menu")

                    user_choice = input("Enter your choice: ")

                    # Implement user-specific functionalities for adding, editing, deleting, and showing data

                    if user_choice == '1':  # Add Data
                        user_name = input("Enter user name: ")
                        date = input("Enter date (YYYY-MM-DD): ")

                        if table_name == 'SleepTracker':
                            duration = float(input("Enter sleep duration (hours): "))
                            cursor = conn.cursor()
                            insert_data = (user_name, date, duration)
                            cursor.execute(f'INSERT INTO {table_name} (user, date, duration) VALUES (?, ?, ?)', insert_data)
                        
                        elif table_name == 'DietTracker':
                            meal = input("Enter meal description: ")
                            calories = float(input("Enter meal calories: "))
                            cursor = conn.cursor()
                            insert_data = (user_name, date, meal, calories)
                            cursor.execute(f'INSERT INTO {table_name} (user, date, meal, calories) VALUES (?, ?, ?, ?)', insert_data)

                        elif table_name == 'ExpenseTracker':
                            amount = float(input("Enter expense amount: "))
                            description = input("Enter expense description: ")
                            cursor = conn.cursor()
                            insert_data = (user_name, date, amount, description)
                            cursor.execute(f'INSERT INTO {table_name} (user, date, amount, description) VALUES (?, ?, ?, ?)', insert_data)

                        elif table_name == 'ExerciseTracker':
                            exercise = input("Enter exercise description: ")
                            duration = float(input("Enter exercise duration (minutes): "))
                            cursor = conn.cursor()
                            insert_data = (user_name, date, exercise, duration)
                            cursor.execute(f'INSERT INTO {table_name} (user, date, exercise, duration) VALUES (?, ?, ?, ?)', insert_data)

                        conn.commit()
                        print("Data added successfully.")

                    if user_choice == '2':  # Edit Data
                        user_name = input("Enter user name: ")
                        date = input("Enter date (YYYY-MM-DD): ")

                        if table_name == 'SleepTracker':
                            duration = float(input("Enter new sleep duration (hours): "))
                            cursor = conn.cursor()
                            update_data = (duration, user_name, date)
                            cursor.execute(f'UPDATE {table_name} SET duration = ? WHERE user = ? AND date = ?', update_data)

                        elif table_name == 'DietTracker':
                            meal = input("Enter new meal description: ")
                            calories = float(input("Enter new meal calories: "))
                            cursor = conn.cursor()
                            update_data = (meal, calories, user_name, date)
                            cursor.execute(f'UPDATE {table_name} SET meal = ?, calories = ? WHERE user = ? AND date = ?', update_data)

                        elif table_name == 'ExpenseTracker':
                            amount = float(input("Enter new expense amount: "))
                            description = input("Enter new expense description: ")
                            cursor = conn.cursor()
                            update_data = (amount, description, user_name, date)
                            cursor.execute(f'UPDATE {table_name} SET amount = ?, description = ? WHERE user = ? AND date = ?', update_data)

                        elif table_name == 'ExerciseTracker':
                            exercise = input("Enter new exercise description: ")
                            duration = float(input("Enter new exercise duration (minutes): "))
                            cursor = conn.cursor()
                            update_data = (exercise, duration, user_name, date)
                            cursor.execute(f'UPDATE {table_name} SET exercise = ?, duration = ? WHERE user = ? AND date = ?', update_data)

                        conn.commit()
                        print("Data edited successfully.")


                    elif user_choice == '3':  # Delete Data
                        user_name = input("Enter user name: ")
                        date = input("Enter date (YYYY-MM-DD): ")

                        cursor = conn.cursor()
                        cursor.execute(f'DELETE FROM {table_name} WHERE user = {user_name} AND date = {date}')

                        conn.commit()
                        print("Data deleted successfully.")

                    elif user_choice == '4':  # Show Data
                        user_name = input("Enter user name: ")
                        cursor = conn.cursor()

                        # Get the table names from the database
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                        table_names = [table[0] for table in cursor.fetchall()]

                        # Display data for each table
                        for table in table_names:
                            cursor.execute(f'SELECT * FROM {table} WHERE user = ?', (user_name,))
                            data = cursor.fetchall()
                            
                            if data:
                                print(f"\n{table} Table:")
                                for i, row in enumerate(data, start=1):
                                    print(f"| {i:^5} | {row[1]:^4} | {row[2]:^4} | {row[3]:^4} |")
                            else:
                                print(f"No data for {user_name} in the {table} Table.")
            
                    elif user_choice == '5':  # Back to Main Menu
                        break
                    
                    else:
                        print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
