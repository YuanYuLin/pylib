import ops

def clone(remote_repo_path):
    CMD = ['git', 'clone', remote_repo_path]
    return ops.execCmd(CMD, ".", False, None)

def pull(local_repo_path):
    CMD = ['git', 'pull']
    return ops.execCmd(CMD, local_repo_path, False, None)

def status(local_repo_path):
    CMD = ['git', 'status']
    return ops.execCmd(CMD, local_repo_path, False, None)

def commit(local_repo_path):
    CMD = ['git', 'add', '.']
    ops.execCmd(CMD, local_repo_path, False, None)

    CMD =  ['git', 'commit']
    ops.execCmd(CMD, local_repo_path, False, None)

    CMD = ['git', 'push']
    ops.execCmd(CMD, local_repo_path, False, None)

