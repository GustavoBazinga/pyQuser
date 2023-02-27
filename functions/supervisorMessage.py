from functions.utils import writeLogs, now, getNomeSup
from functions.auxfiles import findInBackup
from functions.quserFunctions import quserListByUserAll
from functions.message import messageSupervisor
from functions.saveData import saveExcelSup

def superMessage(CRErrados, dictSup):
    superlist = __mountDictSupCR(CRErrados, dictSup)

    for key, value in superlist.items():
        writeLogs(f"Supervisor: {key} - CRs: {value}")
        lastIP = findInBackup(key, 3, False)
        writeLogs(f"Supervisor: {key} - Ultimos IPs: {lastIP}")
        for ip in lastIP:
            check = quserListByUserAll(ip, key.lower())
            if check:
                writeLogs(f"Supervisor {key} esta logado no IP {ip}. Enviando mensagem...")
                messageSupervisor(key, ip, value)
                saveExcelSup(getNomeSup(key), ip, len(value))
                break
            if lastIP.index(ip) == len(lastIP) - 1:
                writeLogs(f"Supervisor {key} nao esta logado em nenhum dos ultimos IPs. Mensagem nao enviada")
                break



def __mountDictSupCR(CRErrados, dictSup):
    superList = {}
    for value in CRErrados:
        for keySup, valueSup in dictSup.items():
            if value in valueSup:
                if keySup in superList:
                    superList[keySup].append(value)
                else:
                    superList[keySup] = [value]
    return superList