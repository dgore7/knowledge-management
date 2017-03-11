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
        self.conn.execute('PRAGMA FOREIGN_KEYS = ON')
        # create the tables if not already in DB
        self.conn.execute('''CREATE TABLE IF NOT EXISTS USER
            (username   TEXT PRIMARY KEY  NOT NULL,
             password   TEXT              NOT NULL,
             repo_id    INTEGER           NOT NULL,
             FOREIGN KEY (repo_id) REFERENCES GROUPS(id));''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS FILE
            (filename   TEXT NOT NULL,
             owner      TEXT NOT NULL,
             timestamp  TEXT,
             notes      TEXT,
             group_id   INTEGER,
             mod_time   INTEGER,
             PRIMARY KEY (filename, group_id),
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
             FOREIGN KEY (group_id) REFERENCES GROUPS(id) ON DELETE CASCADE,
             FOREIGN KEY (username) REFERENCES USER(username) ON DELETE CASCADE);''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS FILE_TAG
            (filename     TEXT,
             group_id     INTEGER,
             tagname      TEXT,
             FOREIGN KEY (filename, group_id) REFERENCES FILE(filename, group_id) ON DELETE CASCADE,
             FOREIGN KEY (tagname)  REFERENCES TAG(tagname) ON DELETE CASCADE ,
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

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM USER WHERE username == ? AND password == ?", (username, pword))

        # user will either be the one result, or 'None'
        user = cursor.fetchone()
        if user is None:
            return None
        elif user[0] == username:
            return user[2]

    def register(self, username, pword):
        """
        Attempts to enter a new username and pword into the USERS table

        :param username: new username, MUST BE UNIQUE
        :param pword: new password

        :return: False if username is not unique (can't have duplicate usernames)
                 True if username is unique and user is put in db
        """
        self.lock.acquire()
        result = 0
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO GROUPS(groupname, user_created) VALUES(?,?)", (username + "_personal_repo", False))
            gid = c.lastrowid
            c.execute("INSERT INTO USER(username, password, repo_id) VALUES(?,?,?)", (username, pword, gid))
            c.execute("INSERT INTO USER_GROUP(group_id, username) VALUES(?,?)", (gid, username))
            self.conn.commit()
            result = gid
        # username is not unique
        except sqlite3.Warning:
            print('ignored')
        except Exception as e:
            print('Exception in register:', e)
        finally:
            self.lock.release()
        return result

    def create_group(self, gname, members):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO GROUPS(groupname, user_created) VALUES(?,?)", (gname, True))
            gid = cursor.lastrowid
            cursor.executemany("INSERT OR IGNORE INTO USER_GROUP(group_id, username) VALUES(?,?)",
                               [(gid, member) for member in members])
            self.conn.commit()
        except sqlite3.Error as e:
            print('Error in create_group', e)
            return 0, None
        return cursor.rowcount, gid

    def add_user_to_group(self, gid, uname):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT OR IGNORE INTO USER_GROUP(group_id, username) VALUES(?,?)",
                               (gid, uname))
            self.conn.commit()
        except sqlite3.Error as e:
            print('Error in add_user_to_group', e)

        return cursor.rowcount == 1

    def delete_user_from_group(self, gid, uname):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM USER_GROUP WHERE username=? AND group_id=?",
                               (uname, gid))
            self.conn.commit()
        except sqlite3.Error as e:
            print('Error in add_user_to_group', e)
        return cursor.rowcount == 1

    def retrieve_repo(self, gid):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT * FROM FILE WHERE group_id=?",
                            (gid,))
            files = cursor.fetchall()
            result = []
            print(files)
            for file in files:
                cursor.execute('SELECT tagname FROM FILE_TAG WHERE filename=? AND group_id=?',
                               (file[0], file[4]))
                result.append(file + tuple(tag[0] for tag in cursor.fetchall()))
            return result

        except sqlite3.Error as e:
            print('Error in retrieve_repo', e)

    def get_username(self, gid):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT username FROM USER_GROUP WHERE group_id=?",
                           (gid,))
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print('Error in get_username', e)

    def repo_name(self, gid):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT groupname FROM GROUPS WHERE id=?",
                            (gid,))
            return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print('Error in repo_name', e)

    def upload(self, file_name, tags, owner, group_id, notes, mod_time):  # Written by Ayad
        """
        This method inserts data into the database
        :param mod_time:
        :param notes:
        :param group_id:
        :param file_name:
        :param tags:
        :param owner:
        :return:
        """
        try:
            self.conn.execute("""INSERT INTO
                              FILE(filename, owner, timestamp, group_id, notes, mod_time)
                              VALUES (?,?,?,?,?,?)""",
                              (file_name, owner, time.time(), group_id, notes, mod_time))
            for tag in tags:
                self.conn.execute("INSERT OR IGNORE INTO TAG VALUES(?)",
                                  (tag,))
                self.conn.execute("INSERT INTO FILE_TAG(filename, group_id, tagname) VALUES(?,?,?)",
                                  (file_name, group_id, tag))
            self.conn.commit()
        except sqlite3.Error as e:
            print("An Error Occured in upload: " + str(e.args) + "\n\t\t all vars = " + str(locals()))

    def get_personal_repo_id(self, uname):
        return self.conn.execute('SELECT repo_id FROM USER WHERE username=?', (uname,)).fetchone()[0]

    def delete(self, fname, gid):
        """
        Attempts to delete fileName from the FILES table

        :param fileName: name of file

        :return: False if file is not found
                 True if the file is found in the FILES table and is deleted
        """
        self.lock.acquire()
        cursor = self.conn.cursor()
        try:
            cursor.execute('DELETE FROM FILE WHERE filename=? AND group_id=?;', (fname, gid))
            self.conn.commit()
        except sqlite3.Error:
            return False
        finally:
            self.lock.release()
            if cursor.rowcount > 0:
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

    def search(self, query, owner):
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
                if results:  # filter results (Intersection of sets)
                    results = {result for result in results if result[2] in tags}
                    # result[2] == tagname
                else:  # (union of sets)
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
                    cursor.execute("SELECT * FROM FILE WHERE filename LIKE ? AND owner", ('%' + query['ext'], owner))
        except Exception:
            raise Exception
        return results


if __name__ == '__main__':
    db = DB()
    results = db.search({'fname': 'py', 'tags': ['tag1']}, "owner")
    print(results)
