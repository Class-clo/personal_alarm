import sqlite3



class Database:
    def __init__(self, database_name):
        try:
            self.database_name = database_name
            self.conn = sqlite3.connect(f"{self.database_name}.db")
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

            self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.database_name} (
                name TEXT NOT NULL UNIQUE
            )
            """)
            self.conn.commit()       #                id INTEGER PRIMARY KEY AUTOINCREMENT,

        except sqlite3.Error as e:
            print("SQLite error", e)
            raise
        except Exception as e:
            print("Something went wrong..", e)
            raise
    def __repr__(self):
        return f"Database_name('{self.database_name}')"

    def add_value(self, name):
        self.cursor.execute(
            f"INSERT OR IGNORE INTO {self.database_name} (name) VALUES (?)",
            (name, )
        )
        self.conn.commit()

    def read_all(self):
        self.cursor.execute(f"SELECT name FROM {self.database_name}")
        # row = self.cursor.fetchone()
        # print("Hello this is a test message for 'read_all_values' function")
        # return self.cursor.fetchall()
        for row in self.cursor:
            yield row["name"]

    def update_value(self, new_name, old_name):
        self.cursor.execute(f"""
            UPDATE {self.database_name}
            SET name = (?)
            WHERE name = (?)
            """, 
            (new_name, old_name)
        )
        self.conn.commit()
        if self.cursor.rowcount == 0:
            print("No matching name found")

    def delete_value(self, name):
        self.cursor.execute(
            f"DELETE FROM {self.database_name} WHERE name = ?",
            (name, )
        )
        self.conn.commit()

    def delete_all(self):
        self.cursor.execute(f"DELETE FROM {self.database_name}")
        self.conn.commit()
    
    def count_values(self):
        self.cursor.execute(
            f"SELECT COUNT(*) FROM {self.database_name}"
        )

        return self.cursor.fetchone()[0]

    def close_db(self):
        self.conn.close() #              remember to add to the last when closing manually

    def __enter__(self):  #for working with 'with' blocks: opening
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):   #for working with 'with' blocks: closing
        self.conn.close()


if __name__ == "__main__":
    print("Module being run directly")
