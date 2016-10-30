#!/usr/bin/env python

import os
import sys
import usage
from subprocess import call, check_call
from get_open_port import get_open_udp_port


def main():
    usage.check_args(sys.argv, os.path.basename(__file__), usage.RECV_FIRST)
    option = sys.argv[1]
    src_dir = os.path.abspath(os.path.dirname(__file__))
    recv_file = os.path.join(src_dir, 'scream/ScreamServer')
    send_file = os.path.join(src_dir, 'scream/ScreamClient')
    submodule_dir = os.path.abspath(
        os.path.join(src_dir, '../third_party/sourdough'))
    code_dir = os.path.abspath(os.path.join(src_dir, 'scream/'))

    # build dependencies
    if option == 'deps':
        print 'dh-autoreconf'

    # build
    if option == 'build':
        for d in [submodule_dir, code_dir]:
            # make alone sufficient if autogen.sh and configure already run
            cmd = 'cd %s && make -j' % d
            if call(cmd, shell=True) is not 0:
                cmd = 'cd %s && ./autogen.sh && ./configure && make -j' % d
                check_call(cmd, shell=True)

    # commands to be run after building and before running
    if option == 'init':
        pass

    # who goes first
    if option == 'who_goes_first':
        print 'Receiver first'

    # receiver
    if option == 'receiver':
        port = get_open_udp_port()
        print 'Listening on port: %s' % port
        sys.stdout.flush()
        cmd = [recv_file, port]
        check_call(cmd)

    # sender
    if option == 'sender':
        ip = sys.argv[2]
        port = sys.argv[3]
        cmd = [send_file, ip, port]
        check_call(cmd)


if __name__ == '__main__':
    main()
