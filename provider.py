#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import re

import pexpect
from pexpect.exceptions import TIMEOUT

# Don't do this unless you like being John Malkovich
# c = pexpect.spawnu('/usr/bin/env python ./python.py')

# Note that, for Python 3 compatibility reasons, we are using spawnu and
# importing unicode_literals (above). spawnu accepts Unicode input and
# unicode_literals makes all string literals in this script Unicode by default.

class PythonProvider:
    def __init__(self):
        self._connections = {}

    def get_connection_by(self, user_id):
        user_conn = self._connections.get(user_id)
        if not user_conn:
            user_conn = pexpect.spawnu('docker run -ti bot python3')
            user_conn.expect('>>> ')
            self._connections[user_id] = user_conn
        return user_conn

    def custom_commands(self, user_id, command):
        if command == 'exit()':
            conn = self.get_connection_by(user_id)
            conn.kill(0)
            del self._connections[user_id]
            user_id, command = None, None

        return user_id, command

    def execute_command(command):
        """
        Executes command for custom user
        If connections was closed  returns None,
        else returns command result
        """
        msg = cl.execute(command)
        print("returned by execute")
        pprint(msg)

        output = ''
        while True:
            msg = cl.get_iopub_msg()
            print("read from iopub")
            #print(msg)
            if msg['msg_type'] ==  'stream':
                output += msg['content']['text']
            elif msg.get('content', {}).get('execution_state') == 'idle':
                break
        return output


    if __name__ == '__main__':
        result = execute_command('a = 1')
        print(result)
        result = execute_command('b = 2\nprint(a)')
        print(result)
        result = execute_command('''for i in range(10): \n print(i)''')
        print(result)
        result = execute_command('import this')
        print(result)
        result = execute_command('import this')
        print(result)

        command = 'a=1\nprint(a)\nfrom time import sleep\nsleep(8)\nprint(100)'
        result = execute_command(command)
        print(result)

    if __name__ == '__main__':
        provider = PythonProvider()
        result = provider.execute_command(1, 'a = 3')
        print(result)
        result = provider.execute_command(1, '''for i in range(10): \n print(i)''')
        print(result)
        result = provider.execute_command(1, 'import this')
        print(result)
        result = provider.execute_command(1, 'import this')
        print(result)

