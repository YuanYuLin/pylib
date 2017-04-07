import json
import os
import subprocess

def appendCmd(cmd, raw_data):
    for data in raw_data:
        cmd.append(data)
    return cmd

def execCmd(cmd_list, work_dir, debug, proc_output=subprocess.PIPE):
    DEBUG = debug
    cmd_str = ''
    response = []
    if DEBUG == False:
        if os.name == "nt":
            proc=subprocess.Popen(cmd_list, cwd=work_dir, shell=True, stdout=proc_output, stderr=proc_output)
        else:
            proc=subprocess.Popen(cmd_list, cwd=work_dir, stdout=proc_output, stderr=proc_output)

        if proc_output == subprocess.PIPE:
            response = proc.communicate()

        proc.wait()

        if proc_output == subprocess.PIPE:
            if response[0] :
                print "    *" + response[0]
            if response[1] :
                print "    *" + response[1]

    if DEBUG == True:
        for cmd in cmd_list:
            cmd_str += cmd + ' '
        print cmd_str

    return response

def loadJson2Obj(script):
    with open(script) as fd:
        data = json.load(fd)
    return data

