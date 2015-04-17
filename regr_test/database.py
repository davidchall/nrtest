from regr_test import Application, Test

import os
import sqlite3


class Database(object):
    """docstring for Database"""
    def __init__(self, path):
        self.path = path
        self.is_new = not os.path.isfile(path)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

        if self.is_new:
            self.define_schema()

    def close(self):
        self.conn.close()

    def define_schema(self):
        self.conn.execute("""
        create table application (
            name            text not null,
            version         text primary key not null,
            description     text,
            date            date default current_timestamp
        )
        """)

        self.conn.execute("""
        create table test (
            name            text primary key not null,
            version         text not null,
            description     text,
            passed          integer not null,
            log_file        text,
            duration        real,
            error_msg       text,
            application     text not null references application(version)
        )
        """)

        self.conn.execute("""
        create table output_file (
            path            text primary key not null,
            test            text not null references test(name)
        )
        """)

        self.conn.execute("""
        create table performance (
            time            real,
            cpu_usage       real,
            mem_usage       real,
            test            text not null references test(name)
        )
        """)

    def write_application(self, app):
        self.conn.execute("""
        insert into application (name, version, description)
        values (:name, :version, :description)
        """, app)

        self.conn.commit()

    def read_application(self, version):
        cursor = self.conn.cursor()

        cursor.execute("""
        select name, version, description from application where version = ?
        """, (version,))

        return Application.from_sqlite(cursor.fetchone())

    def write_test(self, app, test):
        self.conn.execute("""
        insert into test (name, version, description, passed,
            log_file, duration, error_msg, application)
        values (?, ?, ?, ?, ?, ?, ?, ?)
        """, (test.name, test.version, test.description, test.passed,
              test.log_file, test.duration, test.error_msg, app.version))

        for path in test.output_files:
            self.conn.execute("""
            insert into output_file (path, test)
            values (?, ?)
            """, (path, test.name))

        for meas in test.performance:
            self.conn.execute("""
            insert into performance (time, cpu_usage, mem_usage, test)
            values (?, ?, ?, ?)
            """, (meas.time, meas.cpu_usage, meas.mem_usage, test.name))

        self.conn.commit()

    def read_test(self, app, name):
        test_cursor = self.conn.cursor()
        file_cursor = self.conn.cursor()
        perf_cursor = self.conn.cursor()

        test_cursor.execute("""
        select * from test where application = ? order by name
        """, (app.version,))

        for test_row in test_cursor.fetchall():
            data = {k: test_row[k] for k in test_row.keys()}

            file_cursor.execute("""
                select * from output_file
                join application using (test)
                where test = ? and application = ?
                order by path
            """, (test_row['name'], app.version))

            output_files = [row['path'] for row in file_cursor.fetchall()]
            data['output_files'] = output_files


            test = Test.for_reading(data)
