import sqlite3
import os
import sys

# Connect to SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Error: {e}")
    return conn

# Create tables
def create_tables(conn):
    try:
        sql_create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER DEFAULT 0
        );
        """
        
        sql_create_questions_table = """
        CREATE TABLE IF NOT EXISTS questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            correct_option INTEGER NOT NULL
        );
        """
        
        cursor = conn.cursor()
        cursor.execute(sql_create_users_table)
        cursor.execute(sql_create_questions_table)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")

# Add a new user
def add_user(conn, username):
    sql = ''' INSERT INTO users(username) VALUES(?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (username,))
    conn.commit()
    return cursor.lastrowid

# Add a new question
def add_question(conn, question, option1, option2, option3, option4, correct_option):
    sql = ''' INSERT INTO questions(question, option1, option2, option3, option4, correct_option)
              VALUES(?,?,?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (question, option1, option2, option3, option4, correct_option))
    conn.commit()
    return cursor.lastrowid

# Retrieve all questions
def get_all_questions(conn):
    sql = ''' SELECT * FROM questions '''
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

# Update user score
def update_score(conn, user_id, score):
    sql = ''' UPDATE users SET score = ? WHERE user_id = ? '''
    cursor = conn.cursor()
    cursor.execute(sql, (score, user_id))
    conn.commit()

# Delete all questions
def delete_all_questions(conn):
    sql = ''' DELETE FROM questions '''
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

# Clear terminal
def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Detect if running in IDLE
def running_in_idle():
    return 'idlelib' in sys.modules

# Take a quiz
def take_quiz(conn, user_id):
    questions = get_all_questions(conn)
    total_questions = len(questions)
    print(f"There are {total_questions} questions in the quiz.\n")
    score = 0
    for question in questions:
        print(f"Q: {question[1]}")
        print(f"1. {question[2]}")
        print(f"2. {question[3]}")
        print(f"3. {question[4]}")
        print(f"4. {question[5]}")
        while True:
            try:
                answer = int(input("Your answer (1-4): "))
                if 1 <= answer <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
        if answer == question[6]:
            score += 1
        if not running_in_idle():
            clear_terminal()
    update_score(conn, user_id, score)
    print(f"You scored {score} point(s) out of {total_questions}!\n")

# Main function
def main():
    database = "quiz_system.db"

    # Create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # Create tables
        create_tables(conn)
        
        # Delete all existing questions
        delete_all_questions(conn)
        
        # Add new questions
        add_question(conn, "A function in Python begins with which keyword?", "void", "return", "def", "int", 3)
        add_question(conn, "Name the statement that sends back the value from a function?", "return", "print", "input", "None of these", 1)
        add_question(conn, 'The process of arranging the array elements in a specified order is termed as?', 'indexing', 'slicing', 'traversing', 'sorting', 4)
        add_question(conn, 'In file handling, what does the term wb+ mean?', 'read only', 'read and write', 'writing and reading in binary', 'writing in binary', 3)
        add_question(conn, 'Give the output of the following print(\'100+200\')', '300', '100+200', '100', 'None of these', 2)
        
        # Add a new user and take a quiz
        username = input("Enter Your Name: ")
        user_id = add_user(conn, username)
        if not running_in_idle():
            clear_terminal()
        print(f"Welcome, {username}!\n")
        take_quiz(conn, user_id)
    else:
        print("Error! Cannot create the database connection.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nQuiz terminated.")
        sys.exit(0)
