import ops
import sys
import os

def get(workspace, url):
    CMD = ['go']
    res = ops.execCmd(CMD, workspace, False, None)
    CMD = ['go', 'get', url]
    res = ops.execCmd(CMD, workspace, False, None)
    print res
    if res[2] > 0:
        sys.exit(1)
    return res

