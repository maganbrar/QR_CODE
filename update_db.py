import sqlite3

DB_PATH = 'database/students.db'  # adjust path if different

def add_contact_column():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Try adding the contact column if it doesn't already exist
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN contact TEXT")
        print("✅ 'contact' column added successfully.")
    except sqlite3.OperationalError as e:
        if 'duplicate column name' in str(e).lower():
            print("ℹ️ Column 'contact' already exists.")
        else:
            print(f"⚠️ Error: {e}")

    conn.commit()
    conn.close()

add_contact_column()
