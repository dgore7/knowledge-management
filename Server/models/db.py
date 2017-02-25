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
            (filename   TEXT NOT NULL,
             owner      TEXT NOT NULL,
             timestamp  TEXT,
             permission INTEGER,
             notes      TEXT,
             group_id   INTEGER,
             PRIMARY KEY (filename, owner),
             FOREIGN KEY (owner)    REFERENCES USER(username),
             FOREIGN KEY (group_id) REFERENCES GROUPS(id));''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS TAG
            (tagname    TEXT PRIMARY KEY  NOT NULL);''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS GROUPS
            (id           INTEGER   PRIMARY KEY,
             groupname    TEXT,
             user_created BOOLEAN);''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS USER_GROUP
            (group_id     INTEGER,
             username     TEXT,
             FOREIGN KEY (group_id) REFERENCES GROUPS(id),
             FOREIGN KEY (username) REFERENCES USER(username));''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS FILE_TAG
            (filename     TEXT,
             tagname      TEXT,
             FOREIGN KEY (filename) REFERENCES FILE(filename) ON DELETE CASCADE,
             FOREIGN KEY (tagname)  REFERENCES TAG(tagname),
             PRIMARY KEY (filename, tagname));''')

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
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO USER(username, password) VALUES(?,?)", (username, pword))
            c.execute("INSERT INTO GROUPS(group_name) VALUES(?,?)", (username + "_personal_repo", False))
            c.execute("INSERT INTO USER_GROUP(group_id, username) VALUES(?,?)", (c.lastrowid))
            self.conn.commit()
            success = True
        # username is not unique
        except Exception as e:
             print(e)
        finally:
            self.lock.release()
            return success

    def upload(self, fileName, tags, owner, group_id):  ## Written by Ayad
        """
        This method inserts data into the database
        :param fileName:
        :param tags:
        :param owner:
        :return:
        """
        try:
            fileQuery = self.conn.execute("INSERT INTO FILE(filename, owner, timestamp) VALUES(?,?,?)",
                                          (fileName, owner, time.time()))
            for tag in tags:
                tagQuery = self.conn.execute("INSERT OR IGNORE INTO TAG VALUES(?)", (tag))
                tagNameQuery = self.conn.execute("INSERT INTO FILE_TAG(filename,tagname) VALUES(?,?)",
                                                 (fileName, tag))
            self.conn.commit()
        except sqlite3.Error as e:
            print("An Error Occured: " + e.args[0])

    def delete(self, fileName, owner):
        """
        Attempts to delete fileName from the FILES table

        :param fileName: name of file

        :return: False if file is not found
                 True if the file is found in the FILES table and is deleted
        """
        self.lock.acquire()
        total_changes = self.conn.total_changes
        try:
            cursor = self.conn.execute("""
                                       DELETE FROM FILE WHERE filename=? AND ? IN
                                       (SELECT owner FROM USER INNER JOIN
                                        (FILE INNER JOIN FILE_PERMISSION
                                         ON FILE.filename = FILE_PERMISSION.filename)
                                        ON USER.username = FILE_PERMISSION.username);
                                       """,(fileName, owner))
            self.conn.commit()
        except sqlite3.Error:
            return False
        finally:
            self.lock.release()
            if total_changes - self.conn.total_changes > 0:
                return True
            else:
                return False


    def __contains__(self, filename, owner):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT FILE.filename
                          FROM FILE
                          WHERE filename = ? AND owner = ?
                          """, (filename, owner))
        return cursor.rowcount > 0

    def search (self, query, owner):
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
                cursor.execute(
                    """SELECT FILE.filename, FILE.timestamp, TAG.tagname
                       FROM FILE INNER JOIN
                       (TAG INNER JOIN FILE_TAG
                       ON TAG.tagname = FILE_TAG.tagname)
                       ON FILE.filename = FILE_TAG.filename
                       WHERE FILE.filename LIKE ? AND FILE.owner = ?
                    """, ('%' + query['fname'] + '%', owner))
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
                                    WHERE TAG.tagname LIKE ? AND FILE.owner = ?
                                """, ('%' + tag + '%', owner))
                    results.update(row for row in cursor if row not in results)

            if 'ext' in query:
                if results:
                    results = {result for result in results if result[0].endswith(query['ext'])}
                else:
                    cursor.execute("SELECT * FROM FILE WHERE filename LIKE ? and owner", ('%' + query['ext'], owner))
        except Exception:
            raise Exception
        return results

if __name__ == '__main__':
    db = DB()
    results = db.search({'fname': 'py', 'tags': ['tag1']}, "owner")
    print(results)