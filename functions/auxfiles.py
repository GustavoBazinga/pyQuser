import pandas as pd
import shutil

def isNotExpect(target):
    with open(r"\\10.0.150.109\ti\Home Office\scriptQuser\ListaDeExcecoes\except.txt", "r") as f:
        exceptList = f.read().splitlines()
    if target in exceptList:
        return False
    else:
        return True

def getRelatorio():
    df = pd.read_excel(r"relatorio/Relatorio_NAO_ABRIR.xlsx")
    return df

def getRelatorioSup():
    df = pd.read_excel(r"relatorio\Relatorio_Supervisor_NAO_ABRIR.xlsx")
    return df

def findInBackup(login, quant, copyFile):
    df = __getDfBackup(copyFile)
    if copyFile:
        return False
    response = []
    listUser = df[0].tolist()
    listIP = df[1].tolist()
    listStatus = df[7].tolist()
    for linha in range(len(listUser)-1, int(len(listUser)*0.8),-1):
        if str(login).lower() == str(listUser[linha]).lower() and "logon" in str(listStatus[linha]).lower() and not str(listIP[linha]).lower() in response:
            response.append(str(listIP[linha]).lower())
        if len(response) == quant or linha == int(len(listUser)*0.8) + 1:
            return response



def __getDfBackup(copy):
    if copy:
        __copyBackup()
    df = pd.read_csv("excel/Backup.csv", sep=";", encoding="latin-1", header=None)
    return df

def __copyBackup():
    shutil.copy(r"\\10.0.150.43\acessos\Backup.csv", r"excel/Backup.csv")

