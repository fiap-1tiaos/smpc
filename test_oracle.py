import os

instant_client_path = r"C:\Users\defaultuser0\Downloads\sqldeveloper\oracledb_client\instantclient_23_9"
os.environ["PATH"] = instant_client_path + ";" + os.environ["PATH"]

os.add_dll_directory(instant_client_path)

import cx_Oracle
print("Versão do Oracle Client:", cx_Oracle.clientversion())
