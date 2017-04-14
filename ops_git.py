import ops
import sys
import os

COMMIT_MSG_FILE="commit_msg"

def clone(remote_repo_path, packages_dir):
    CMD = ['git', 'clone', remote_repo_path]
    res = ops.execCmd(CMD, packages_dir, False, None)
    print packages_dir
    print res
    return res

def pull(local_repo_path):
    CMD = ['git', 'pull']
    return ops.execCmd(CMD, local_repo_path, False, None)

def status(local_repo_path):
    CMD = ['git', 'status', '-s']
    print "-Status-------------------"
    ret = ops.execCmd(CMD, local_repo_path, False, None)
    print "--------------------------"
    return ret

def latest_commit_hash(local_repo_path):
    CMD = ['git', 'log', '--pretty=format:%H', '-1']
    res = ops.execCmd(CMD, local_repo_path, False)
    commit_hash = res[0]
    return commit_hash

def get_version_from_log(local_repo_path):
    major = 1
    minor = 0
    aux = 0
    CMD = ['git', 'log', '--pretty=format:%B', '-1']
    res = ops.execCmd(CMD, local_repo_path, False)
    commit_msg = res[0]
    commit_msg_list = commit_msg.split('\n')
    for msg in commit_msg_list:
        msg = msg.strip()
        if msg.startswith('MAJOR_NUM'):
            major = int(msg.split('=')[1])
        if msg.startswith('MINOR_NUM'):
            minor = int(msg.split('=')[1])
        if msg.startswith('AUX_NUM'):
            aux = int(msg.split('=')[1])
    return [major, minor, aux]

def update_version_header(local_repo_path, major, minor, aux):
    pkg_repo = local_repo_path
    new_version_file = pkg_repo + os.sep + "version.h.new"
    old_version_file = pkg_repo + os.sep + "version.h"
    macros = []
    with open(new_version_file, 'w') as h_new_file:
        with open(old_version_file) as h_file:
            for line in h_file:
                found = 0
                line = line.strip()
                if line.startswith('#define'):
                    macros = line.split()
                    macro = macros[1]
                    if macro == 'MAJOR_NUM':
                        found = 1
                    if macro == 'MINOR_NUM':
                        found = 1
                    if macro == 'AUX_NUM':
                        found = 1

                if not found:
                    h_new_file.write(line)
                    h_new_file.write(os.linesep)

        h_new_file.write('#define MAJOR_NUM ' + str(major))
        h_new_file.write(os.linesep)
        h_new_file.write('#define MINOR_NUM ' + str(minor))
        h_new_file.write(os.linesep)
        h_new_file.write('#define AUX_NUM ' + str(aux))
        h_new_file.write(os.linesep)

    os.rename(new_version_file, old_version_file)

def read_commit_msg(local_repo_path, major, minor, aux):
    commit_msg_file = local_repo_path + os.sep + COMMIT_MSG_FILE
    if not os.path.exists(commit_msg_file):
        print "Please write the commit message in [" + commit_msg_file + "]"
        sys.exit(1)

    print "read commit message from [" + commit_msg_file + "]"
    commit_msg = ''
    commit_msg += 'MAJOR_NUM=' + str(major) + os.linesep
    commit_msg += 'MINOR_NUM=' + str(minor) + os.linesep
    commit_msg += 'AUX_NUM=' + str(aux) + os.linesep
    with open(commit_msg_file) as msg_file:
        for msg in msg_file:
            commit_msg += msg 

    return commit_msg

def get_commit_msg(local_repo_path, major, minor, aux):
    commit_msg = read_commit_msg(local_repo_path, major, minor, aux)
    return commit_msg

def commit(local_repo_path, major, minor, aux, commit_msg):
    ret = None
    pre_status = 0

    update_version_header(local_repo_path, major, minor, aux)

    CMD = ['git', 'add', '.']
    ret = ops.execCmd(CMD, local_repo_path, False, None)
    pre_status = ret[2]
    if pre_status > 0:
        print 'add failed'
        sys.exit(1)

    CMD =  ['git', 'commit', '-m', commit_msg]
    ret = ops.execCmd(CMD, local_repo_path, False, None)
    pre_status = ret[2]
    if pre_status > 0:
        print 'commit failed'
        sys.exit(1)

    CMD = ['git', 'push']
    ret = ops.execCmd(CMD, local_repo_path, False, None)
    pre_status = ret[2]
    if pre_status > 0:
        sys.exit(1)

