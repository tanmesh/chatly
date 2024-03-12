import sqlite3
from entity.user import User

class UserStorage:
    def __init__(self, db_name):
        self.db_name = db_name

    def add_user(self, user):
        print(user.email, user.password, user.calendly_personal_access_token, user.calendly_user_url)
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO users VALUES (?, ?, ?, ?)''', (user.email, user.password, user.calendly_personal_access_token, user.calendly_user_url))
                conn.commit()
                print("User added successfully.")
        except sqlite3.IntegrityError:
            print("Email ID already exists in storage. Use update_user to modify.")

    def delete_user(self, email):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM users WHERE email=?''', (email,))
                conn.commit()
                print("User deleted successfully.")
        except sqlite3.IntegrityError:
            print("Error deleting user.")

    def display_users(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM users''')
                rows = cursor.fetchall()
                print("Users in storage:")
                for row in rows:
                    print("Email:", row[0])
                    print("Password:", row[1])
                    print("CalendlyPersonalAccessToken:", row[2])
                    print("CalendlyUserUrl:", row[3])
        except sqlite3.IntegrityError:
            print("Error displaying users.")

    def get_user_by_email(self, email):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM users WHERE email=?''', (email,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(user_data[0], user_data[1], user_data[2], user_data[3])
                else:
                    return None
        except sqlite3.IntegrityError:
            print("Error fetching user.")
