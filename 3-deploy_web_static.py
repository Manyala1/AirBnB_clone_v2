#!/usr/bin/env bash
# This script cleans up old archives both locally and on the web servers

from fabric.api import *

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_clean(number=0):
    """Deletes out-of-date archives"""
    number = int(number)
    if number <= 1:
        number = 1

    # Local cleanup
    local_archives = sorted(local("ls -tr versions", capture=True).split())
    local_archives = local_archives[:-(number)]

    with lcd("versions"):
        for archive in local_archives:
            local("rm -f ./{}".format(archive))

    # Remote cleanup
    with cd("/data/web_static/releases"):
        remote_archives = run("ls -tr").split()
        remote_archives = [a for a in remote_archives if "web_static_" in a]
        remote_archives = remote_archives[:-(number)]

        for archive in remote_archives:
            run("rm -rf ./{}".format(archive))
