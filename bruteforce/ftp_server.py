""" Opens a simple FTP server using pyftpdlib with default connection details in a different process. """

import logging
import multiprocessing
import consts

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


class FTP:

    """Configures and establish an FTP server with default details.

        Args:
            user (str): User for FTP server auth
            password (str): Password for FTP server auth
            working_dir (str): The local working dir to init the ftp server on.

    """

    def __init__(self, user=consts.FTP_SERVER_USER, password=consts.FTP_SERVER_PASSWORD,
                 working_dir=consts.FTP_WORKING_DIR):
        """Look at class level docstring."""

        self.user = user
        self.password = password
        self.working_dir = working_dir

    def run_server(self, user=consts.FTP_SERVER_USER, password=consts.FTP_SERVER_PASSWORD,
                   working_dir=consts.FTP_WORKING_DIR):

        """ Configures and runs the ftp server to listen forever until stopped.

            Args:
                user (str): User for FTP server auth
                password (str): Password for FTP server auth
                working_dir (str): The local working dir to init the ftp server on.
        """

        # Defining an authorizer and configuring the ftp user
        authorizer = DummyAuthorizer()
        authorizer.add_user(user, password, working_dir, perm='elradfmw')

        # Normal ftp handler
        handler = FTPHandler
        handler.authorizer = authorizer

        address = (consts.FTP_SERVER_ADDRESS, consts.FTP_SERVER_PORT)

        # Configuring the server using the address and handler. Global usage in stop_server thats why using self keyword
        self.server = FTPServer(address, handler)

        # Starting ftp server, this server has no auto stop or stop clause, and also, its blocking on use, thats why I
        # multiproccess is being used here.
        self.server.serve_forever()

    def stop_server(self):
        # Stops the FTP server and closing all connections.
        self.server.close_all()

if __name__ =='__main__':
    ftp = FTP()
    multiprocessing.log_to_stderr(logging.DEBUG)
    p = multiprocessing.Process(target=ftp.run_server)
    p.start()
    import time
    time.sleep(1)
    print 'shutting down'
    p.terminate()