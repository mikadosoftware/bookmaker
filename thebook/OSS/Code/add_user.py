#!/usr/local/bin/python

# pbrian
# to add user to samba server, but does some checking

import commands
import sys
import crypt
from ppp import passwdgen
from ppp import db
import subprocess
import pprint



def mkpasswd():
    
    return passwdgen.genpasswd()

def get_smbuser_add_cmd(username, passwd):
    """returns command needed to *add* a smbuser, assuming
       such username already in /etc/passwd
    """
    cmd = "(echo %s; echo %s) | smbpasswd -a -s %s" % (passwd,passwd,username)
    return cmd

def get_unix_add_cmd(username,password):
    cmds = []
    cmds.append("pw adduser %s" % username)
    cmds.append("mkdir -p /home/%s" % username)
    cmds.append("chown %(u)s:%(u)s /home/%(u)s" % {'u':username})
    cmds.append("mkdir -p /DATA/_SMB_/profiles/%s" % username)
    cmds.append("chown %(u)s:%(u)s /DATA/_SMB_/profiles/%(u)s" % {'u':username})

    return cmds

def getsmbusername(fn, sn):
    """given a first second name, return a smb suitable username"""

    smbusername = fn + "." + sn

    if len(smbusername) > 15:
        smbusername = fn[:1] + "." + sn
    if len(smbusername) > 15:
        raise "This produces a smbusername > 15 characters. Must be 15 or less. %s" % smbusername

    return smbusername

def getusername():
    """ask for firstname and surname
    """

    request_string = """
  **** user add program ****
  Enter First and Second name of User.
  No quotation marks or unusual characters
first second: """

    name = raw_input(request_string)
    try:
        fn, sn = name.lower().split(" ")
    except:
        print "you must enter firstname space secondname"
        sys.exit()
    
    smbusername = getsmbusername(fn,sn)

    return (fn, sn, smbusername)

def getemailusername(fn,sn):
    """ given first and surname, return the user portion of email addr
    """
    emailusername = fn + sn[:1]
    return emailusername
    
def add_to_dbase(username, password, fullname, samba_name):
    '''create sql to add user to tbluser in COMPS
    '''
    SQL = '''INSERT INTO tbluser (username, userpassplaintext, 
             status, samba_username, fullname)
VALUES ('%s', '%s','live','%s','%s' );'''

    return SQL % (username, password, samba_name, fullname)


def apache(email, password):
    """create crypt based password necessary for apache basic auth
and return entry as expected for apache password file
    - kept in app_comps\trunk\apache
    """
    apachepass = crypt.crypt(password, 'xx')
    return r"Put this line into app_comps\trunk\apache\passwords_pirc\n %s:%s\n" % (email, apachepass)
 
def main():
    """
    get persons name, calculate the appropriate naming convention,
    add user to samba and email
    1. its not automated so...

    """

    output = """
**************
usage: this script has not done anything yet - 
it reamins for you to cut and paste the commands. 
THis is because I really have not thought about the script. 

1. add the username to samba unix
%s
2. add the username to smbpasswd
%s
3. add the user as a email user to postfix/sendmail
%s
4. Send a welcome message

"""

    fn,sn,smbusername = getusername()
    fullname = fn + ' ' + sn
    email = getemailusername(fn,sn)
    password = mkpasswd()
    unixadd = get_unix_add_cmd(smbusername, password)
    smbadd = get_smbuser_add_cmd(smbusername, password)

    stg3 = "email: %s\n" % (email)
    stg3 += "passwd: %s\n" % password 
    stg3 += "Now go to nagios:/usr/local/PIRC/CONTROL/MAIL/Users.cfg and add \
           %s %s" % (email, password)
    stg3 += "actually - just use http://nagios"

    print output % (unixadd, smbadd, stg3)
    adduserSQL = add_to_dbase(email, password, fullname, smbusername)
    print adduserSQL
    print apache(email, password)

    cmds = []
    cmds.extend(unixadd)
    cmds.append(smbadd)
    cmds.append(stg3)
    cmds.append(adduserSQL)
    cmds.append(apache(email, password))

    for cmd in cmds:
         
        print cmd,
        raw_input(' <<< cont..')
        print commands.getstatusoutput(cmd)

 
if __name__ == '__main__':
    main()

