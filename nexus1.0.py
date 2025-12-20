# NEXUS (Health Tracker) Prototype
# This is the most basic, the very first version of Nexus

import sqlite3
from datetime import datetime, timedelta

#Database Setup
conn = sqlite3.connect("nexus_proto.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS proto_prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicine_name TEXT,
    dosage TEXT,
    start_date TEXT,
    end_date TEXT,
    last_updated TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS proto_test_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_name TEXT,
    test_date TEXT,
    result_summary TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS proto_appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_name TEXT,
    appointment_date TEXT,
    appointment_time TEXT,
    purpose TEXT
)''')

cur.execute('''CREATE TABLE IF NOT EXISTS proto_details (
    details TEXT
)''')

conn.commit()

#Helper Functions
def add_prescription():
    medicine = input("Enter medicine name: ")
    dosage = input("Enter dosage: ")
    start_date = input("Enter start date (DD-MM-YYYY): ")
    end_date = input("Enter end date (DD-MM-YYYY): ")

    cur.execute("INSERT INTO proto_prescriptions (medicine_name, dosage, start_date, end_date, last_updated) VALUES (?, ?, ?, ?, ?)",
                (medicine, dosage, start_date, end_date, datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
    conn.commit()
    print("Prescription added successfully.\n")

def add_test_report():
    test_name = input("Enter test name: ")
    test_date = input("Enter test date (DD-MM-YYYY): ")
    result_summary = input("Enter result summary: ")

    cur.execute("INSERT INTO proto_test_reports (test_name, test_date, result_summary) VALUES (?, ?, ?)",
                (test_name, test_date, result_summary))
    conn.commit()
    print("Test report added successfully.\n")

def add_appointment():
    doctor_name = input("Enter doctor's name: ")
    appointment_date = input("Enter appointment date (DD-MM-YYYY): ")
    appointment_time = input("Time of the appointment: ")
    purpose = input("Enter purpose of visit: ")

    cur.execute("INSERT INTO proto_appointments (doctor_name, appointment_date, purpose) VALUES (?, ?, ?)",
                (doctor_name, appointment_date, purpose))
    conn.commit()
    print("Appointment added successfully.\n")

def view_all_records():
    print("\n Prescriptions")
    for row in cur.execute("SELECT * FROM proto_prescriptions"):
        print(f"ID: {row[0]}, Medicine: {row[1]}, Dosage: {row[2]}, Start: {row[3]}, End: {row[4]}")

    print("\n Test Reports")
    for row in cur.execute("SELECT * FROM proto_test_reports"):
        print(f"ID: {row[0]}, Test: {row[1]}, Date: {row[2]}, Result: {row[3]}")

    print("\n Appointments")
    for row in cur.execute("SELECT * FROM proto_appointments"):
        print(f"ID: {row[0]}, Doctor: {row[1]}, Date: {row[2]}, Purpose: {row[3]}")
    print()

def update_prescription():
    view_all_records()
    presc_id = input("Enter the ID of the prescription to update: ")

    new_name = input("Enter new medicine name: ")
    new_dosage = input("Enter new dosage: ")
    new_start = input("Enter new start date (DD-MM-YYYY): ")
    new_end = input("Enter new end date (DD-MM-YYYY): ")

    cur.execute('''UPDATE proto_prescriptions
                   SET medicine_name=?, dosage=?, start_date=?, end_date=?, last_updated=?
                   WHERE id=?''',
                (new_name, new_dosage, new_start, new_end, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), presc_id))
                
    conn.commit()
    print("Prescription updated successfully.")

    # Follow-up prompt
    symptom = input("Have you experienced any new symptoms after changing this medicine? (yes/no): ")
    if symptom.lower() == "yes":
        details = input("Please describe your symptoms: ")
        print("Thank you! This information can help your doctor adjust your treatment.\n")
    else:
        print("Noted. Keep monitoring your health.\n")
    
    cur.execute("INSERT INTO proto_details (details) VALUES (?)",
                (details))

def check_reminders():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    print("\n Reminders")

    # Check prescriptions
    cur.execute("SELECT medicine_name, end_date FROM proto_prescriptions")
    for med, end in cur.fetchall():
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        if today <= end_date:
            print(f" Reminder: Take your medicine '{med}' today.")
        elif end_date == tomorrow:
            print(f" Reminder: '{med}' course ends tomorrow.")

    # Check appointments
    cur.execute("SELECT doctor_name, appointment_date FROM proto_appointments")
    for doc, app_date in cur.fetchall():
        date_obj = datetime.strptime(app_date, "%Y-%m-%d").date()
        if date_obj == today:
            print(f" Reminder: Appointment with Dr. {doc} today.")
        elif date_obj == tomorrow:
            print(f" Reminder: Appointment with Dr. {doc} tomorrow.")

    print("Reminders check complete.\n")

#Main Menu Loop
def main():
    while True:
        print("""
======== NEXUS ========
1. Add new prescription
2. Add new test report
3. Add new appointment
4. View all records
5. Update prescription
6. Check reminders
7. Exit
""")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            add_prescription()
        elif choice == '2':
            add_test_report()
        elif choice == '3':
            add_appointment()
        elif choice == '4':
            view_all_records()
        elif choice == '5':
            update_prescription()
        elif choice == '6':
            check_reminders()
        elif choice == '7':
            print("Stay healthy!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.\n")

#Run Program
if __name__ == "__main__":
    main()
    conn.close()
