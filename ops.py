import json
import hashlib
import imp
import os
import sys
import subprocess
import shutil
import tarfile
import lzma
import contextlib

def path_join(src, src2):
    return src + "/" + src2
#    return os.path.join(src, src2)

def ln(workspace, src, dst):
    CMD = ['ln', '-s', src, dst]
    execCmd(CMD, workspace, False, None)
    
def sudo_copyto(src, dst, workspace = None):
    CMD = ['sudo', 'cp', '-avr', src, dst]
    if workspace == None:
        res = execCmd(CMD, ".", False, None)
    else:
        res = execCmd(CMD, workspace, False, None)
    if res[2] > 0:
        print "error:", res
        sys.exit(1)

def copyto(src, dst, workspace = None):
    CMD = ['cp', '-avr', src, dst]
    if workspace == None:
        res = execCmd(CMD, ".", False, None)
    else:
        res = execCmd(CMD, workspace, False, None)
    if res[2] > 0:
        print "error:", res
        sys.exit(1)
    #shutil.copyfile(src, dst)

def rm_file(src, workspace = None):
    CMD = ['rm', '-f', src]
    if workspace == None:
        res = execCmd(CMD, ".", False, None)
    else:
        res = execCmd(CMD, workspace, False, None)
    if res[2] > 0:
        print "error:", res
        sys.exit(1)

def isExist(path):
    if os.path.exists(path):
        return True
    else:
        return False

def touch(file_name, time_stamp=None):
    with open(file_name, 'a'):
        os.utime(file_name, time_stamp)

def pkg_mkdir(pkg_path, dir_path):
    abspath = os.path.abspath(pkg_path + os.sep + dir_path)
    if not os.path.exists(abspath):
        os.makedirs(abspath)
    return abspath

def mknod_block(pkg_path, dev_name, dev_major, dev_minor):
    CMD = ['sudo', 'mknod', '-m', '660', dev_name, 'b', dev_major, dev_minor]
    res = execCmd(CMD, pkg_path, False, None)
    print res
    if res[2] != 0:
        sys.exit(1)

def mknod_char(pkg_path, dev_name, dev_major, dev_minor):
    CMD = ['sudo', 'mknod', '-m', '660', dev_name, 'c', dev_major, dev_minor]
    res = execCmd(CMD, pkg_path, False, None)
    print res
    if res[2] != 0:
        sys.exit(1)

def sudo_mkdir(dir_path, workspace=None):
    if not os.path.exists(dir_path):
        CMD = ['sudo', 'mkdir', '-p', dir_path]
        execCmd(CMD, ".", False, None)
        #os.mkdir(dir_path)

def mkdir(dir_path, workspace=None):
    if not os.path.exists(dir_path):
        CMD = ['mkdir', '-p', dir_path]
        execCmd(CMD, ".", False, None)
        #os.mkdir(dir_path)

def appendCmd(cmd, raw_data):
    for data in raw_data:
        cmd.append(data)
    return cmd

def execCmd(raw_cmd_list, work_dir, debug, proc_output=subprocess.PIPE, proc_input=None, env_config=None):
    cmd_list = []
    for cmd_arg in raw_cmd_list:
        cmd_list.append(str(cmd_arg))
    ret_code = 0
    DEBUG = debug
    cmd_str = ''
    response = []
    tmp_response = []
    if DEBUG == False:
        if os.name == "nt":
            proc=subprocess.Popen(cmd_list, cwd=work_dir, shell=True, stdout=proc_output, stderr=subprocess.PIPE, stdin=proc_input, env=env_config)
        else:
            proc=subprocess.Popen(cmd_list, cwd=work_dir, stdout=proc_output, stderr=subprocess.PIPE, stdin=proc_input, env=env_config)

        #if proc_output == subprocess.PIPE:
        tmp_response = proc.communicate()

        ret_code = proc.wait()

        #if proc_output == subprocess.PIPE:
        #    if tmp_response[0] :
        #        print "    *" + tmp_response[0]
        #    if tmp_response[1] :
        #        print "    *" + tmp_response[1]

    response = list(tmp_response)
    response.append(ret_code)

    if DEBUG == True:
        for cmd in cmd_list:
            cmd_str += cmd + ' '
        print cmd_str

    return response

