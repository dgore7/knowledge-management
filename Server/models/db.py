# Copyright 2016. DePaul University. All rights reserved.
# This work is distributed pursuant to the Software License
# for Community Contribution of Academic Work, dated Oct. 1, 2016.
# For terms and conditions, please see the license file, which is
# included in this distribution.

""" All the sqlite3 functions needed for querying the db (encapsulates the sql code)
    DB object used by the data_retriever"""

import sqlite3
import threading
import time


class DB:
    def __init__(self):
        # establish a connection w/ the database (check_same_thread=False is possibly sketchy, needs more research)
        self.conn = sqlite3.connect('database.db', check_same_thread=False)

        # create a lock for syncronization
        self.lock = threading.Lock()

        # create the tables if not already in DB
        self.conn.execute('''CREATE TABLE IF NOT EXISTS USER
            (username   TEXT PRIMARY KEY  NOT NULL,
             password   TEXT              NOT NULL);''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS FILE
            (filename  TEXT PRIMARY KEY  NOT NULL,
             owner     TEXT,
             timestamp TEXT,
             FOREIGN KEY (owner) REFERENCES USER(username));''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS TAG
                    (tagname    TEXT PRIMARY KEY  NOT NULL
                     );''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS FILE_TAG
                    (filename     TEXT,
                     tagname      TEXT,
                     FOREIGN KEY (filename) REFERENCES FILE(filename),
                     FOREIGN KEY (tagname)  REFERENCES TAG(tagname),
                     PRIMARY KEY (filename, tagname)
                     );''')

        self.conn.commit()

    def login(self, username, pword):
        """
        Attempts to find an entry in the USERS table with the given parameters

        :param username: username entered by user
        :param pword: password entered by user

        :return: False if username doesn't exist or incorrect password OR
                 True if username exists and enters correct password
        """

        cursor = self.conn.execute("SELECT * FROM USER WHERE username == ? AND password == ?", (username, pword))

        # user will either be the one result, or 'None'
        user = cursor.fetchone()
        if user is None:
            return False
        elif user[0] == username:
            return True

        # backup catchall if for some reason the returned username != input username
        else:
            return 0

    def register(self, username, pword):
        """
        Attempts to enter a new username and pword into the USERS table

        :param username: new username, MUST BE UNIQUE
        :param pword: new password

        :return: False if username is not unique (can't have duplicate usernames)
                 True if username is unique and user is put in db
        """
        self.lock.acquire()
        success = False
        try:
            self.conn.execute("INSERT INTO USER(username, password) VALUES(?,?)", (username, pword))
            self.conn.commit()
            success = True
        # username is not unique
        except sqlite3.IntegrityError:
             pass
        finally:
            self.lock.release()
            return success


    def upload(self, fileName, tags, owner):  ## Written by Ayad
        """
        This method inserts data into the database
        :param fileName:
        :param tags:
        :param owner:
        :return:
        """
        try:
            fileQuery = self.conn.execute("INSERT INTO FILE(filename,owner,timestamp) VALUES(?,?,?)",
                                          (fileName, owner, time.time()))
            for tag in tags:
                tagQuery = self.conn.execute("INSERT INTO TO TAG(tagname) VALUES(?) ON CONFLICT IGNORE", (tag))
                tagNameQuery = self.conn.execute("INSERT INTO FILE_TAG(filename,tagname) VALUES(?,?)",
                                                 (fileName, tag))
            self.conn.commit()
        except sqlite3.Error as e:
            print("An Error Occured: " + e.args[0])

    def delete(self,fileName):
        """
        Attempts to delete fileName from the FILES table

        :param fileName: name of file

        :return: False if file is not found
                 True if the file is found in the FILES table and is deleted
        """
        self.lock.acquire()
        total_changes = self.conn.total_changes
        try:
            cursor = self.conn.execute("DELETE FROM FILE WHERE filename=?",(fileName,))
            self.conn.commit()
        except sqlite3.Error:
            return False
        finally:
            self.lock.release()
            if total_changes - self.conn.total_changes > 0:
                return True
            else:
                return False

    def search (self, query):
        """
        Attempts to find all files matching the user's Query.

        :param query: a query supplied by the user
        :type query: dict

        :return results:  the set of rows in the format of (filename, timestamp, tagname) from the search
        """

        results = set()
        try:
            cursor = self.conn.cursor()
            if query['fname']:
                cursor.execute("""SELECT FILE.filename, FILE.timestamp, TAG.tagname
                                  FROM FILE INNER JOIN
                                  (TAG INNER JOIN FILE_TAG
                                  ON TAG.tagname = FILE_TAG.tagname)
                                  ON FILE.filename = FILE_TAG.filename
                                  WHERE FILE.filename LIKE ?
                              """, ('%' + query['fname'] + '%',))
                results.update(row for row in cursor)

            if 'tags' in query:
                tags = set(query['tags'])
                if results: # filter results (Intersection of sets)
                    results = {result for result in results if result[2] in tags}
                    # result[2] == tagname
                else: # (union of sets)
                    for tag in tags:
                        cursor.execute(
                                """ SELECT FILE.filename, FILE.timestamp, TAG.tagname
                                    FROM FILE INNER JOIN
                                    (TAG INNER JOIN FILE_TAG
                                    ON TAG.tagname = FILE_TAG.tagname)
                                    ON FILE.filename = FILE_TAG.filename
                                    WHERE TAG.tagname LIKE ?
                                """, ('%' + tag + '%',))
                    results.update(row for row in cursor if row not in results)

            if 'ext' in query:
                if results:
                    results = {result for result in results if result[0].endswith(query['ext'])}
                else:
                    cursor.execute("SELECT * FROM FILE WHERE ?  ", '%' + query['ext'])
        except Exception:
            raise Exception
        return results

if __name__ == '__main__':
    db = DB()
    results = db.search({'fname': 'py', 'tags': ['tag1']})
    print(results)