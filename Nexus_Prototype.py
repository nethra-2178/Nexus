#Initialize Nexus 
import sqlite3
import os
from datetime import datetime

def start_nexus():
    #Connect or create database
    db_name = "Nexus_data.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    #Create Doctors table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS nex_doctors(
            Doctor_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT,
            Contact INTEGER,
            Specialization TEXT
        )
    ''')

    #Create Patients Table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS nex_patients(
            Patient_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Email TEXT,
            Contact INTEGER,
            Gender TEXT,
            Date_of_Birth TEXT,
            Age INTEGER,
            Height REAL,
            Weight REAL,
            Blood_Group TEXT
        )
    ''')

    #Create Prescriptions Table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS nex_prescriptions (
            Prescription_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Doctor_ID INTEGER,
            Patient_ID INTEGER,
            Prescription_Title TEXT,   
            Prescription_Text TEXT,
            Prescription_Date TEXT,   
            Medicine_Details TEXT,     
            Follow_Up TEXT,
            Follow_Up_Date TEXT,
            Date_Uploaded TEXT,
            Last_Updated TEXT,
            FOREIGN KEY(Patient_ID) REFERENCES nex_patients(Patient_ID),
            FOREIGN KEY(Doctor_ID) REFERENCES nex_doctors(Doctor_ID)
        )
    ''')

    # Create Test Reports Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nex_reports(
            Test_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Patient_ID INTEGER,
            Doctor_ID INTEGER,
            Test_Name TEXT,
            Test_Date TEXT,
            Test_Center TEXT,
            Result_Summary TEXT,
            Date_Uploaded TEXT,
            FOREIGN KEY(Patient_ID) REFERENCES nex_patients(Patient_ID),
            FOREIGN KEY(Doctor_ID) REFERENCES nex_doctors(Doctor_ID)
        )
    ''')

    #Create Appointments Table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS nex_appointments(
            Appointment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Doctor_ID INTEGER,
            Patient_ID INTEGER,
            Appointment_Date TEXT,
            Appointment_Time TEXT,
            Purpose TEXT,
            FOREIGN KEY(Patient_ID) REFERENCES nex_patients(Patient_ID),
            FOREIGN KEY(Doctor_ID) REFERENCES nex_doctors(Doctor_ID)
        )
    ''')
    
    #Create Reminders Table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS nex_reminders(
            Reminder_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Doctor_ID INTEGER,
            Patient_ID INTEGER,
            Reminder_Type TEXT,
            Message TEXT,
            Time TEXT,
            Status TEXT,
            FOREIGN KEY(Patient_ID) REFERENCES nex_patients(Patient_ID),
            FOREIGN KEY(Doctor_ID) REFERENCES nex_doctors(Doctor_ID)
        )
    ''')

     # Create Doctor–Patient Link Table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS nex_doctorpatient(
            link_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Doctor_ID INTEGER,
            Patient_ID INTEGER,
            Link_Date TEXT,
            Notes TEXT,
            FOREIGN KEY(Patient_ID) REFERENCES nex_patients(Patient_ID),
            FOREIGN KEY(Doctor_ID) REFERENCES nex_doctors(Doctor_ID)
        )
    ''')
    
     #Commit, save and close
    conn.commit()
    conn.close()

def doc_patient(): 
    #connect to database
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print("Welcome to NEXUS🤍\n")

    # Ask user type
    user_type = input("Are you a Doctor or a User? (Doctor/User): ").strip().lower()

    if user_type == "doctor":
        print("\n--- Doctor Login / Registration ---\n")
        # Ask if doctor exists
        exist = input("Is this an existing doctor? (YES/NO): ").strip().lower()

        if exist == "yes":
            doc_email = input("Enter Doctor Email: ").strip()
            cursor.execute("SELECT Email, Name FROM nex_doctors WHERE Email=?", (doc_email,))

            doc = cursor.fetchone()

            if doc:
                doctor_email, doc_name = doc
                print(f"Doctor found: {doc_name}\n")
            else:
                print("No doctor found. Please create a new one.\n")
                exist = "no"  # Force new doctor entry

        if exist == "no":
            # Get Doctor Info
            print("Enter Doctor Details🩺\n")
            doc_name = input("Doctor Name: ")
            doc_email = input("Doctor Email: ")
            doc_contact = input("Doctor Contact: ")
            doc_specialization = input("Doctor Specialization: ")

            # Check if doctor exists
            cursor.execute("SELECT Doctor_ID FROM nex_doctors WHERE Email=?", (doc_email,))
            doc = cursor.fetchone()
            if doc:
                doctor_id = doc[0]
                print(f"Doctor already exists with ID {doctor_id}. Using existing entry.\n")
            else:
                cursor.execute("INSERT INTO nex_doctors (name,email,contact,specialization) VALUES (?,?,?,?)",
                               (doc_name, doc_email, doc_contact, doc_specialization))
                doctor_id = cursor.lastrowid

        # Doctor flow complete (you can later add options to add prescriptions, reminders, etc.)

    elif user_type == "user":
        print("\n--- User Details ---\n")
        # Get Patient Info
        pat_name = input("Patient Name: ")
        pat_email = input("Patient Email: ")
        pat_contact = input("Patient Contact: ")
        pat_gender = input("Gender (M/F): ")
        pat_dob = input("Date of Birth (DD-MM-YYYY): ")
        pat_age = input("Age: ")
        pat_height = input("Height (cm): ")
        pat_weight = input("Weight (kg): ")
        pat_blood_group = input("Blood Group: ")

        # Check if patient exists
        cursor.execute("SELECT patient_id FROM nex_patients WHERE email=?", (pat_email,))
        pat = cursor.fetchone()
        if pat:
            patient_id = pat[0]
            cursor.execute("""
                UPDATE nex_patients 
                SET name=?, contact=?, gender=?, date_of_birth=?, age=?, height=?, weight=?, blood_group=? 
                WHERE patient_id=?
            """, (pat_name, pat_contact, pat_gender, pat_dob, pat_age, pat_height, pat_weight, pat_blood_group, patient_id))
            print(f"\nPatient '{pat_name}' info updated successfully!\n")
        else:
            cursor.execute("""
                INSERT INTO nex_patients (name,email,contact,gender,date_of_birth,age,height,weight,blood_group) 
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (pat_name, pat_email, pat_contact, pat_gender, pat_dob, pat_age, pat_height, pat_weight, pat_blood_group))
            patient_id = cursor.lastrowid
            print(f"\nPatient '{pat_name}' added successfully!\n")

        # Optional: link patient to a doctor
        link_doctor = input("Do you want to link with a Doctor? (yes/no): ").strip().lower()
        if link_doctor == "yes":
            doc_id = input("Enter Doctor ID to link: ").strip()
            cursor.execute("SELECT name FROM nex_doctors WHERE doctor_id=?", (doc_id,))
            doc = cursor.fetchone()
            if doc:
                doc_name = doc[0]
                link_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                notes = input("Add notes for this link (optional): ")
                cursor.execute("""
                    INSERT INTO nex_doctorpatient (doctor_id, patient_id, link_date, notes)
                    VALUES (?, ?, ?, ?)
                """, (doc_id, patient_id, link_date, notes))
                print(f"\nPatient '{pat_name}' linked with Doctor '{doc_name}' successfully!\n")
            else:
                print("Doctor ID not found. Skipping link.\n")

    else:
        print("Invalid input. Please enter Doctor or Patient.")

    # Commit and close
    conn.commit()
    conn.close()

def add_prescription():
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print("\nAdd Prescription\n")
    doctor_id = input("Enter Doctor ID: ")
    patient_id = input("Enter Patient ID: ")
    title = input("Prescription Title: ")
    text = input("Prescription Notes: ")
    medicine = input("Medicine Details: ")
    follow_up = input("Follow-Up Notes (optional): ")
    follow_up_date = input("Follow-Up Date (DD-MM-YYYY, optional): ")
    prescription_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    date_uploaded = prescription_date
    last_updated = prescription_date

    cursor.execute("""
            INSERT INTO nex_prescriptions
            (Doctor_ID, Patient_ID, Prescription_Title, Prescription_Text, Medicine_Details,
            Follow_Up, Follow_Up_Date, Prescription_Date, Date_Uploaded, Last_Updated)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (doctor_id, patient_id, title, text, medicine, follow_up, follow_up_date,
            prescription_date, date_uploaded, last_updated))

    conn.commit()
    conn.close()
    print(f"Prescription for Patient ID {patient_id} added successfully!\n")

def add_appointment():
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print("\n--- Add Appointment ---\n")
    doctor_id = input("Enter Doctor ID: ")
    patient_id = input("Enter Patient ID: ")
    date = input("Appointment Date (DD-MM-YYYY): ")
    time = input("Appointment Time (HH:MM): ")
    purpose = input("Purpose: ")

    cursor.execute("""
        INSERT INTO nex_appointments
        (Doctor_ID, Patient_ID, Appointment_Date, Appointment_Time, Purpose)
        VALUES (?,?,?,?,?)
    """, (doctor_id, patient_id, date, time, purpose))

    conn.commit()
    conn.close()
    print(f"Appointment for Patient ID {patient_id} added successfully!\n")

def add_test_report():
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print("\n--- Add Test Report ---\n")
    doctor_id = input("Enter Doctor ID: ")
    patient_id = input("Enter Patient ID: ")
    test_name = input("Test Name: ")
    test_date = input("Test Date (DD-MM-YYYY): ")
    test_center = input("Test Center: ")
    result = input("Result Summary: ")
    date_uploaded = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO nex_reports
        (Patient_ID, Doctor_ID, Test_Name, Test_Date, Test_Center, Result_Summary, Date_Uploaded)
        VALUES (?,?,?,?,?,?,?)
    """, (patient_id, doctor_id, test_name, test_date, test_center, result, date_uploaded))

    conn.commit()
    conn.close()
    print(f"Test report for Patient ID {patient_id} added successfully!\n")

def add_reminder():
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print("\n--- Add Reminder ---\n")
    doctor_id = input("Enter Doctor ID: ")
    patient_id = input("Enter Patient ID: ")
    reminder_type = input("Reminder Type (Medicine/Appointment/Other): ")
    message = input("Message: ")
    time = input("Date & Time (DD-MM-YYYY HH:MM): ")
    status = "Pending"

    cursor.execute("""
        INSERT INTO nex_reminders
        (Doctor_ID, Patient_ID, Reminder_Type, Message, Time, Status)
        VALUES (?,?,?,?,?,?)
    """, (doctor_id, patient_id, reminder_type, message, time, status))

    conn.commit()
    conn.close()
    print(f"Reminder for Patient ID {patient_id} added successfully!\n")

def update_prescription():
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print("\n--- Update Prescription ---\n")

    pres_id = input("Enter Prescription ID: ")

    # Check if prescription exists
    cursor.execute("SELECT * FROM nex_prescriptions WHERE Prescription_ID=?", (pres_id,))
    data = cursor.fetchone()

    if not data:
        print("❌ No prescription found with that ID.\n")
        conn.close()
        return

    print("Prescription found! Leave a field empty if you don't want to change it.\n")

    new_medicine = input("New Medicine Details: ")
    new_followup = input("New Follow-Up Notes: ")
    new_followup_date = input("New Follow-Up Date (DD-MM-YYYY): ")

    last_updated = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cursor.execute("""
        UPDATE nex_prescriptions
        SET Medicine_Details = COALESCE(NULLIF(?, ''), Medicine_Details),
            Follow_Up = COALESCE(NULLIF(?, ''), Follow_Up),
            Follow_Up_Date = COALESCE(NULLIF(?, ''), Follow_Up_Date),
            Last_Updated = ?
        WHERE Prescription_ID = ?
    """, (new_medicine, new_followup, new_followup_date, last_updated, pres_id))

    conn.commit()
    conn.close()
    print("\n✅ Prescription updated successfully!\n")

def update_appointment():
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print("\n--- Update Appointment ---\n")

    appt_id = input("Enter Appointment ID: ")

    # Check if appointment exists
    cursor.execute("SELECT * FROM nex_appointments WHERE Appointment_ID=?", (appt_id,))
    data = cursor.fetchone()

    if not data:
        print("❌ No appointment found with that ID.\n")
        conn.close()
        return

    print("Appointment found! Leave a field empty if you don't want to change it.\n")

    new_date = input("New Date (DD-MM-YYYY): ")
    new_time = input("New Time (HH:MM): ")
    new_purpose = input("New Purpose: ")

    cursor.execute("""
        UPDATE nex_appointments
        SET Appointment_Date = COALESCE(NULLIF(?, ''), Appointment_Date),
            Appointment_Time = COALESCE(NULLIF(?, ''), Appointment_Time),
            Purpose = COALESCE(NULLIF(?, ''), Purpose)
        WHERE Appointment_ID = ?
    """, (new_date, new_time, new_purpose, appt_id))

    conn.commit()
    conn.close()
    print("\n✅ Appointment updated successfully!\n")

def view_docboard(doctor_id):
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print(f"\nDOCTOR DASHBOARD — Doctor ID: {doctor_id}\n")

    # Doctor Info
    cursor.execute("SELECT * FROM nex_doctors WHERE Doctor_ID=?", (doctor_id,))
    doc = cursor.fetchone()
    print("Doctor Details:", doc, "\n")

    # Patients linked to doctor
    print("Your Patients")
    cursor.execute("""
        SELECT p.Patient_ID, p.Name, p.Email, p.Contact
        FROM nex_patients p
        JOIN nex_doctorpatient l ON p.Patient_ID = l.Patient_ID
        WHERE l.Doctor_ID=?
    """, (doctor_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Prescriptions by this doctor
    print("Your Prescriptions")
    cursor.execute("SELECT * FROM nex_prescriptions WHERE Doctor_ID=?", (doctor_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Appointments created by this doctor
    print("Your Appointments")
    cursor.execute("SELECT * FROM nex_appointments WHERE Doctor_ID=?", (doctor_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Reports uploaded by this doctor
    print("---- Test Reports You Added ----")
    cursor.execute("SELECT * FROM nex_reports WHERE Doctor_ID=?", (doctor_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Reminders created by this doctor
    print("---- Reminders You Set ----")
    cursor.execute("SELECT * FROM nex_reminders WHERE Doctor_ID=?", (doctor_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    print("END OF DOCTOR DASHBOARD\n")
    conn.close()

def view_patboard(patient_id):
    conn = sqlite3.connect("Nexus_data.db")
    cursor = conn.cursor()

    print(f"\n========== PATIENT DASHBOARD — Patient ID: {patient_id} ==========\n")

    # Patient details
    cursor.execute("SELECT * FROM nex_patients WHERE Patient_ID=?", (patient_id,))
    pat = cursor.fetchone()
    print("Patient Details:", pat, "\n")

    # Doctors linked
    print("---- Your Doctor(s) ----")
    cursor.execute("""
        SELECT d.Doctor_ID, d.Name, d.Specialization, d.Contact
        FROM nex_doctors d
        JOIN nex_doctorpatient l ON d.Doctor_ID = l.Doctor_ID
        WHERE l.Patient_ID=?
    """, (patient_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Prescriptions for this patient
    print("---- Your Prescriptions ----")
    cursor.execute("SELECT * FROM nex_prescriptions WHERE Patient_ID=?", (patient_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Appointments for this patient
    print("---- Your Appointments ----")
    cursor.execute("SELECT * FROM nex_appointments WHERE Patient_ID=?", (patient_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Test reports for this patient
    print("---- Your Test Reports ----")
    cursor.execute("SELECT * FROM nex_reports WHERE Patient_ID=?", (patient_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    # Reminders for this patient
    print("---- Your Reminders ----")
    cursor.execute("SELECT * FROM nex_reminders WHERE Patient_ID=?", (patient_id,))
    for r in cursor.fetchall():
        print(r)
    print("\n")

    print("========== END OF PATIENT DASHBOARD ==========\n")
    conn.close()


def main_menu():
    while True:
        print("""
1. Add Doctor / Patient
2. Add Prescription
3. Add Appointment
4. Add Test Report
5. Add Reminder
6. Update Prescription
7. Update Appointment
8. View Doctor Dashboard
9. View Patient Dashboard
10. Exit
""")

        choice = input("Select an option: ")

        if choice == "1":
            doc_patient()
        elif choice == "2":
            add_prescription()
        elif choice == "3":
            add_appointment()
        elif choice == "4":
            add_test_report()
        elif choice == "5":
            add_reminder()
        elif choice == "6":
            update_prescription()
        elif choice == "7":
            update_appointment()
        elif choice == "8":
            did = input("Enter Doctor ID: ")
            view_docboard(did)
        elif choice == "9":
            pid = input("Enter Patient ID: ")
            view_patboard(pid)
        elif choice == "10":
            print("Exiting NEXUS…")
            break
        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    try:
        start_nexus()
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting NEXUS… Goodbye!")