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

    def execute_command(self, user_id, command):
        """
        Executes command for custom user
        If connections was closed  returns None, 
        else returns command result
        """
        user_id, command = self.custom_commands(user_id, command)

        if not all([user_id, command]):
            return None

        conn = self.get_connection_by(user_id)
        # for multilines commands to work correct
        command = command + conn.linesep
        lines_count = command.count(conn.linesep)

        conn.sendline(command)
        conn.expect('>>> ')
        result = conn.before
        result = conn.linesep.join(result.split(conn.linesep)[lines_count:])

        # going to the end of flow to avoid redundant new lines at the end of command
        # example: a=3\n\n\n
        while True:
            try:
                conn.expect('>>> ', timeout=0.001)
            except TIMEOUT:
                break

        return result


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

