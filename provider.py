from jupyter_client.multikernelmanager import MultiKernelManager


class PythonProvider:
    def __init__(self):
        self.mk_manager = MultiKernelManager()

    def start(self, user_id):
        """
        Runs jupyter kernel in new container
        """
        self.mk_manager.start_kernel(kernel_id=user_id)

    def restart(self, user_id):
        """
        Restarts jupyter kernel
        """
        self.mk_manager.shutdown_kernel(user_id)
        self.start(user_id)

    def get_client_by(self, user_id):
        """
        Get client connected to kernel
        """
        try:
            kernel_manager = self.mk_manager.get_kernel(user_id)
        except KeyError:
            self.start(user_id)
            kernel_manager = self.mk_manager.get_kernel(user_id)
        return kernel_manager.client()

    def execute(self, user_id, command):
        """
        Executes command for custom user
        If connections was closed  returns None,
        else returns command result
        """
        if not all((user_id, command)):
            return None

        client = self.get_client_by(user_id)
        client.execute(command)

        output = ''
        while True:
            msg = client.get_iopub_msg()

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
    try:
        provider = PythonProvider()
        result = provider.execute_command(1, 'asdf')
        print(result)
        result = provider.execute_command(1, 'a = 1')
        print(result)
        result = provider.execute_command(1, 'a')
        print(result)
        result = provider.execute_command(1, 'b = 2\nprint(a)')
        print(result)
        result = provider.execute_command(1, 'for i in range(10): \n print(i)')
        print(result)
        result = provider.execute_command(1, 'import this')
        print(result)
        result = provider.execute_command(1, 'import this')
        print(result)

        command = 'a=1\nprint(a)\nfrom time import sleep\nsleep(3)\nprint(100)'
        result = provider.execute_command(1, command)
        print(result)
    finally:
        provider.mk_manager.shutdown_all()
