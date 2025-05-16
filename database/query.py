from sqlite3 import connect

DB_PATH = 'database/students.db'

def get_all_students():
    conn = connect(DB_PATH)
    conn.row_factory = lambda cursor, row: {
    col[0]: row[idx] for idx, col in enumerate(cursor.description)
    }
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return students