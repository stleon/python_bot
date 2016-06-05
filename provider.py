from pprint import pprint

from jupyter_client.multikernelmanager import MultiKernelManager


class PythonProvider:
    def __init__(self):
        self.mk_manager = MultiKernelManager()

    def get_connection_by(self, user_id):
        try:
            kernel_manager = self.mk_manager.get_kernel(user_id)
        except KeyError:
            self.mk_manager.start_kernel(kernel_id=user_id)
            kernel_manager = self.mk_manager.get_kernel(user_id)
        user_client = kernel_manager.client()
        return user_client

    def custom_commands(self, user_id, command):
        if command == 'exit()':
            self.mk_manager.shutdown_kernel(user_id)
            user_id, command = None, None
        return user_id, command

    def execute_command(self, user_id, command):
        """
        Executes command for custom user
        If connections was closed  returns None,
        else returns command result
        """
        user_id, command = self.custom_commands(user_id, command)

        if not all((user_id, command)):
            return None

        cl = self.get_connection_by(user_id)
        cl.execute(command)

        print('\n{}\n'.format('-'*85))
        print(command)

        output = ''
        while True:
            msg = cl.get_iopub_msg()
            pprint(msg)
            if msg['msg_type'] == 'execute_result':
                output += msg['content']['data']['text/plain']
            elif msg['msg_type'] == 'stream':
                output += msg['content']['text']
            elif msg['msg_type'] == 'error':
                output += '\n'.join(msg['content']['traceback'])
            elif msg.get('content', {}).get('execution_state') == 'idle':
                break
        return output


if __name__ == '__main__':
    provider = PythonProvider()
    result = provider.execute_command(1, 'asdf')
    print(result)
    result = provider.execute_command(1, 'a = 1')
    print(result)
    result = provider.execute_command(1, 'a')
    print(result)

'''
    result = provider.execute_command(1, 'b = 2\nprint(a)')
    print(result)
    result = provider.execute_command(1, 'for i in range(10): \n print(i)')
    print(result)
    result = provider.execute_command(1, 'import this')
    print(result)
    result = provider.execute_command(1, 'import this')
    print(result)

    command = 'a=1\nprint(a)\nfrom time import sleep\nsleep(8)\nprint(100)'
    result = provider.execute_command(1, command)
    print(result)
'''
