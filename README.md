# MSSQL Bruteforce and information modules

This project is divided to two modules:
* bruteforce - Takes a list of users and passwords, a payload path and host ip, and tries to bruteforce connect an MSSQL server and execute the payload.

* fingerprint - Used for fingerprinting the MSSQL host which uses the SQL Browser service (works only if enabled).

# Usage:

* bruteforce module:

  mssql_bruteforce.py [-h] [-H HOST] [-p PORT] -v VERSION -u USERS
                             [USERS ...] -pass PASSWORDS [PASSWORDS ...] -f
                             PAYLOAD
   
Example: 
python mssql_bruteforce.py -H  192.168.1.3 -v 1 -u sa admin username user name -pass 123 1234 12345 123456 pass password    -f ./payload.bat


* fingerprint module:
	info.py [-h] [-H HOST] Optional: [-p PORT] [-t TIMEOUT] [-i INSTANCE]

Example:
	python info.py -H 192.168.1.3 


# Dependencies and Resources


Python libs that were used in the project are (sub-libs and dependencies not mentioned, for full list see requirements.txt):
* pymssql - This lib was used for MSSQL communicating and query executions.
* pyftpdlib - This lib was used for the FTP server used in one of the attacks.

Resources I've used:


* https://www.bobpusateri.com/archive/2010/09/a-look-at-the-sql-server-browser-service/

* https://s3.amazonaws.com/img.bobpusateri.com/bc/2010/09/CoonleyShark.png

* https://s3.amazonaws.com/img.bobpusateri.com/bc/2010/09/PortQry.jpg

* http://www.internationaldatascience.com/wp-content/uploads/2013/09/WiresharkUDP1434Response.png

* http://infocenter.sybase.com/help/index.jsp?topic=/com.sybase.infocenter.dc36273.1550/html/sprocs/X20958.htm

* https://www.techinfected.net/2017/07/create-simple-ftp-server-client-in-python.html

* https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql?view=sql-server-2017

* http://pentestmonkey.net/cheat-sheet/sql-injection/mssql-sql-injection-cheat-sheet
