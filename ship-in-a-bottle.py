#!/usr/bin/env python3
from bottle import Bottle, server_names
import argparse
import configparser
import config
import sys
import os

def main():
    args = get_arguments()
    print("Preparing equipment...")
    mainconf = parse_config(args.main_config)
    scriptconf = parse_config(args.script_config)
    print("Bringing out the largest bottle we could find...")
    mainapp = Bottle()
    print("Building ships...")
    for x in scriptconf:
        print("Building ship " + x + "...")
        modified_locals = locals()[:]
        scriptpath = os.path.join(args.scripts, scriptconf[x]["wsgi-script"])
        exec(open(scriptpath, mode="r", encoding="UTF-8").read(), globals(),
             modified_locals)
        mainapp.mount(x, modified_locals[scriptconf[x][app-var])
    print("Preparing to finish up our bottle...")
    servername = mainconf["bottle-config"]["server"]
    if not servername in server_names:
        print("Whoopsie, we don't know any server named " + servername + ".")
        print("We know of the following ones:")
        for x in server_names:
            print("  * " + x)
        print("Are you sure it's available in this version of bottle?")
        exit(1)
    print("All sealed up and ready to go!")
    bottleconf = mainconf["bottle-config"]
    mainapp.run(server=servername, host=bottleconf["ip"],
                port=bottleconf["port"])

def get_arguments():
    argparser = argparse.ArgumentParser(description="""
    Orchestrate multiple bottles or WSGI applications!

    Ship in a Bottle is a simple, generic solution to run multiple WSGI
    applications, such as scripts created with bottle.py, under the same
    server and port.
    """)
    argparser.add_argument("--main-config", help="primary configuration",
                           default="/etc/ship-in-a-bottle.conf", type=file)
    argparser.add_argument("--script-config", help="configuration file",
                           default="/srv/bottles/ships.conf", type=file)
    argparser.add_argument("--scripts", help="folder containing scripts",
                           default="/srv/bottles/")
    return argparser.parse_args()

def parse_config(filehandle):
    config = configparser.ConfigParser()
    config.read_file(filehandle)
    return config