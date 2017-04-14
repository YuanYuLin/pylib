import json
import imp
import os
import subprocess

def appendCmd(cmd, raw_data):
    for data in raw_data:
        cmd.append(data)
    return cmd

def execCmd(cmd_list, work_dir, debug, proc_output=subprocess.PIPE, proc_input=None):
    ret_code = 0
    DEBUG = debug
    cmd_str = ''
    response = []
    if DEBUG == False:
        if os.name == "nt":
            proc=subprocess.Popen(cmd_list, cwd=work_dir, shell=True, stdout=proc_output, stderr=subprocess.PIPE, stdin=proc_input)
        else:
            proc=subprocess.Popen(cmd_list, cwd=work_dir, stdout=proc_output, stderr=subprocess.PIPE, stdin=proc_input)

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

def loadModule(module_name, module_path):
    imp_fp, imp_pathname, imp_description = imp.find_module(module_name, module_path)
    module = imp.load_module('packageComponent', imp_fp, imp_pathname, imp_description)
    return module

