import paramiko


def put(name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('37.140.192.137', username='u1145099', password='Z!Hq2ukD')
    sftp = ssh.open_sftp()
    lnk = "www/bsl-show.online/push/number/" + name[1] + '.html'
    sftp.put(name[0], lnk)
    return 'https://bsl-show.online/push/number/' + name[1] + '.html'