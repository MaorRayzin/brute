# MSSQL Bruteforce and information modules

This project is divided to two modules:
* bruteforce - Takes a list of users and passwords, a payload path and host ip, and tries to bruteforce connect an MSSQL server and execute the payload.

*fingerprint - Used for fingerprinting the MSSQL host which uses the SQL Browser service (works only if enabled).

Usage is documented in every function of the modules.


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
