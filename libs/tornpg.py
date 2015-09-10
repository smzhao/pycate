#!/usr/bin/env python

'''
Connecting to PostgreSQL in Tornado like torndb for MySQL
Refer to another version of tornpg, which I can not find it now.
Running under Python 3 now.


Typical usage::
    db = database.Connection("server", "postdb")
    for article in db.query("SELECT * FROM posts"):
        print (posts.title)
'''

__author__ = 'bukun@osgeo.cn'

import logging
import time
import psycopg2


class Connection(object):
    def __init__(self, host, database, user=None, password=None, max_idle_time=7 * 3600):
        self.host = host
        self.database = database
        self.max_idle_time = max_idle_time

        args = "port=5432 dbname={0}".format(self.database)
        if host is not None:
            args += " host={0}".format(host)
        if user is not None:
            args += " user={0}".format(user)
        if password is not None:
            args += " password={0}".format(password)

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to PostgreSQL", self.host, exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """
        Closes this database connection.
        """
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """
        Closes the existing database connection and re-opens it.
        """
        self.close()
        self._db = psycopg2.connect(self._db_args)

    def query(self, query, *parameters):
        """
        Returns a row list for the given query and parameters.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters):
        """
        Returns the first row returned for the given query.
        """
        rows = self.query(query, *parameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]


    def execute(self, query, *parameters):
        """
        Executes the given query, returning the lastrowid from the query.
        Note:
            rowcount is a more reasonable default return value than lastrowid,
            but for historical compatibility execute() must return lastrowid.
        """
        return self.execute_lastrowid(query, *parameters)

    def execute_lastrowid(self, query, *parameters):
        """
        Executes the given query, returning the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters):
        """
        Return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """
        Return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """
        Return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """
        Return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def _ensure_connected(self):
        '''
        PostgreSQL by default closes client connections that are idle for
        8 hours, but the client library does not report this fact until
        you try to perform a query and it fails.  Protect against this
        case by preemptively closing and reopening the connection
        if it has been idle for too long (7 hours by default).
        '''
        if (self._db is None or (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters):
        try:
            # return cursor.execute(query, parameters)
            cursor.execute(query, parameters)
            return self._db.commit()
        except OperationalError:
            logging.error("Error connecting to PostgreSQL", self.host)
            self.close()
            raise


class Row(dict):
    """
    A dict that allows for object-like property access syntax.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


OperationalError = psycopg2.OperationalError
