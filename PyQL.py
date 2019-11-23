import sqlite3


class PyQL:
    # SQL shell for Python by me
    def __init__(self, connection, dbname):
        self.dbname = dbname.split("/")[-1].split(".")[0]
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.executions = []

    def insert(self, table, values, variables=[], options=""):
        # Insert row
        if variables:
            option = "(" + ", ".join(variables) + ")"
        else:
            option = ""

        values = "(" + ", ".join(map(str, values)) + ")"

        execution = f"INSERT INTO {table}{option} VALUES {values} {options}"
        self.append(execution)

        return self.execute(execution)

    def update(self, table, key, value, row=[], options=""):
        # Update table
        if row:
            condition = "WHERE " + " AND ".join(row)
        else:
            condition = ""
    
        execution = f"UPDATE {table} SET {key}={value} {condition} {options}"
        self.append(execution)

        return self.execute(execution)

    def select(self, table, columns="*", row=[], options=""):
        # Select by query
        if row:
            condition = "WHERE " + " AND ".join(row)
        else:
            condition = ""

        if type(columns) == list:
            columns = ", ".join(columns)

        execution = f"SELECT {columns} FROM {table} {condition} {options}"
        
        return self.execute(execution)

    def reindex_table(self, table):
        # Reindex table
        execution = f"REINDEX {table}"
        return self.execute(execution)

    def commit(self):
        # Commit
        self.connection.commit()

    def delete_table(self, table):
        # Delete table
        execution = f"DROP TABLE {table}"
        return self.execute(execution)

    def truncate_table(self, table):
        # Truncate table
        execution = f"DELETE FROM {table}"
        return self.execute(execution)

    def execute(self, execution):
        # Execute special query and return it result
        self.cursor.execute(execution)
        return self.cursor.fetchall()

    def import_commits(self, commits):
        # Import local commits from class (QLTableViewWindow as ex.)
        for c in commits:
            self.append(c)

    def get_commit_list(self):
        # Get self commit list
        return self.executions

    def clear_commits(self):
        # Clear commit list
        self.executions = []

    def append(self, execution):
        # Add execuion to self list
        if not self.executions or execution != self.executions[-1]:
            self.executions.append(execution)

    def add_column(self, table, column_name, data_type, default_value=""):
        # Add column (field) to a table
        execution = f"""ALTER TABLE {table}
                        ADD COLUMN {column_name}
                        {data_type} {'DEFAULT ' + default_value if default_value else ''}"""
        self.execute(execution)

    def rename_table(self, table, new_name):
        # Rename a table
        execution = f"ALTER TABLE {table} RENAME TO {new_name}"
        self.execute(execution)

    def rename_column(self, table, column, new_name):
        # Rename a column (not working in Python)
        execution = f"ALTER TABLE {table} RENAME COLUMN {column} TO {new_name}"
        print(execution)
        self.execute(execution)

    def create_table(self, table_name, columns):
        # Create table from created columns
        def prepare_field(field):
            # Preparing field description from tuple
            out = ""
            out += str(field[0]) + " "
            out += str(field[1]) + " "
            if field[2]:
                out += "DEFAULT " + field[2] + " "
            if field[3]:
                out += "PRIMARY KEY "
            if field[4]:
                out += "UNIQUE "
            return out

        execution = f"CREATE TABLE {table_name} ({', '.join(map(prepare_field, columns))})"
        self.execute(execution)

    def vacuum(self):
        # Vacuum database (isn't working in Python)
        execution = f"VACUUM {self.dbname}"
        self.execute(execution)

    def delete(self, table, row=[], options=""):
        # Delete row
        if row:
            condition = "WHERE " + " AND ".join(row)
        else:
            condition = ""

        execution = f"DELETE FROM {table} {condition} {options}"
        self.append(execution)
        self.execute(execution)

    def get_dbname(self):
        # Get name of database
        return self.dbname
