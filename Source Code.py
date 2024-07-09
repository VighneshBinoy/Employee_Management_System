import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import datetime

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname="General",
        user="postgres",
        password="Vighnesh@sql",
        host="localhost"
    )

# Create User
def create_user(username, email, password):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id;",
                (username, email, password))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

# delete user
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

# Create employee
def create_employee(e_id,name,age,sex,joining_date,salary,address,contact):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO employees (e_id,name,age,sex,joining_date,salary,address,contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (e_id,name,age,sex,joining_date,salary,address,contact))
    # employee_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return "created succesfully......."

# delete employee
def delete_employee(e_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE e_id = %s;", (e_id,))
    conn.commit()
    cur.close()
    conn.close()

# Register for Project
def register_for_project(p_id, p_name, location, e_id, d_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO project (p_id, p_name, location, e_id, d_id) VALUES (%s, %s, %s, %s, %s);", (p_id, p_name, location, e_id, d_id))
        conn.commit()
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        cur.close()
        conn.close()
        return False
    cur.close()
    conn.close()
    return True

# delete project
def delete_project(p_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM project WHERE e_id = %s;", (p_id,))
    conn.commit()
    cur.close()
    conn.close()

# Get projects
def get_projects():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM project;")
    project = cur.fetchall()
    cur.close()
    conn.close()
    return project

# Get employees
def get_employees():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM employees;")
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return employees


# Get users
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users;")
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return employees

def check_credentials(email, password):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and user['email'] == email and user['password'] == password:
        return True

def check_credentials_admin(email, password):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM admin_user WHERE email = %s;", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and user['email'] == email and user['password'] == password:
        return True

# Define user login
def user_login():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if check_credentials(email, password):
            st.success("Login successful!")
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = 'Regular'
        else:
            st.error("Invalid username or password")

# Define admin login
def admin_login():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if check_credentials_admin(email, password):
            st.success("Login successful!")
            st.session_state['logged_in'] = True
            st.session_state['user_type'] = 'Admin'
        else:
            st.error("Invalid username or password")


def login():
    st.title("Login Page")
    options = ['Regular', 'Admin']
    selected_option = st.selectbox('Select the User:', options)
    if selected_option == 'Regular':
        user_login()
    elif selected_option == 'Admin':
        admin_login()



def regular_user_app():
    # Streamlit UI
    st.title("Employee Management System")
    # Tab layout
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Create User", "Create Employee", "Create project", "View projects", "View employee Details"])

    # Create User
    with tab1:
        st.header("Create User")
        username = st.text_input("Username")
        mail = st.text_input("Email Address")
        password = st.text_input("Password (min 8 charactors)", type="password")
        if st.button("Create User"):
            user_id = create_user(username, mail, password)
            st.success(f"User created with ID: {user_id}")

    # Create employee
    with tab2:
        st.header("Create Employee")
        e_id = st.text_input("Employee id")
        name = st.text_input("Employee Name")
        age = st.text_input("Age")
        sex = st.text_input("Sex")
        joining_date = st.date_input("Joining date Date", datetime.date.today())
        salary = st.text_input("Salary")
        address = st.text_area("address")
        contact = st.text_input("Contact")
        if st.button("Create Employee"):
            employee_id = create_employee(e_id,name,age,sex,joining_date,salary,address,contact)
            st.success(f"Event created with ID: {employee_id}")

    # Create Project
    with tab3:
        st.header("create project")
        p_id = st.text_input("Project ID")
        p_name = st.text_input("Project Name")
        location = st.text_input("Location")
        e_id = st.text_input("ID of the employee incharge")
        d_id = st.text_input("Department id")
        if st.button("Create Project"):
            if register_for_project(p_id, p_name, location, e_id, d_id):
                st.success("Registered successfully")
            else:
                st.error("An Error has been occured... please check the employee id and the department id entered!!!!!")

    # View projects
    with tab4:
        st.header("View projects")
        projects = get_projects()
        for p in projects:
            st.subheader(p["p_name"])
            st.write(f"Priject ID: {p['p_id']}")
            st.write(f"Location: {p['location']}")
            st.write(f"Emlpoyee assigned(employee id): {p['e_id']}")
            st.write(f"Department(depaetment id): {p['d_id']}")
            st.write("---")
            
    # view employee details
    with tab5:
        st.header("View Employee Details")
        employees = get_employees()
        for e in employees:
            st.write(f"Employee Name : {e['name']}")
            st.write(f"Employee ID: {e['e_id']}")
            st.write("---")


def admin_user_app():
    # Streamlit UI
    st.title("Employee Management System")
    # Tab layout
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Create User", "Create Employee", "Create project", "View projects", "View employee Details","User Info"])

    # Create User
    with tab1:
        st.header("Create User")
        username = st.text_input("Username")
        mail = st.text_input("Email Address")
        password = st.text_input("Password (min 8 charactors)", type="password")
        if st.button("Create User"):
            user_id = create_user(username, mail, password)
            st.success(f"User created with ID: {user_id}")

    # Create employee
    with tab2:
        st.header("Create Employee")
        e_id = st.text_input("Employee id")
        name = st.text_input("Employee Name")
        age = st.text_input("Age")
        sex = st.text_input("Sex")
        joining_date = st.date_input("Joining date Date", datetime.date.today())
        salary = st.text_input("Salary")
        address = st.text_area("address")
        contact = st.text_input("Contact")
        if st.button("Create Employee"):
            employee_id = create_employee(e_id,name,age,sex,joining_date,salary,address,contact)
            st.success(f"Event created with ID: {employee_id}")

    # Create Project
    with tab3:
        st.header("create project")
        p_id = st.text_input("Project ID")
        p_name = st.text_input("Project Name")
        location = st.text_input("Location")
        e_id = st.text_input("ID of the employee incharge")
        d_id = st.text_input("Department id")
        if st.button("Create Project"):
            if register_for_project(p_id, p_name, location, e_id, d_id):
                st.success("Registered successfully")
            else:
                st.error("An Error has been occured... please check the employee id and the department id entered!!!!!")

    # View projects
    with tab4:
        st.header("View projects")
        projects = get_projects()
        for p in projects:
            st.subheader(p["p_name"])
            st.write(f"Priject ID: {p['p_id']}")
            st.write(f"Location: {p['location']}")
            st.write(f"Emlpoyee assigned(employee id): {p['e_id']}")
            st.write(f"Department(depaetment id): {p['d_id']}")
            if st.button(f"delete {p['p_name']}"):
                delete_project(p['p_name']) 
                st.success(f"Deleted project: {p['p_name']}")
            st.write("---")
            
    # view employee details
    with tab5:
        st.header("View Employee Details")
        employees = get_employees()
        for e in employees:
            st.write(f"Employee Name : {e['name']}")
            st.write(f"Employee ID: {e['e_id']}")
            st.write(f"Age: {e['age']}")
            st.write(f"Sex: {e['sex']}")
            st.write(f"Joining Date: {e['joining_date']}")
            st.write(f"Salary: {e['salary']}")
            st.write(f"Address: {e['address']}")
            st.write(f"Contact: {e['contact']}")
            if st.button(f"delete {e['name']}"):
                delete_employee(e['e_id']) 
                st.success(f"Deleted employee: {e['name']}")
            st.write("---")

    with tab6:
        st.header("User info")
        users = get_users()
        for user in users:
            st.subheader(user["username"])
            st.write(f"Email: {user['email']}")
            if st.button(f"Delete {user['username']}"):
                delete_user(user['id']) 
                st.success(f"Deleted user: {user['username']}")
            st.write("---")



if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_type'] = None

if st.session_state['logged_in']:
    if st.session_state['user_type'] == 'Regular':
        regular_user_app()
    elif st.session_state['user_type'] == 'Admin':
        admin_user_app()
else:
    login()
