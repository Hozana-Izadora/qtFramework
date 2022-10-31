from itertools import count
from unittest import result
import requests
import psycopg2
import paramiko
from sshtunnel import SSHTunnelForwarder,create_logger

HOST = '172.30.99.50'
HOST2 = '127.0.0.1'
DB = 'cabemce-associados-cake4-v01-homol2'
DB2 = 'carteirinhas'
USER = 'associado_user'
USER2 = 'chatbot'
PASSWORD = 'ASSO123ciado'
PASSWORD2 = 'fb86f4fc8'

conn = psycopg2.connect(host=HOST, database=DB, user=USER, password=PASSWORD)
print("Connection established")
cursor = conn.cursor()

cursor.execute(
    """select * from carteirinhas join associados on id_associado = associado_id order by nome_associado """)

filename = '/home/izadora/.ssh/id_rsa'
password = 'izah.051295'
mypkey = paramiko.RSAKey.from_private_key_file('/home/izadora/.ssh/id_rsa')
# print(mypkey)
# exit()

tunnel =  SSHTunnelForwarder(
        ('boleto.cabemce.com.br', 22),
        ssh_username='root',
        ssh_pkey=mypkey,
        remote_bind_address=('localhost', 5432),
        local_bind_address=('127.0.0.1', 6666))

tunnel.skip_tunnel_checkup = False

try:
        tunnel.start()
except:
        try:
            tunnel.stop()
            tunnel.start()
        except:
            try:
                tunnel.stop()
                tunnel.start()
            except:
                tunnel.stop()
                tunnel.start()

conn2 = psycopg2.connect(host=HOST2, database=DB2, user=USER2, password=PASSWORD2)
cur_remoto = conn2.cursor()


def verificaExistencia(hash):
    sql = "SELECT * FROM validacao WHERE hash = '{}'".format(hash)
    cur_remoto.execute(sql)
    result = cur_remoto.fetchall()
    if (result[0] == []):
        return False
    return True

def insertData(row, ativo):
    sql = "INSERT INTO validacao(nome,matricula,ativo,validade,created,modified, hash) VALUES('{}','{}','{}','{}', NOW(),NOW(),'{}')".format(row['nome'],row['matricula'],ativo,row['validade'],row['hash'])
    cur_remoto.execute(sql)
    print('oi')

def updateData(row, ativo):
    sql = "UPDATE validacao SET (nome,matricula,ativo,validade,modified,hash) VALUES('{}','{}','{}','{}', NOW(),'{}')".format(row['nome'],row['matricula'],ativo,row['validade'],row['hash'])
    cur_remoto.execute(sql)
    print('tchau')


rows = cursor.fetchall()
countAssoc = 0
for row in rows:
    possuiCadastro = verificaExistencia(row['hash'])
    ativo = 'f'
    if(row['bloqueio_id'] == 1):
        ativo = 't'
    if(possuiCadastro==False):
        insertData(row,ativo)
    else:
        updateData(row,ativo)

conn2.commit()
conn.close()
cursor.close()
conn2.close()
cur_remoto.close()

