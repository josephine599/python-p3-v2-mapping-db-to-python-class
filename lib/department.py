from __init__ import CURSOR, CONN

class Department:
    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        """Create and save a new Department."""
        department = cls(name, location)
        department.save()
        return department

    @classmethod
    def instance_from_db(cls, row):
        """Return a Department instance from a database row."""
        return cls(id=row[0], name=row[1], location=row[2])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments;"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM departments WHERE id = ?;"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name = ?;"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def save(self):
        sql = "INSERT INTO departments (name, location) VALUES (?, ?);"
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()
        self.id = CURSOR.lastrowid

    def update(self):
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        if self.id is None:
            return  # object already deleted or not saved
        sql = "DELETE FROM departments WHERE id = ?;"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        self.id = None  # reset the object id
