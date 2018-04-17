"""Retrieves Microsoft SQL Server instance information by querying the SQL Browser
service.
"""

import socket
import consts
import logging
import argparse
from collections import OrderedDict

logging.basicConfig(format='%(asctime)s %(message)s')

def retrieve_instance_info(host, instance_name=None, buffer_size=consts.BUFFER_SIZE, timeout=consts.TIMEOUT,
                           browser_port=consts.SQL_BROWSER_DEFAULT_PORT):
    """Gets Microsoft SQL Server instance information by querying the SQL Browser service.

        Args:
            host (str): Hostname or IP address of the SQL Server to query for information.
            instance_name (str): The name of the instance to query for information.
                            All instances are included if none.
            browser_port (int): SQL Browser port number to query.
            buffer_size (int): Buffer size for the UDP request.
            timeout (int): timeout for the query.

        Returns:
            dict: A dictionary with the server name as the key and a dictionary of the
                server information as the value.

    """
    # Create a UDP socket and sets a timeout
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    server_address = (host, browser_port)

    if instance_name:
        # The message is a CLNT_UCAST_INST packet to get a single instance
        # https://msdn.microsoft.com/en-us/library/cc219746.aspx
        message = '\x04{0}\x00'.format(instance_name)
    else:
        # The message is a CLNT_UCAST_EX packet to get all instances
        # https://msdn.microsoft.com/en-us/library/cc219745.aspx
        message = '\x03'

    # Encode the message as a bytesarray
    message = message.encode()

    # send data and receive response
    results = []
    try:
        logging.info('Sending message to requested host: {0}, {1}'.format(host, message))
        sock.sendto(message, server_address)
        data, server = sock.recvfrom(buffer_size)
    except socket.timeout:
        logging.error('Socket timeout reached, maybe browser service on host: {0} doesnt exist'.format(host))
        return results

    # Loop through the server data
    for server in data[3:].decode().split(';;'):
        server_info = OrderedDict()
        instance_info = server.split(';')

        if len(instance_info) > 1:
            for i in range(1, len(instance_info), 2):
                server_info[instance_info[i-1]] = instance_info[i]

            results.append(server_info)

    # Close the socket
    sock.close()

    return results


def main():
    """
           If the script is being used as a standalone this will handle it using arguments.

           Args:
               -h (str): Host IP address
               -p (str): SQL Browser protocol port
               -t (str): Timeout for the request
               -i (str): SQL Instance name if there is one.
       """

    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-h', '--host',
                        help='hostname or IP address of the SQL Server to query for information')
    parser.add_argument('-p', '--port', default=consts.SQL_BROWSER_DEFAULT_PORT, required=False,
                        help='SQL Browser Protocol udp port')
    parser.add_argument('-t', '--timeout', default=consts.TIMEOUT, required=False,
                        help='Socket timeout')
    parser.add_argument('-i', '--instance', required=False,
                        help='Socket timeout')

    arguments = parser.parse_args()

    try:
        info = retrieve_instance_info(arguments.host, arguments.instance,
                                      timeout=arguments.timeout, browser_port=arguments.port)
        for instance_info in info:
            print ('')

            for key, value in instance_info.items():
                print('{0}: {1}'.format(key, value))
    except socket.error as error:
        print 'Connection to {0} failed: {1}'.format(arguments.host, error)

if __name__ == '__main__':
   main()
