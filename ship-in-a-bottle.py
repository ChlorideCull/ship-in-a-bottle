#!/usr/bin/env python3
#Ship in a Bottle - Run multiple WSGI scripts and/or bottles at the same port.
#Copyright (C) 2014 Chloride Cull
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bottle import Bottle, server_names
import argparse
import configparser
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
    paths = []
    for x in scriptconf:
        if x == "DEFAULT":
            continue

        cursc = scriptconf[x]
        print("Building ship " + x + "...")
        modified_locals = {}
        scriptpath = os.path.join(args.scripts, x)
        exec(open(scriptpath, mode="r", encoding="UTF-8").read(), globals(),
             modified_locals)
        scriptapp = modified_locals[cursc["app-var"]]

        try:
            if (not cursc["path"] in paths) and (cursc["path"] != "/"):
                mainapp.mount(cursc["path"], scriptapp)
                print(" Ship " + x + " added to path " + cursc["path"] + ".")
            else:
                willimport = True
                for y in scriptapp.routes:
                    if (y.rule, y.method) in paths:
                        print(" ERROR: " + y.method + " " +  y.rule + " ALREADY EXISTS.")
                        print(" SKIPPING SHIP")
                        willimport = False
                        break
                if willimport:
                    for y in scriptapp.routes:
                        paths.append((y.rule, y.method))
                    mainapp.merge(scriptapp)
                    print(" Ship " + x + " merged with path " + cursc["path"] + ".")
        except ValueError as e:
            print("Whoopsie! An error occured.")
            print(e)
            exit(1)

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
                           default="/etc/ship-in-a-bottle.conf", type=open)
    argparser.add_argument("--script-config", help="configuration file",
                           default="/srv/bottles/ships.conf", type=open)
    argparser.add_argument("--scripts", help="folder containing scripts",
                           default="/srv/bottles/")
    return argparser.parse_args()

def parse_config(filehandle):
    config = configparser.ConfigParser()
    config.read_file(filehandle)
    return config

if __name__ == "__main__":
    main()
