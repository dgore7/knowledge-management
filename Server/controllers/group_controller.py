import os
import pickle

import struct

from . import db, SUCCESS, FAILURE


def addGroup(connection,group_info):
    """
    :param groupName: Takes the name of the group to add
    :param group_members: Takes the name of the group members in that group
    :param connection: Client connection
    :return:
    """
    print("Adding Group")
    gname = group_info['gname']
    membersString = group_info['members']
    members = membersString.split(',')
    for i, mem in enumerate (members):
        members[i] = mem.strip()
    result = db.create_group(gname,members)
    assert result[0] != 0
    gid = result[1]
    packed_gid = struct.pack("<L", gid)
    connection.send(packed_gid)
    print("Finished adding group: "+ gname )


def deleteGroup(connection, group_info):
    print("Deleting Group")
    gname = group_info['gname']
    members = group_info['members']
    db.delete_group(gname,members)
    print("group "+gname+" has been deleted!")


def addMember(connection,member_info):
    print("inside Add member Handler")
    gid = member_info['gid']
    uname = member_info['uname']
    user_exists = db.does_user_exists(uname)
    if not user_exists:
        connection.send(FAILURE)
        return
    result = db.add_user_to_group(gid, uname)
    if result:
        connection.send(SUCCESS)
    else:
        connection.send(FAILURE)
    print("Group Members are:" + uname)


def removeMember(connection, member_info):
    print("Inside Remove Member Handler")
    gid = member_info['gid']
    uname = member_info['uname']
    result = db.delete_user_from_group(gid,uname)
    if result:
        connection.send(SUCCESS)
    else:
        connection.send(FAILURE)
    print("Done Removing member: " + uname)


def retrieve_groups(connection, groups_info):
    if 'username' not in groups_info:
        connection.send(FAILURE)
    username = groups_info['username']
    result = db.get_groups(username)
    if result:
        connection.send(SUCCESS)
    else:
        connection.send(FAILURE)
    result = pickle.dumps(result)
    connection.send(result)



