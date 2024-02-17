import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Establish connection to MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Prathamesh",  # Replace with your MySQL password
            database="hospital_management"
        )
        print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as err:
        print("Error: ", err)

# Create tables in the database
def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Patient (
                patient_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                gender VARCHAR(10),
                contact_info VARCHAR(100),
                address VARCHAR(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Doctor (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                specialization VARCHAR(100),
                contact_info VARCHAR(100),
                address VARCHAR(255)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Appointment (
                appointment_id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT,
                doctor_id INT,
                appointment_date DATE,
                appointment_time TIME,
                status VARCHAR(20),
                FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES Doctor(doctor_id)
            )
        """)
        connection.commit()
        print("Tables created successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)

# Insert data into tables using Faker
def insert_data_using_faker(connection, num_patients, num_doctors, num_appointments):
    try:
        cursor = connection.cursor()

        # Insert fake patient data
        for _ in range(num_patients):
            cursor.execute("""
                INSERT INTO Patient (name, age, gender, contact_info, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (fake.name(), fake.random_int(min=1, max=100), random.choice(['Male', 'Female']), fake.phone_number(), fake.address()))

        # Insert fake doctor data
        for _ in range(num_doctors):
            cursor.execute("""
                INSERT INTO Doctor (name, specialization, contact_info, address)
                VALUES (%s, %s, %s, %s)
            """, (fake.name(), fake.job(), fake.phone_number(), fake.address()))

        # Insert fake appointment data
        for _ in range(num_appointments):
            appointment_date = fake.date_between(start_date='today', end_date='+30d')
            appointment_time = fake.time(pattern='%H:%M:%S')
            cursor.execute("""
                INSERT INTO Appointment (patient_id, doctor_id, appointment_date, appointment_time, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (random.randint(1, num_patients), random.randint(1, num_doctors), appointment_date, appointment_time, random.choice(['Confirmed', 'Pending'])))

        connection.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)

# Query data from tables
def query_data_Patients(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Patient")
        patients = cursor.fetchall()
        print("Patients:")
        for patient in patients:
            print(patient)

    except mysql.connector.Error as err:
        print("Error: ", err)
# Query data from tables
def query_data_Doctors(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Doctor")
        doctors = cursor.fetchall()
        print("\nDoctors:")
        for doctor in doctors:
            print(doctor)

    except mysql.connector.Error as err:
        print("Error: ", err)
# Query data from tables
def query_data_Appointments(connection):
    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Appointment")
        appointments = cursor.fetchall()
        print("\nAppointments:")
        for appointment in appointments:
            print(appointment)
    except mysql.connector.Error as err:
        print("Error: ", err)

# Update data in tables
def update_patient(connection,id,no):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE Patient
            SET contact_info = %s
            WHERE patient_id = %s
        """,(no,id))

        connection.commit()
        print("Data updated successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)
        
def update_doctor(connection,id,no):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE doctor
            SET contact_info = %s
            WHERE doctor_id = %s
        """,(no,id))
        connection.commit()
        print("Data updated successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)

# Add new patient
def add_new_patient(connection, name, age, gender, contact_info, address):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Patient (name, age, gender, contact_info, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, age, gender, contact_info, address))
        connection.commit()
        print("New patient added successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)

# Add new doctor
def add_new_doctor(connection, name, specialization, contact_info, address):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Doctor (name, specialization, contact_info, address)
            VALUES (%s, %s, %s, %s)
        """, (name, specialization, contact_info, address))
        connection.commit()
        print("New doctor added successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)

# Schedule appointment
def schedule_appointment(connection, patient_id, doctor_id, appointment_date, appointment_time, status):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Appointment (patient_id, doctor_id, appointment_date, appointment_time, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (patient_id, doctor_id, appointment_date, appointment_time, status))
        connection.commit()
        print("Appointment scheduled successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)
        
# View Appointment For Patient
def view_appointments_for_patient(connection, patient_id):
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT d.name, d.doctor_id,a.appointment_date, a.appointment_time, a.status
                FROM Appointment as a
                INNER JOIN Doctor as d ON a.doctor_id = d.doctor_id
                WHERE a.patient_id = %s
                """,(patient_id,)
            )
            appointments = cursor.fetchall()
            if appointments:
                print(f"Appointments for Patient ID {patient_id}:")
                for appointment in appointments:
                    print(appointment)
            else:
                print(f"No appointments found for Patient ID {patient_id}")
        except mysql.connector.Error as err:
            print("Error: ", err)
            
# View appointments for a doctor
def view_appointments_for_doctor(connection, doctor_id):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT DISTINCT a.appointment_id as AppointmentId,p.name as Patient_Name,a.appointment_date as Date ,a.appointment_time as Time,a.status 
            FROM Appointment as a INNER JOIN patient as p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = %s
        """, (doctor_id,))
        print(doctor_id)
        appointments = cursor.fetchall()
        if appointments:
            print(f"Appointments for Doctor ID {doctor_id}:")
            print(f"AppointmentId  PatientId")
            for appointment in appointments:
                print(appointment)
        else:
            print(f"No appointments found for Doctor ID {doctor_id}")
    except mysql.connector.Error as err:
        print("Error: ", err)

# Cancel appointment
def cancel_appointment(connection, appointment_id):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Appointment WHERE appointment_id = %s", (appointment_id,))
        connection.commit()
        print("Appointment canceled successfully")
    except mysql.connector.Error as err:
        print("Error: ", err)
        
# Main function
def main():
    connection = connect_to_database()
    while True:
        print("\n Hospital Management System ")
        print("1. Add New Patient")
        print("2. Add New Doctor")
        print("3. Schedule Appointment")
        print("4. View Doctors in Hospital")
        print("5. View Patients in Hospital")
        print("6. View total Appointments")
        print("7. Cancel Appointment")
        print("8. Update Patient Information")
        print("9. Update Doctor Information")
        print("10. View Appointments for a Patient")
        print("11. View Appointments for a Doctor")
        print("12. Insert data using faker")
        print("13. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter patient's name: ")
            age = int(input("Enter patient's age: "))
            gender = input("Enter patient's gender: ")
            contact_info = input("Enter patient's contact info: ")
            address = input("Enter patient's address: ")
            add_new_patient(connection, name, age, gender, contact_info, address)
        elif choice == '2':
            name = input("Enter doctor's name: ")
            specialization = input("Enter doctor's specialization: ")
            contact_info = input("Enter doctor's contact info: ")
            address = input("Enter doctor's address: ")
            add_new_doctor(connection, name, specialization, contact_info, address)
        elif choice == '3':
            patient_id = int(input("Enter patient ID: "))
            doctor_id = int(input("Enter doctor ID: "))
            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            appointment_time = input("Enter appointment time (HH:MM:SS): ")
            status = input("Enter appointment status: ")
            schedule_appointment(connection, patient_id, doctor_id, appointment_date, appointment_time, status)
        elif choice == '4':
            print("Total Doctors in Hospital: ")
            query_data_Doctors(connection)
        elif choice == '5':
            print("Total Patients in Hospital: ")
            query_data_Patients(connection)
        elif choice == '6':
            print("Total Appointments in Hospital: ")
            query_data_Appointments(connection)
        elif choice == '7':
            appointment_id = int(input("Enter appointment ID to cancel: "))
            cancel_appointment(connection, appointment_id)
        elif choice == '8':
            id = int(input("Enter patient ID to update: "))
            no = input("Enter new contact : ")
            update_patient(connection,id,no)
        elif choice == '9':
            id = int(input("Enter patient ID to update: "))
            no = input("Enter new contact : ")
            update_doctor(connection,id,no)
        elif choice == '10':
            patient_id = int(input("Enter patient ID: "))
            view_appointments_for_patient(connection, patient_id)
        elif choice == '11':
            doctor_id = int(input("Enter doctor ID: "))
            view_appointments_for_doctor(connection, doctor_id)
        elif choice == '12':
            insert_data_using_faker(connection,10,10,10)
            print("Inserted data")
        elif choice == '13':
            break
        else:
            print("Invalid choice. Please enter a valid option.")
    
    insert_data_using_faker(connection, 20, 10, 50)  # Example: 20 patients, 10 doctors, 50 appointments
    connection.close()

if __name__ == "__main__":
    main()