#! /usr/bin/env python

import os
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def execute_cmd(cmd:str) -> int:
    print(f"{bcolors.HEADER}Execute {bcolors.BOLD}{cmd}{bcolors.ENDC}")
    is_ok = os.system(cmd)
    if is_ok != 0:
        print(f"{bcolors.FAIL}   Fail {bcolors.BOLD}{cmd}{bcolors.ENDC}")
    return is_ok


def build() -> int:
    execute_cmd("doxygen doxygen.conf")
    return execute_cmd("rsync -a --delete --progress tmp/html/ asymptote-doc --exclude .git")
    

def deploy() -> int:
    execute_cmd('git -C asymptote-doc add .')
    execute_cmd('git -C asymptote-doc commit -a -m "auto deploy"')
    execute_cmd('git -C asymptote-doc push origin master')
    return 0

def cleanup():
    execute_cmd('rm -rf tmp')
    execute_cmd('git commit -a -m "auto deploy"')
    execute_cmd('git push origin master')


def commit(msg:str):
    cmds = [
        'git -C asymptote config --local user.name FF',
        'git -C asymptote config --local user.email felixfuchsff@users.noreplay.github.com',
        f'git -C asymptote commit -a -m {msg}'
    ]
    for cmd in cmds:
        execute_cmd(cmd)


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        build()
        deploy()
        cleanup()
    elif len(argv) == 2:
        cmd = argv[1]
        if cmd == 'b':
            build()
        elif cmd == 'd':
            deploy()
        elif cmd == 'c':
            cleanup()
        else:
            raise RuntimeError(f"invalid cmd {cmd}")
    elif len(argv) == 3:
        cmd = argv[1]
        msg = argv[2]
        commit(msg)
    else:
        raise RuntimeError("ony zero or one cmd OR commit is accepted")






