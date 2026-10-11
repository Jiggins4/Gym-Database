import FreeSimpleGUI as sg
import mysql.connector
from mysql.connector import Error

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'gym',
    'user': 'root',
    'password': '**********'
}

# DATABASE CONNECTION

def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        sg.popup_error(f"Database Error: {e}")
        return None

# GENERIC CRUD FUNCTIONS

def get_next_id(table_name, id_column):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT COALESCE(MAX({id_column}), 0) + 1 FROM {table_name}")
            next_id = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            return next_id
        except Error as e:
            sg.popup_error(f"Error: {e}")
            return None
    return None

def get_all_records(table_name):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            
            # Convert pool_open from 1/0 to Open/Closed for display
            if table_name == 'pool_schedule':
                converted_records = []
                for record in records:
                    record_list = list(record)
                    # pool_open is at index 1
                    record_list[1] = "Open" if record_list[1] == 1 else "Closed"
                    converted_records.append(tuple(record_list))
                return converted_records
            
            cursor.close()
            connection.close()
            return records
        except Error as e:
            sg.popup_error(f"Error: {e}")
            return []
    return []

def delete_record(table_name, id_column, record_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE {id_column}=%s", (record_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Record deleted!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# MEMBERS

def add_member(fname, lname, email, phone, join_date):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            member_id = get_next_id('members', 'member_id')
            query = """INSERT INTO members (member_id, member_fname, member_lname, email, phone, join_date) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (member_id, fname, lname, email, phone, join_date))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Member added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_member(member_id, fname, lname, email, phone, join_date):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE members SET member_fname=%s, member_lname=%s, email=%s, phone=%s, join_date=%s 
                       WHERE member_id=%s"""
            cursor.execute(query, (fname, lname, email, phone, join_date, member_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Member updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# MEMBERSHIP TYPES

def add_membership_type(type_name, monthly_price, description):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            membership_id = get_next_id('membership_types', 'membership_id')
            query = """INSERT INTO membership_types (membership_id, membership_type, monthly_price, membership_description) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (membership_id, type_name, monthly_price, description))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Membership type added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_membership_type(membership_id, type_name, monthly_price, description):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE membership_types SET membership_type=%s, monthly_price=%s, membership_description=%s 
                       WHERE membership_id=%s"""
            cursor.execute(query, (type_name, monthly_price, description, membership_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Membership type updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# MEMBERSHIP RECORDS

def add_membership_record(member_id, membership_id, start_date, end_date, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            record_id = get_next_id('membership_records', 'record_id')
            # Handle empty end_date as NULL
            end_date_value = end_date if end_date.strip() else None
            query = """INSERT INTO membership_records (record_id, member_id, membership_id, start_date, end_date, membership_status) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (record_id, member_id, membership_id, start_date, end_date_value, status))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Membership record added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_membership_record(record_id, member_id, membership_id, start_date, end_date, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Handle empty end_date as NULL
            end_date_value = end_date if end_date.strip() else None
            query = """UPDATE membership_records SET member_id=%s, membership_id=%s, start_date=%s, 
                       end_date=%s, membership_status=%s WHERE record_id=%s"""
            cursor.execute(query, (member_id, membership_id, start_date, end_date_value, status, record_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Membership record updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# PAYMENTS

def add_payment(member_id, account, payment_date, payment_method):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            payment_id = get_next_id('payments', 'payment_id')
            query = """INSERT INTO payments (payment_id, member_id, member_account, payment_date, payment_method) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (payment_id, member_id, account, payment_date, payment_method))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Payment added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_payment(payment_id, member_id, account, payment_date, payment_method):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE payments SET member_id=%s, member_account=%s, payment_date=%s, 
                       payment_method=%s WHERE payment_id=%s"""
            cursor.execute(query, (member_id, account, payment_date, payment_method, payment_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Payment updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# CLASSES

def add_class(class_name, description, duration):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            class_id = get_next_id('classes', 'class_id')
            query = """INSERT INTO classes (class_id, class_name, class_description, duration_minutes) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (class_id, class_name, description, duration))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Class added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_class(class_id, class_name, description, duration):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE classes SET class_name=%s, class_description=%s, duration_minutes=%s 
                       WHERE class_id=%s"""
            cursor.execute(query, (class_name, description, duration, class_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Class updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# CLASS SCHEDULES

def add_class_schedule(class_id, instructor_id, room_id, class_date, start_time, end_time, capacity):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            schedule_id = get_next_id('class_schedule', 'class_schedule_id')
            query = """INSERT INTO class_schedule (class_schedule_id, class_id, instructor_id, room_id, class_date, start_time, end_time, capacity) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (schedule_id, class_id, instructor_id, room_id, class_date, start_time, end_time, capacity))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Class schedule added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_class_schedule(schedule_id, class_id, instructor_id, room_id, class_date, start_time, end_time, capacity):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE class_schedule SET class_id=%s, instructor_id=%s, room_id=%s, 
                       class_date=%s, start_time=%s, end_time=%s, capacity=%s WHERE class_schedule_id=%s"""
            cursor.execute(query, (class_id, instructor_id, room_id, class_date, start_time, end_time, capacity, schedule_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Class schedule updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# CLASS ENROLLMENT

def add_class_enrollment(member_id, class_schedule_id, enroll_date, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            enroll_id = get_next_id('class_enroll', 'enroll_id')
            query = """INSERT INTO class_enroll (enroll_id, member_id, class_schedule_id, enroll_date, class_status) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (enroll_id, member_id, class_schedule_id, enroll_date, status))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Enrollment added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_class_enrollment(enroll_id, member_id, class_schedule_id, enroll_date, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE class_enroll SET member_id=%s, class_schedule_id=%s, enroll_date=%s, 
                       class_status=%s WHERE enroll_id=%s"""
            cursor.execute(query, (member_id, class_schedule_id, enroll_date, status, enroll_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Enrollment updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# ROOMS

def add_room(room_name, capacity, room_type):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            room_id = get_next_id('rooms', 'room_id')
            query = """INSERT INTO rooms (room_id, room_name, capacity, room_type) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (room_id, room_name, capacity, room_type))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Room added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_room(room_id, room_name, capacity, room_type):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE rooms SET room_name=%s, capacity=%s, room_type=%s WHERE room_id=%s"""
            cursor.execute(query, (room_name, capacity, room_type, room_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Room updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# EQUIPMENT

def add_equipment(name, type_eq, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            equipment_id = get_next_id('equipment', 'equipment_id')
            query = """INSERT INTO equipment (equipment_id, equipment_name, equipment_type, equipment_status) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (equipment_id, name, type_eq, status))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Equipment added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_equipment(equipment_id, name, type_eq, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE equipment SET equipment_name=%s, equipment_type=%s, equipment_status=%s 
                       WHERE equipment_id=%s"""
            cursor.execute(query, (name, type_eq, status, equipment_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Equipment updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# EQUIPMENT MAINTENANCE

def add_equipment_maintenance(equipment_id, employee_id, maintenance_date, issue_text, cost):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            maintenance_id = get_next_id('equipment_maintenance', 'maintenance_id')
            query = """INSERT INTO equipment_maintenance (maintenance_id, equipment_id, employee_id, maintenance_date, issue_text, cost) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (maintenance_id, equipment_id, employee_id, maintenance_date, issue_text, cost))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Maintenance record added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_equipment_maintenance(maintenance_id, equipment_id, employee_id, maintenance_date, issue_text, cost):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE equipment_maintenance SET equipment_id=%s, employee_id=%s, maintenance_date=%s, 
                       issue_text=%s, cost=%s WHERE maintenance_id=%s"""
            cursor.execute(query, (equipment_id, employee_id, maintenance_date, issue_text, cost, maintenance_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Maintenance record updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# EMPLOYEES

def add_employee(fname, lname, position, hire_date):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            employee_id = get_next_id('employee', 'employee_id')
            query = """INSERT INTO employee (employee_id, fname, lname, employee_position, hire_date) 
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (employee_id, fname, lname, position, hire_date))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Employee added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_employee(employee_id, fname, lname, position, hire_date):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE employee SET fname=%s, lname=%s, employee_position=%s, hire_date=%s 
                       WHERE employee_id=%s"""
            cursor.execute(query, (fname, lname, position, hire_date, employee_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Employee updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# INSTRUCTORS

def add_instructor(employee_id, specialization, certification):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            instructor_id = get_next_id('instructor', 'instructor_id')
            query = """INSERT INTO instructor (instructor_id, employee_id, specialization, certification) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (instructor_id, employee_id, specialization, certification))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Instructor added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_instructor(instructor_id, employee_id, specialization, certification):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE instructor SET employee_id=%s, specialization=%s, certification=%s 
                       WHERE instructor_id=%s"""
            cursor.execute(query, (employee_id, specialization, certification, instructor_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Instructor updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# COURTS

def add_court(court_name, court_type, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            court_id = get_next_id('courts', 'court_id')
            query = """INSERT INTO courts (court_id, court_name, court_type, court_status) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (court_id, court_name, court_type, status))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Court added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_court(court_id, court_name, court_type, status):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE courts SET court_name=%s, court_type=%s, court_status=%s WHERE court_id=%s"""
            cursor.execute(query, (court_name, court_type, status, court_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Court updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# COURT RESERVATIONS

def add_court_reservation(court_id, member_id, reservation_date, start_time, end_time):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            reservation_id = get_next_id('court_reservation', 'reservation_id')
            query = """INSERT INTO court_reservation (reservation_id, court_id, member_id, reservation_date, start_time, end_time) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (reservation_id, court_id, member_id, reservation_date, start_time, end_time))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Reservation added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_court_reservation(reservation_id, court_id, member_id, reservation_date, start_time, end_time):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE court_reservation SET court_id=%s, member_id=%s, reservation_date=%s, 
                       start_time=%s, end_time=%s WHERE reservation_id=%s"""
            cursor.execute(query, (court_id, member_id, reservation_date, start_time, end_time, reservation_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Reservation updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# GUEST PASS

def add_guest_pass(member_id, guest_name, visit_date, check_in_time, check_out_time):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            guest_pass_id = get_next_id('guest_pass', 'guest_pass_id')
            query = """INSERT INTO guest_pass (guest_pass_id, member_id, guest_name, visit_date, check_in_time, check_out_time) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (guest_pass_id, member_id, guest_name, visit_date, check_in_time, check_out_time))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Guest pass added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_guest_pass(guest_pass_id, member_id, guest_name, visit_date, check_in_time, check_out_time):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """UPDATE guest_pass SET member_id=%s, guest_name=%s, visit_date=%s, 
                       check_in_time=%s, check_out_time=%s WHERE guest_pass_id=%s"""
            cursor.execute(query, (member_id, guest_name, visit_date, check_in_time, check_out_time, guest_pass_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Guest pass updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# POOL SCHEDULE

def add_pool_schedule(pool_open, schedule_date, start_time, end_time, activity_type, capacity):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            pool_schedule_id = get_next_id('pool_schedule', 'pool_schedule_id')
            # Convert "Open"/"Closed" string to 1/0
            pool_open_value = 1 if pool_open == "Open" else 0
            query = """INSERT INTO pool_schedule (pool_schedule_id, pool_open, schedule_date, start_time, end_time, activity_type, capacity) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (pool_schedule_id, pool_open_value, schedule_date, start_time, end_time, activity_type, capacity))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Pool schedule added!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

def update_pool_schedule(pool_schedule_id, pool_open, schedule_date, start_time, end_time, activity_type, capacity):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # Convert "Open"/"Closed" string to 1/0
            pool_open_value = 1 if pool_open == "Open" else 0
            query = """UPDATE pool_schedule SET pool_open=%s, schedule_date=%s, start_time=%s, 
                       end_time=%s, activity_type=%s, capacity=%s WHERE pool_schedule_id=%s"""
            cursor.execute(query, (pool_open_value, schedule_date, start_time, end_time, activity_type, capacity, pool_schedule_id))
            connection.commit()
            cursor.close()
            connection.close()
            return True, "Pool schedule updated!"
        except Error as e:
            return False, f"Error: {e}"
    return False, "Connection failed"

# GUI LAYOUTS

def main_menu_layout():
    layout = [
        [sg.Text("Gym Database Management System", font=("Helvetica", 20, "bold"))],
        [sg.Text("_" * 70)],
        [sg.Text("Core Tables:", font=("Helvetica", 12, "bold"))],
        [sg.Button("Members", size=(22, 1), button_color=("white", "#4CAF50")),
         sg.Button("Membership Types", size=(22, 1), button_color=("white", "#9C27B0"))],
        [sg.Button("Membership Records", size=(22, 1), button_color=("white", "#E91E63")),
         sg.Button("Payments", size=(22, 1), button_color=("white", "#FF5722"))],
        [sg.Text("_" * 70)],
        [sg.Text("Class Management:", font=("Helvetica", 12, "bold"))],
        [sg.Button("Classes", size=(22, 1), button_color=("white", "#2196F3")),
         sg.Button("Class Schedules", size=(22, 1), button_color=("white", "#03A9F4"))],
        [sg.Button("Class Enrollments", size=(22, 1), button_color=("white", "#00BCD4")),
         sg.Button("Rooms", size=(22, 1), button_color=("white", "#009688"))],
        [sg.Text("_" * 70)],
        [sg.Text("Equipment & Facilities:", font=("Helvetica", 12, "bold"))],
        [sg.Button("Equipment", size=(22, 1), button_color=("white", "#FF9800")),
         sg.Button("Equipment Maintenance", size=(22, 1), button_color=("white", "#FF6F00"))],
        [sg.Button("Courts", size=(22, 1), button_color=("white", "#673AB7")),
         sg.Button("Court Reservations", size=(22, 1), button_color=("white", "#9C27B0"))],
        [sg.Button("Pool Schedule", size=(22, 1), button_color=("white", "#3F51B5"))],
        [sg.Text("_" * 70)],
        [sg.Text("Staff:", font=("Helvetica", 12, "bold"))],
        [sg.Button("Employees", size=(22, 1), button_color=("white", "#00BCD4")),
         sg.Button("Instructors", size=(22, 1), button_color=("white", "#0097A7"))],
        [sg.Text("_" * 70)],
        [sg.Text("Other:", font=("Helvetica", 12, "bold"))],
        [sg.Button("Guest Passes", size=(22, 1), button_color=("white", "#607D8B"))],
        [sg.Text("_" * 70)],
        [sg.Button("Exit", size=(47, 1), button_color=("white", "#f44336"))]
    ]
    return layout

def simple_layout(title, headings):
    num_fields = len(headings) - 1
    layout = [
        [sg.Text(title, font=("Helvetica", 16, "bold"))],
        [sg.Text("_" * 120)],
        [sg.Table(values=[], headings=headings, key="-TABLE-",
                  auto_size_columns=False, 
                  col_widths=[12] * len(headings),
                  num_rows=12, 
                  enable_events=True,
                  justification='left')],
        [sg.Text("_" * 120)]
    ]
    return layout

def member_layout():
    layout = simple_layout("Members", ["ID", "First", "Last", "Email", "Phone", "Join Date"])
    layout.extend([
        [sg.Text("ID:", size=(18, 1)), sg.Input(key="-ID-", size=(30, 1), disabled=True)],
        [sg.Text("First Name:", size=(18, 1)), sg.Input(key="-F1-", size=(30, 1))],
        [sg.Text("Last Name:", size=(18, 1)), sg.Input(key="-F2-", size=(30, 1))],
        [sg.Text("Email:", size=(18, 1)), sg.Input(key="-F3-", size=(30, 1))],
        [sg.Text("Phone:", size=(18, 1)), sg.Input(key="-F4-", size=(30, 1))],
        [sg.Text("Join Date (YYYY-MM-DD):", size=(18, 1)), sg.Input(key="-F5-", size=(30, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def membership_type_layout():
    layout = simple_layout("Membership Types", ["ID", "Type", "Price", "Description"])
    layout.extend([
        [sg.Text("ID:", size=(18, 1)), sg.Input(key="-ID-", size=(30, 1), disabled=True)],
        [sg.Text("Type Name:", size=(18, 1)), sg.Input(key="-F1-", size=(30, 1))],
        [sg.Text("Monthly Price:", size=(18, 1)), sg.Input(key="-F2-", size=(30, 1))],
        [sg.Text("Description:", size=(18, 1)), sg.Multiline(key="-F3-", size=(30, 3))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def membership_record_layout():
    layout = simple_layout("Membership Records", ["Record ID", "Member ID", "Type ID", "Start", "End", "Status"])
    layout.extend([
        [sg.Text("Record ID:", size=(18, 1)), sg.Input(key="-ID-", size=(30, 1), disabled=True)],
        [sg.Text("Member ID:", size=(18, 1)), sg.Input(key="-F1-", size=(30, 1))],
        [sg.Text("Membership Type ID:", size=(18, 1)), sg.Input(key="-F2-", size=(30, 1))],
        [sg.Text("Start Date (YYYY-MM-DD):", size=(18, 1)), sg.Input(key="-F3-", size=(30, 1))],
        [sg.Text("End Date (YYYY-MM-DD):", size=(18, 1)), sg.Input(key="-F4-", size=(30, 1))],
        [sg.Text("Status:", size=(18, 1)), sg.Combo(["Active", "Expired", "Cancelled"], key="-F5-", size=(28, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def payment_layout():
    layout = simple_layout("Payments", ["Payment ID", "Member ID", "Account", "Date", "Method"])
    layout.extend([
        [sg.Text("Payment ID:", size=(18, 1)), sg.Input(key="-ID-", size=(30, 1), disabled=True)],
        [sg.Text("Member ID:", size=(18, 1)), sg.Input(key="-F1-", size=(30, 1))],
        [sg.Text("Account Amount:", size=(18, 1)), sg.Input(key="-F2-", size=(30, 1))],
        [sg.Text("Payment Date (YYYY-MM-DD):", size=(18, 1)), sg.Input(key="-F3-", size=(30, 1))],
        [sg.Text("Method:", size=(18, 1)), sg.Combo(["Cash", "Credit Card", "Debit Card", "Check"], key="-F4-", size=(28, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def class_layout():
    layout = simple_layout("Classes", ["Class ID", "Name", "Description", "Duration"])
    layout.extend([
        [sg.Text("Class ID:", size=(18, 1)), sg.Input(key="-ID-", size=(30, 1), disabled=True)],
        [sg.Text("Class Name:", size=(18, 1)), sg.Input(key="-F1-", size=(30, 1))],
        [sg.Text("Description:", size=(18, 1)), sg.Multiline(key="-F2-", size=(30, 3))],
        [sg.Text("Duration (min):", size=(18, 1)), sg.Input(key="-F3-", size=(30, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def class_schedule_layout():
    layout = simple_layout("Class Schedules", ["Schedule ID", "Class ID", "Instructor ID", "Room ID", "Date", "Start", "End", "Capacity"])
    layout.extend([
        [sg.Text("Schedule ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Class ID:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Instructor ID:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Room ID:", size=(15, 1)), sg.Input(key="-F3-", size=(25, 1))],
        [sg.Text("Date (YYYY-MM-DD):", size=(15, 1)), sg.Input(key="-F4-", size=(25, 1))],
        [sg.Text("Start Time (HH:MM:SS):", size=(15, 1)), sg.Input(key="-F5-", size=(25, 1))],
        [sg.Text("End Time (HH:MM:SS):", size=(15, 1)), sg.Input(key="-F6-", size=(25, 1))],
        [sg.Text("Capacity:", size=(15, 1)), sg.Input(key="-F7-", size=(25, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def class_enroll_layout():
    layout = simple_layout("Class Enrollments", ["Enroll ID", "Member ID", "Schedule ID", "Date", "Status"])
    layout.extend([
        [sg.Text("Enroll ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Member ID:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Schedule ID:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Enroll Date (YYYY-MM-DD):", size=(15, 1)), sg.Input(key="-F3-", size=(25, 1))],
        [sg.Text("Status:", size=(15, 1)), sg.Combo(["Enrolled", "Completed", "Cancelled"], key="-F4-", size=(23, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def room_layout():
    layout = simple_layout("Rooms", ["Room ID", "Name", "Capacity", "Type"])
    layout.extend([
        [sg.Text("Room ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Room Name:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Capacity:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Type:", size=(15, 1)), sg.Combo(["Studio", "Gym Floor", "Pool Area", "Court"], key="-F3-", size=(23, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def equipment_layout():
    layout = simple_layout("Equipment", ["ID", "Name", "Type", "Status"])
    layout.extend([
        [sg.Text("Equipment ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Name:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Type:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Status:", size=(15, 1)), sg.Combo(["Available", "In Use", "Maintenance"], key="-F3-", size=(23, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def equipment_maintenance_layout():
    layout = simple_layout("Equipment Maintenance", ["Maint ID", "Equip ID", "Emp ID", "Date", "Issue", "Cost"])
    layout.extend([
        [sg.Text("Maintenance ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Equipment ID:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Employee ID:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Date (YYYY-MM-DD):", size=(15, 1)), sg.Input(key="-F3-", size=(25, 1))],
        [sg.Text("Issue:", size=(15, 1)), sg.Multiline(key="-F4-", size=(25, 3))],
        [sg.Text("Cost:", size=(15, 1)), sg.Input(key="-F5-", size=(25, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def employee_layout():
    layout = simple_layout("Employees", ["ID", "First", "Last", "Position", "Hire Date"])
    layout.extend([
        [sg.Text("Employee ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("First Name:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Last Name:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Position:", size=(15, 1)), sg.Input(key="-F3-", size=(25, 1))],
        [sg.Text("Hire Date (YYYY-MM-DD):", size=(15, 1)), sg.Input(key="-F4-", size=(25, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def instructor_layout():
    layout = simple_layout("Instructors", ["ID", "Employee ID", "Specialization", "Certification"])
    layout.extend([
        [sg.Text("Instructor ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Employee ID:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Specialization:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Certification:", size=(15, 1)), sg.Input(key="-F3-", size=(25, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def court_layout():
    layout = simple_layout("Courts", ["ID", "Name", "Type", "Status"])
    layout.extend([
        [sg.Text("Court ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Court Name:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Type:", size=(15, 1)), sg.Combo(["Basketball", "Pickleball", "Multi-purpose"], key="-F2-", size=(23, 1))],
        [sg.Text("Status:", size=(15, 1)), sg.Combo(["Available", "Occupied", "Maintenance"], key="-F3-", size=(23, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def court_reservation_layout():
    layout = simple_layout("Court Reservations", ["Res ID", "Court ID", "Member ID", "Date", "Start", "End"])
    layout.extend([
        [sg.Text("Reservation ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Court ID:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Member ID:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Date (YYYY-MM-DD):", size=(15, 1)), sg.Input(key="-F3-", size=(25, 1))],
        [sg.Text("Start Time:", size=(15, 1)), sg.Input(key="-F4-", size=(25, 1))],
        [sg.Text("End Time:", size=(15, 1)), sg.Input(key="-F5-", size=(25, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def guest_pass_layout():
    layout = simple_layout("Guest Passes", ["Pass ID", "Member ID", "Guest Name", "Visit Date", "Check In", "Check Out"])
    layout.extend([
        [sg.Text("Pass ID:", size=(15, 1)), sg.Input(key="-ID-", size=(25, 1), disabled=True)],
        [sg.Text("Member ID:", size=(15, 1)), sg.Input(key="-F1-", size=(25, 1))],
        [sg.Text("Guest Name:", size=(15, 1)), sg.Input(key="-F2-", size=(25, 1))],
        [sg.Text("Visit Date (YYYY-MM-DD):", size=(15, 1)), sg.Input(key="-F3-", size=(25, 1))],
        [sg.Text("Check In Time:", size=(15, 1)), sg.Input(key="-F4-", size=(25, 1))],
        [sg.Text("Check Out Time:", size=(15, 1)), sg.Input(key="-F5-", size=(25, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

def pool_schedule_layout():
    layout = simple_layout("Pool Schedule", ["ID", "Status", "Date", "Start Time", "End Time", "Activity", "Capacity"])
    layout.extend([
        [sg.Text("Schedule ID:", size=(18, 1)), sg.Input(key="-ID-", size=(30, 1), disabled=True)],
        [sg.Text("Pool Status:", size=(18, 1)), sg.Combo(["Open", "Closed"], key="-F1-", size=(28, 1))],
        [sg.Text("Date (YYYY-MM-DD):", size=(18, 1)), sg.Input(key="-F2-", size=(30, 1))],
        [sg.Text("Start Time (HH:MM:SS):", size=(18, 1)), sg.Input(key="-F3-", size=(30, 1))],
        [sg.Text("End Time (HH:MM:SS):", size=(18, 1)), sg.Input(key="-F4-", size=(30, 1))],
        [sg.Text("Activity Type:", size=(18, 1)), sg.Input(key="-F5-", size=(30, 1))],
        [sg.Text("Capacity:", size=(18, 1)), sg.Input(key="-F6-", size=(30, 1))],
        [sg.Button("Add"), sg.Button("Update"), sg.Button("Delete"), sg.Button("Refresh"), sg.Button("Back")]
    ])
    return layout

# WINDOW MANAGER

def manage_table(table_config):
    window = sg.Window(table_config['title'], table_config['layout'](), size=(1100, 850), finalize=True, resizable=True)
    
    # Load data
    data = get_all_records(table_config['table_name'])
    window["-TABLE-"].update(values=data)
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == "Back":
            window.close()
            return
        
        if event == "Refresh":
            data = get_all_records(table_config['table_name'])
            window["-TABLE-"].update(values=data)
        
        if event == "Add":
            field_values = [values[f"-F{i}-"] for i in range(1, table_config['num_fields'] + 1)]
            
            # Validate all fields filled
            if all(str(v).strip() for v in field_values):
                success, msg = table_config['add_func'](*field_values)
                sg.popup(msg)
                if success:
                    data = get_all_records(table_config['table_name'])
                    window["-TABLE-"].update(values=data)
                    # Clear fields
                    for i in range(1, table_config['num_fields'] + 1):
                        try:
                            window[f"-F{i}-"].update("")
                        except:
                            pass
            else:
                sg.popup("Please fill all fields")
        
        if event == "Update" and table_config.get('update_func'):
            record_id = values["-ID-"]
            if record_id:
                field_values = [values[f"-F{i}-"] for i in range(1, table_config['num_fields'] + 1)]
                if all(str(v).strip() for v in field_values):
                    success, msg = table_config['update_func'](record_id, *field_values)
                    sg.popup(msg)
                    if success:
                        data = get_all_records(table_config['table_name'])
                        window["-TABLE-"].update(values=data)
                else:
                    sg.popup("Please fill all fields")
            else:
                sg.popup("Please select a record first")
        
        if event == "Delete":
            record_id = values["-ID-"]
            if record_id:
                confirm = sg.popup_yes_no("Delete this record?")
                if confirm == "Yes":
                    success, msg = delete_record(table_config['table_name'], 
                                                table_config['id_column'], record_id)
                    sg.popup(msg)
                    if success:
                        data = get_all_records(table_config['table_name'])
                        window["-TABLE-"].update(values=data)
                        window["-ID-"].update("")
                        for i in range(1, table_config['num_fields'] + 1):
                            try:
                                window[f"-F{i}-"].update("")
                            except:
                                pass
            else:
                sg.popup("Select a record to delete")
        
        if event == "-TABLE-":
            if values["-TABLE-"]:
                row = data[values["-TABLE-"][0]]
                window["-ID-"].update(row[0])
                for i in range(1, min(len(row), table_config['num_fields'] + 1)):
                    try:
                        window[f"-F{i}-"].update(row[i])
                    except:
                        pass

# MAIN

def main():
    sg.theme("DarkBlue3")
    window = sg.Window("Gym Database", main_menu_layout(), size=(600, 750))
    
    tables = {
        'Members': {
            'title': 'Members',
            'layout': member_layout,
            'table_name': 'members',
            'id_column': 'member_id',
            'num_fields': 5,
            'add_func': add_member,
            'update_func': update_member
        },
        'Membership Types': {
            'title': 'Membership Types',
            'layout': membership_type_layout,
            'table_name': 'membership_types',
            'id_column': 'membership_id',
            'num_fields': 3,
            'add_func': add_membership_type,
            'update_func': update_membership_type
        },
        'Membership Records': {
            'title': 'Membership Records',
            'layout': membership_record_layout,
            'table_name': 'membership_records',
            'id_column': 'record_id',
            'num_fields': 5,
            'add_func': add_membership_record,
            'update_func': update_membership_record
        },
        'Payments': {
            'title': 'Payments',
            'layout': payment_layout,
            'table_name': 'payments',
            'id_column': 'payment_id',
            'num_fields': 4,
            'add_func': add_payment,
            'update_func': update_payment
        },
        'Classes': {
            'title': 'Classes',
            'layout': class_layout,
            'table_name': 'classes',
            'id_column': 'class_id',
            'num_fields': 3,
            'add_func': add_class,
            'update_func': update_class
        },
        'Class Schedules': {
            'title': 'Class Schedules',
            'layout': class_schedule_layout,
            'table_name': 'class_schedule',
            'id_column': 'class_schedule_id',
            'num_fields': 7,
            'add_func': add_class_schedule,
            'update_func': update_class_schedule
        },
        'Class Enrollments': {
            'title': 'Class Enrollments',
            'layout': class_enroll_layout,
            'table_name': 'class_enroll',
            'id_column': 'enroll_id',
            'num_fields': 4,
            'add_func': add_class_enrollment,
            'update_func': update_class_enrollment
        },
        'Rooms': {
            'title': 'Rooms',
            'layout': room_layout,
            'table_name': 'rooms',
            'id_column': 'room_id',
            'num_fields': 3,
            'add_func': add_room,
            'update_func': update_room
        },
        'Equipment': {
            'title': 'Equipment',
            'layout': equipment_layout,
            'table_name': 'equipment',
            'id_column': 'equipment_id',
            'num_fields': 3,
            'add_func': add_equipment,
            'update_func': update_equipment
        },
        'Equipment Maintenance': {
            'title': 'Equipment Maintenance',
            'layout': equipment_maintenance_layout,
            'table_name': 'equipment_maintenance',
            'id_column': 'maintenance_id',
            'num_fields': 5,
            'add_func': add_equipment_maintenance,
            'update_func': update_equipment_maintenance
        },
        'Employees': {
            'title': 'Employees',
            'layout': employee_layout,
            'table_name': 'employee',
            'id_column': 'employee_id',
            'num_fields': 4,
            'add_func': add_employee,
            'update_func': update_employee
        },
        'Instructors': {
            'title': 'Instructors',
            'layout': instructor_layout,
            'table_name': 'instructor',
            'id_column': 'instructor_id',
            'num_fields': 3,
            'add_func': add_instructor,
            'update_func': update_instructor
        },
        'Courts': {
            'title': 'Courts',
            'layout': court_layout,
            'table_name': 'courts',
            'id_column': 'court_id',
            'num_fields': 3,
            'add_func': add_court,
            'update_func': update_court
        },
        'Court Reservations': {
            'title': 'Court Reservations',
            'layout': court_reservation_layout,
            'table_name': 'court_reservation',
            'id_column': 'reservation_id',
            'num_fields': 5,
            'add_func': add_court_reservation,
            'update_func': update_court_reservation
        },
        'Guest Passes': {
            'title': 'Guest Passes',
            'layout': guest_pass_layout,
            'table_name': 'guest_pass',
            'id_column': 'guest_pass_id',
            'num_fields': 5,
            'add_func': add_guest_pass,
            'update_func': update_guest_pass
        },
        'Pool Schedule': {
            'title': 'Pool Schedule',
            'layout': pool_schedule_layout,
            'table_name': 'pool_schedule',
            'id_column': 'pool_schedule_id',
            'num_fields': 6,
            'add_func': add_pool_schedule,
            'update_func': update_pool_schedule
        }
    }
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        
        if event in tables:
            window.hide()
            manage_table(tables[event])
            window.un_hide()
    
    window.close()

if __name__ == "__main__":
    main()