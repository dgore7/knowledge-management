from unittest import TestCase
from Server.models.db import DB


class TestDB(TestCase):
    def _drop_tables(self):
        '''
        utility method to reset environment
        '''
        tables = ['FILE', 'FILE_TAG', 'USER_GROUP', 'GROUPS', 'TAG', 'USER']
        c = self.db.conn.cursor()
        c.execute('PRAGMA FOREIGN_KEYS = OFF')
        try:
            for table in tables:
                c.execute('DROP TABLE {}'.format(table))
        except Exception as e:
            print('test')
        self.db.conn.commit()

    def setUp(self):
        self.db = DB()
        self.uname = 'jane doe'
        self.pword = 'password'

    def tearDown(self):
        self._drop_tables()

    def test_login(self):
        self.db.register(self.uname, self.pword)
        result = self.db.login(self.uname, self.pword)
        self.assertTrue(result)

    def test_register(self):
        self.db.register(self.uname, self.pword)
        result = self.db.conn.cursor()
        result.execute('SELECT * FROM USER')
        self.assertTupleEqual(result.fetchone()[:2],
                              (self.uname, self.pword),
                              'username and password should match those inserted')
        result.execute('SELECT * FROM GROUPS')
        group = result.fetchone()
        self.assertTupleEqual(group[1:],
                              (self.uname + ' personal_repo', 0))
        result.execute('SELECT group_id, username FROM USER_GROUP')
        self.assertTupleEqual(result.fetchone(),
                              (group[0], self.uname))

    def test_delete(self):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM TAG')
        self.db.register(self.uname, self.pword)
        cursor.execute('SELECT * FROM USER')
        user = cursor.fetchone()
        fname = 'foo.txt'
        tags = ['bar', 'baz']
        self.db.upload(fname, tags, user[0], user[2])
        res = self.db.delete(fname)
        cursor.execute('SELECT * FROM FILE')
        self.assertTrue(res)
        self.assertFalse(cursor.fetchall())
        cursor.execute('SELECT * FROM FILE_TAG')
        self.assertFalse(cursor.fetchall())

    def test_upload(self):
        self.db.register(self.uname, self.pword)
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM USER')
        user = cursor.fetchone()
        fname = 'foo.txt'
        tags = ['bar', 'baz']
        self.db.upload(fname, tags, user[0], user[2])
        cursor.execute('SELECT * FROM FILE')
        file = cursor.fetchone()
        self.assertTupleEqual(file[:2] + file[4:],  # check fname, uname, and group_id
                              (fname, self.uname, user[2]))
        cursor.execute('SELECT * FROM TAG')
        self.assertListEqual(cursor.fetchall(), [(tag,) for tag in tags])
        cursor.execute('SELECT * FROM FILE_TAG')
        self.assertListEqual(cursor.fetchall(), [(fname, user[2], tag) for tag in tags])


    def test_create_group(self):
        unames = 'jane doe', 'john smith', 'haskell curry'
        pwords = 'password', 'pword', 'passw'
        gname = 'python snakes'
        cursor = self.db.conn.cursor()
        for uname, pword in zip(unames, pwords):
            self.db.register(uname, pword)
        users_added, gid = self.db.create_group(gname, unames)
        self.assertEqual(3, users_added)
        cursor.execute('SELECT * FROM GROUPS')
        self.assertTrue((gid, gname, 1) in cursor.fetchall())
        cursor.execute('SELECT * FROM USER_GROUP WHERE group_id = 4')
        users_in_group = cursor.fetchall()
        for user in unames:
            self.assertIn((gid, user), users_in_group)

    def test_add_user_to_group(self):
        self.fail()

    def test_delete_user_from_group(self):
        self.fail()

    def test_get_personal_repo_id(self):
        self.db.register(self.uname, self.pword)
        self.assertEqual(self.db.get_personal_repo_id(self.uname), 1)

    def test_retrieve_repo(self):
        cursor = self.db.conn.cursor()
        cursor.execute('SELECT * FROM USER')
        user = cursor.fetchone()
        print(user)
        self.db.register(self.uname, self.pword)
        cursor.execute('SELECT * FROM USER')
        user = cursor.fetchone()
        print(user)
        fname = 'foo.txt'
        tags = ['bar', 'baz']
        self.db.upload(fname, tags, user[0], user[2])
        fname2 = 'snake.py'
        tags2 = ['boo', 'bla']
        self.db.upload(fname2, tags2, user[0], user[2])
        cursor.execute('SELECT * FROM FILE')
        f1 , f2 = cursor.fetchall()
        self.assertListEqual(self.db.retrieve_repo(user[2]),
                             [f1 + tuple(tags), f2 + tuple(tags2[::-1])])