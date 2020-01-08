#!/usr/bin/env python3
# original: https://github.com/fkt/36c3-junior-ctf-pub/tree/master/ikuchen
import re, signal, datetime
from subprocess import Popen, PIPE
from functools import partial
from socketserver import ForkingTCPServer, BaseRequestHandler
from sys import stdin, stdout, exit, argv

class RequestHandler(BaseRequestHandler):
    def handle(self):
        print(f"{datetime.datetime.now()}: session for {self.client_address[0]} started")
        fd = self.request.makefile("rwb", buffering=0)
        main(fd, fd)


def main(f_in=stdin, f_out=stdout):
    def alarm_handler(signum, frame):
        f_out.write(b"\nTimeout!\n")
        print(f"{datetime.datetime.now()}: Another timeout reached.")
        exit(15)

    # set timeout
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(20)

    # open process and greet
    proc = Popen(["python3", "-u", "-m", "IPython", "--HistoryManager.enabled=False"],
                    stdin=PIPE,stdout=f_out.fileno(),stderr=f_out.fileno())
    f_out.write(WELCOME_MSG.encode())

    while True:
        # forward "sanitized" input to IPython
        userinput = FILTER(f_in.readline().decode()).strip()
        print(f"User input: '''{userinput}'''")
        proc.stdin.write(f"{userinput}\n".encode())
        proc.stdin.flush()


if __name__ == "__main__":
    print(argv)
    PORT, REGEX= argv[-2:]
    FILTER = partial(re.compile(REGEX).sub, "")
    WELCOME_MSG = f"I'll re.sub('{REGEX}', '', your_input). GO!\n\n"
    
    print(f"Listening on port {PORT}")
    ForkingTCPServer(("0.0.0.0", int(PORT)), RequestHandler).serve_forever()
