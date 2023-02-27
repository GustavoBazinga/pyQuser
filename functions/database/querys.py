import MySQLdb
from functions.utils import writeLogs, getSupAccount, now
import pandas as pd

__HOST = "10.0.150.59"
__USER = "ti"
__PASS = "Y22@astT*"

def insertIntoDB(insertData):
    db = MySQLdb.connect(host=__HOST, user=__USER, passwd=__PASS, db="db_ti")
    cursor = db.cursor()
    if db.open:
        writeLogs("Conexão com o banco de dados realizada com sucesso")
        writeLogs("Deletando dados antigos do banco de dados")
        cursor.execute("DELETE FROM tb_ipserrados")
        db.commit()
        writeLogs("Dados antigos deletados com sucesso")
        writeLogs("Inserindo novos dados no banco de dados")
        cursor.execute(f"INSERT INTO tb_ipserrados (matricula, ipcorreto, iperrado, horario) VALUES {insertData}")
        db.commit()
        writeLogs("Dados inseridos com sucesso")
        db.close()
        writeLogs("Conexao com o banco de dados fechada")
    else:
        writeLogs("Erro ao conectar com o banco de dados")
        raise Exception("Erro ao conectar com o banco de dados")

def getBaseIP():
    writeLogs("Iniciando conexão com o banco de dados")
    db = MySQLdb.connect(__HOST, __USER, __PASS, "db_general_data")
    cursor = db.cursor()
    if db.open:
        writeLogs("Conexão com o banco de dados realizada com sucesso")
        cursor.execute("SELECT * FROM tb_home_office_chat where ipaddress <> ''")
        result = cursor.fetchall()
        db.close()
        writeLogs("Conexão com o banco de dados finalizada")

        df = pd.DataFrame(list(result))

        dictIP, dictSup, allCR = __mountDicts(df)

        return df, dictIP, dictSup, allCR, len(dictIP)
    else:
        writeLogs("Erro ao conectar com o banco de dados")
        return False

def __mountDicts(df):
    dictIP = {}
    dictSup = {}
    allCR = {}
    dfSup = getSupAccount()
    listName = dfSup["NOME_EQUIPE"].tolist()
    listAccount = dfSup["CONTA"].tolist()

    for sup in range(len(listAccount)):
        try:
            listAccount[sup] = str(listAccount[sup].replace(" ", ""))
        except:
            listAccount[sup] = str(listAccount[sup])

    for index, row in df.iterrows():
        try:
            if row[10] != "" or row[10] is not None:
                allCR[str(row[0])] = [row[8], row[9]]
                if row[10] not in dictIP:
                    dictIP[row[10]] = [str(row[0])]
                else:
                    dictIP[row[10]].append(str(row[0]))
                index = listName.index(row[6])
                key = str(listAccount[index])
                if key not in dictSup:
                    dictSup[key] = [str(row[0])]
                else:
                    dictSup[key].append(str(row[0]))
        except:
            pass

    return dictIP, dictSup, allCR