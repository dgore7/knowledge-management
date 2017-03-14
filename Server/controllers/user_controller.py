from Server import verboseFunc
from . import db
from . import SUCCESS, FAILURE
import os
from Server import loginDecryption


@verboseFunc
def login_user(connection, login_info):
    username = login_info['username']
    login = loginDecryption.LoginDecoding(username)
    username = login.getUsername()
    password = login_info['password']
    hash_dic = db.get_hashinfo(username)
    hashed_pw = hash_dic.get("password")
    salt = hash_dic.get("salt")
    login.setSalt(salt)
    login.setAttemptedPasswordHash(password)
    login.setHashedPassword(hashed_pw)
    if login.checkPassword()==True:
        repo_id = db.login(username, hashed_pw)
        return repo_id

@verboseFunc
def register_user(register_info):
    username = register_info['username']
    password = register_info['password']
    sec_question = register_info["sec_question"]
    sec_answer = register_info["sec_answer"]
    password_salt = register_info["password_salt"]
    print("username: " + username)
    print("password: " +password)
    print ("question: " +sec_question)
    print ("answer:" + sec_answer)
    print("Leaving RegisterHandler")
    repo_id = db.register(username, password, sec_question, sec_answer, password_salt)
    print(repo_id)
    if repo_id:
        os.makedirs(
            os.path.normpath(
                os.path.join(
                    os.getcwd(),
                    'FILE_REPO',
                    username + '_personal_repo')))
    return repo_id