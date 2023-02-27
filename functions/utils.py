import pandas as pd
from datetime import datetime

def __getDfNameAccount():
    dfNameAccount = pd.read_excel("excel/listMatUsername.xlsx")
    return dfNameAccount

def __getDfSupAccount():
    dfSupAccount = pd.read_excel("excel/listaNameToAccount.xlsx")
    return dfSupAccount

def getSupAccount():
    return __getDfSupAccount()

def getKey(dictParameter, value):
    for key, values in dictParameter.items():
        if value in values:
            return key
    return False

def getNomeSup(name):
    dfSupAccount = __getDfSupAccount()
    listUser = dfSupAccount["CONTA"].tolist()
    listSup = dfSupAccount["NOME_EQUIPE"].tolist()

    for i in range(len(listUser)):
        if str(name).lower() in str(listUser[i]).lower():
            return str(listSup[i])
    return name


def getMatr(name):
    dfNameAccount = __getDfNameAccount()
    listUser = dfNameAccount["Username"].tolist()
    listMatr = dfNameAccount["Matricula"].tolist()

    for i in range(len(listUser)):
        if str(name).lower() == str(listUser[i]).lower():
            return "#" + str(listMatr[i])
    return False

def getLogin(mat):
    dfNameAccount = __getDfNameAccount()
    listUser = dfNameAccount["Username"].tolist()
    listMatr = dfNameAccount["Matricula"].tolist()
    for i in range(len(listMatr)):
        if mat == str(listMatr[i]):
            return str(listUser[i])
    return False

def correctIp(dictIP, ip, mat):
    for key, value in dictIP.items():
        if mat in value:
            if ip == value:
                return True
            else:
                return False

def getIp(dictIP, mat):
    for key, value in dictIP.items():
        if mat in value:
            return key
    return False


def writeLogs(msg):
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(r'logs/log.txt', 'a') as file:
        file.write(f"\n{now} - {msg}")

def writeIPErrado(ips):
    with open(r'logs/ipsComErro.txt', "w") as f:
        for ip in ips:
            f.write(f"{ip}\n")

def now():
    nowTime = datetime.now()
    nowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
    return nowTime

def appendDict(dictParameter, key, value):
    if key in dictParameter:
        dictParameter[key].append(value)
    else:
        dictParameter[key] = [value]