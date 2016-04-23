#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import pexpect

# Don't do this unless you like being John Malkovich
# c = pexpect.spawnu('/usr/bin/env python ./python.py')

# Note that, for Python 3 compatibility reasons, we are using spawnu and
# importing unicode_literals (above). spawnu accepts Unicode input and
# unicode_literals makes all string literals in this script Unicode by default.

class PythonProvider:
    def __init__(self):
        _connections = {}

    def get_connection_by(self, user_id):
        user_conn = self._connections.get(user_id)
        if not user_conn:
            user_conn = pexpect.spawnu('/usr/bin/env python')
            self._connections[user_id] = new_user_connection
        return user_conn

    def custom_commands(self, user_id, command):
        if command == 'exit()':
            conn = self.get_user_connection_by(user_id)
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

        conn.sendline(command)

        result = ''.join(conn.readline())
        return result


if __name__ == '__main__':
    provider = PythonProvider()