def loadJson2Obj(script):
    with open(script) as fd:
        data = json.load(fd)
    return data

def loadModule(module_name, module_file, module_path):
    imp_fp, imp_pathname, imp_description = imp.find_module(module_file, module_path)
    module = imp.load_module(module_name, imp_fp, imp_pathname, imp_description)
    return module

def getEnv(key):
    return os.environ[key]

def exportEnv(env_list):
    for env in env_list:
        key = env
        val = env_list[env]
        os.environ[key] = val

def addEnv(key, val):
    env = {}
    env_val = os.environ[key]
    env[key] = env_val + ";" + val

    return env

def setEnv(key, val):
    env = {}
    env[key] = val
    return env

def splitFile(workspace, file_name, split_size, split_prefix, split_postfix):
    split_file_name = split_prefix + file_name + split_postfix
    CMD = ['split', '--verbose', '-d', '-b', split_size, file_name, split_file_name]
    return execCmd(CMD, workspace, False)

def mergeFiles(workspace, output_file_name, file_list):
    fp = file(path_join(workspace, output_file_name), 'wb')
    for file_name in file_list:
        with open(path_join(workspace, file_name)) as src_file:
            fp.write(src_file.read())
    fp.close()

    return path_join(workspace, output_file_name)

def file_md5_str(full_file_name):
    hash_md5 = hashlib.md5()
    with open(full_file_name) as fp:
        for chunk in iter(lambda: fp.read(4096), b""):
            hash_md5.update(chunk)
    return str(hash_md5.hexdigest())

def unTarBz2SUDO(src_file, dst_dir):
    if not os.path.exists(dst_dir):
        CMD = ['sudo', 'mkdir', '-p', dst_dir]
        execCmd(CMD, ".", False, None)
    CMD = ['sudo', 'tar', 'jxvf', src_file, '-C', dst_dir]
    execCmd(CMD, dst_dir, False, None)

def unTarBz2(src_file, dst_dir):
    CMD = ['tar', 'jxvf', src_file, '-C', dst_dir]
    execCmd(CMD, dst_dir, False, None)
    #bz2 = tarfile.open(src_file)
    #bz2.extractall(dst_dir)
    #bz2.close()

def unTarGzSUDO(src_file, dst_dir):
    if not os.path.exists(dst_dir):
        CMD = ['sudo', 'mkdir', '-p', dst_dir]
        execCmd(CMD, ".", False, None)
    CMD = ['sudo', 'tar', 'zxvf', src_file, '-C', dst_dir]
    execCmd(CMD, dst_dir, False, None)
 
def unTarGz(src_file, dst_dir):
    CMD = ['tar', 'zxvf', src_file, '-C', dst_dir]
    execCmd(CMD, dst_dir, False, None)

def unTarXzSUDO(src_file, dst_dir):
    if not os.path.exists(dst_dir):
        CMD = ['sudo', 'mkdir', '-p', dst_dir]
        execCmd(CMD, ".", False, None)
    CMD = ['sudo', 'tar', 'Jxvf', src_file, '-C', dst_dir]
    execCmd(CMD, dst_dir, False, None)

def unTarXz(src_file, dst_dir):
    CMD = ['tar', 'Jxvf', src_file, '-C', dst_dir]
    execCmd(CMD, dst_dir, False, None)
    '''
    with contextlib.closing(lzma.LZMAFile(src_file)) as xz:
        with tarfile.open(fileobj=xz) as f:
            f.extractall(dst_dir)
    '''

def kbuild_config_replace(config_file, key, new_value):
    src_config_file = config_file + '.src'
    dst_config_file = config_file + '.dst'
    copyto(config_file, src_config_file)
    with open(src_config_file) as in_cfg, open(dst_config_file, 'w') as out_cfg:
        for line in in_cfg:
            if line.startswith(key + "="):
                line = line.replace("<#CONFIG_VALUE#>", new_value)
            out_cfg.write(line)

    copyto(dst_config_file, config_file)
    rm_file(src_config_file)
    rm_file(dst_config_file)

