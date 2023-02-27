from functions.auxfiles import isNotExpect, findInBackup
from functions.utils import writeLogs, now, getLogin, getMatr, getIp
from functions.quserFunctions import quserListBasic, quserListByUserRDP
from functions.message import *
from functions.database.querys import getBaseIP
import datetime

def verifyIPStart():
    df, dictIP, dictSup, allCR, quant = getBaseIP()
    dictAppend = {"Matricula": ["========"], "IPDimensionado": ["========"], "IPErrado": ["========"],
                  "Horario": ["Novo Loop"], "Data": ["========"]}
    IPComErro = []
    crErrados = []
    insertData = ""
    for key, value in dictIP.items():
        if quant % 10 == 0:
            writeLogs(f"Restam {quant} IPs para verificar")
        quant -= 1
        writeLogs(f"Verificando IP {key}")
        errados = []
        if isNotExpect(key):
            listCR, allCR = quserListBasic(key, allCR)
            nowTime = now()
            if not "Timeout" in listCR and not "RPC Error" in listCR and not "Vazio" in listCR:
                errados = [x for x in listCR if x.replace("#", "") not in value]
                for i in range(len(errados)):
                    if isNotExpect(errados[i]):
                        if "#" in errados[i]:
                            loginMsg = getLogin(errados[i].replace("#", ""))
                        else:
                            loginMsg = errados[i].replace("#", "")
                        errados[i] = errados[i].replace("#", "")
                        ipBruto = df.loc[df[0] == int(errados[i].replace("#", ""))][10].values
                        if len(ipBruto) == 0:
                            ip = __semIp(loginMsg, key)
                        else:
                            ip = __ipErrado(loginMsg, key, ipBruto[0])
                        writeLogs("CR errado: " + errados[i])
                        crErrados.append(errados[i])
                        dateList = nowTime.split(" ")
                        dictAppend["Matricula"].append(errados[i])
                        dictAppend["IPDimensionado"].append(ip)
                        dictAppend["IPErrado"].append(key)
                        dictAppend["Horario"].append(dateList[1])
                        dictAppend["Data"].append(dateList[0])
                        insertData += "(" + str(errados[i]) + ", '" + ip + "', '" + key + "', '" + nowTime + "'),"
                    else:
                        writeLogs(f"CR {errados[i]} esta na lista de excecoes")
                else:
                    if "Timeout" in listCR:
                        writeLogs(f"Timeout - {key}")
                        IPComErro.append(key + " - Timeout")
                    elif "RPC Error" in listCR:
                        IPComErro.append(key + " - RPC Error")
                        writeLogs(f"RPC Error - {key}")
        else:
            writeLogs(f"IP {key} esta na lista de excecoes")

    plusData, crErrados, dictAppend = __verifyRestantes(dictIP, allCR, crErrados, dictAppend)
    insertData += plusData
    return IPComErro, crErrados, dictAppend, insertData, dictSup

def __verifyRestantes(dictIP, allCR, crErrados, dictAppend):
    findInBackup("teste", 1, True)
    insertData = ""
    crNaoEncontrado = []
    nowTime = datetime.datetime.now().strftime("%H:%M:%S")
    nowTime = datetime.datetime.strptime(nowTime, "%H:%M:%S")
    nowTime = (nowTime - datetime.datetime(1900, 1, 1)).total_seconds()
    for key, value in allCR.items():
        # Verify if now is between the time of the dictionary
        startTime = value[0].total_seconds()
        endTime = value[1].total_seconds()
        if startTime <= nowTime <= endTime:
            crNaoEncontrado.append(key)

    for cr in range(len(crNaoEncontrado)):
        isFound = getLogin(crNaoEncontrado[cr])
        if isFound:
            crNaoEncontrado[cr] = isFound

    writeLogs(msg="Verificando CRs nao encontrados")
    writeLogs(msg="CRs nao encontrados: " + str(crNaoEncontrado))

    for i in range(len(crNaoEncontrado)):
        consultorMat = __findMat(crNaoEncontrado[i])
        login = crNaoEncontrado[i]
        writeLogs(f"Verificando CR {consultorMat}/{login}")
        if isNotExpect(consultorMat):
            lastIP = findInBackup(login, 3, False)
            writeLogs(f"Verificando IPs: {lastIP}")
            for ip in lastIP:
                if isNotExpect(ip):
                    online = quserListByUserRDP(ip, login)
                    correct = getIp(dictIP, consultorMat)
                    nowTime = now()
                    dateList = nowTime.split(" ")
                    if online:
                        if correct:
                            if not ip in correct:
                                crErrados.append(consultorMat)
                                writeLogs(f"CR {consultorMat} encontrado no IP e esta errado")
                                ipLogado = __ipErrado(login, ip, correct)
                                dictAppend["Matricula"].append(consultorMat)
                                dictAppend["IPDimensionado"].append(correct)
                                dictAppend["IPErrado"].append(ip)
                                dictAppend["Horario"].append(dateList[1])
                                dictAppend["Data"].append(dateList[0])
                                insertData += "(" + str(consultorMat) + ", '" + correct + "', '" + ip + "', '" + nowTime + "'),"
                                break
                            else:
                                break
                        else:
                            crErrados.append(consultorMat)
                            writeLogs(f"CR {consultorMat} encontrado no IP e nao possui IP dimensionado")
                            ipLogado = __semIp(login, ip)
                            dictAppend["Matricula"].append(consultorMat)
                            dictAppend["IPDimensionado"].append(ipLogado)
                            dictAppend["IPErrado"].append(ip)
                            dictAppend["Horario"].append(dateList[1])
                            dictAppend["Data"].append(dateList[0])
                            insertData += "(" + str(consultorMat) + ", '" + "Nao encontrado" + "', '" + ip + "', '" + nowTime + "'),"
                            break
                else:
                    writeLogs(f"IP {ip} esta na lista de excecoes")
        else:
            writeLogs(f"CR {consultorMat} esta na lista de excecoes")
    return insertData, crErrados, dictAppend

def __semIp(loginMsg, key):
    writeLogs(f"O CR {loginMsg} nao esta cadastrado na base de homeoffice")
    ip = "Nao encontrado"
    messageSemIp(loginMsg, key)
    return ip

def __ipErrado(loginMsg, key, ip):
    messageIpErrado(loginMsg, key, ip)
    return ip

def __findMat(login):
    if login.isnumeric():
        return login
    else:
        return getMatr(login).replace("#", "")