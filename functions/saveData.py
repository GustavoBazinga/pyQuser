import pandas as pd
import shutil
from functions.auxfiles import getRelatorio, getRelatorioSup
from functions.utils import now, writeLogs
from functions.database.querys import insertIntoDB
import os
import datetime

def saveExcel(dictAppend):
    __checkTemp()
    
    nowTime = now
    df = getRelatorio()
    dfAppend = pd.DataFrame.from_dict(dictAppend)
    df = pd.concat([df, dfAppend], ignore_index=True)
    try:
        df.to_excel(r"relatorio/Relatorio_NAO_ABRIR.xlsx", index=False)
    except PermissionError:
        writeLogs("Erro ao salvar o arquivo de relatório... salvando relatorio em uma pasta temporária")
        df.to_excel(f"relatorio/temp/Relatorio_NAO_ABRIR_{str(nowTime)}.xlsx", index=False)
    else:
        try:
            shutil.copy(r"relatorio/Relatorio_NAO_ABRIR.xlsx", r"\\10.0.150.109\ti\Home "
                                                        r"Office\scriptQuser\Relatorio.xlsx")
        except Exception as e:
            writeLogs(f"Erro ao copiar o relatório para a pasta do nas... {e}")
        finally:
            try:
                shutil.copy(r"relatorio/Relatorio_NAO_ABRIR.xlsx", r"\\10.0.150.241\c$\Users\user\Documents\scripts\logs\pyMail\Relatorio.xlsx")
            except:
                writeLogs("Erro ao copiar o relatório para a pasta do .241...")
        writeLogs("Relatório salvo com sucesso!")
        
def saveExcelSup(sup, ip, quant):
    nowTime = now()
    dateList = nowTime.split(" ")
    df = getRelatorioSup()
    dfAppend = {"Supervisor": [sup], "IP": [ip], "Quantidade": [quant], "Data": [dateList[0]], "Hora": [dateList[1]]}
    pdAppend = pd.DataFrame.from_dict(dfAppend)
    df = pd.concat([df, pdAppend], ignore_index=True)
    print(df)
    try:
        df.to_excel(r"relatorio\Relatorio_Supervisor_NAO_ABRIR.xlsx", index=False)
    except:
        writeLogs(msg="Erro ao salvar o relatório do supervisor...")
    else:
        try:
            shutil.copy(r"relatorio\Relatorio_Supervisor_NAO_ABRIR.xlsx", r"\\10.0.150.109\ti\Home Office\scriptQuser\Relatorio_Supervisor.xlsx")
        except:
            writeLogs(msg="Erro ao copiar o relatório do supervisor para a pasta do nas...")
        try:
            shutil.copy(r"relatorio\Relatorio_Supervisor_NAO_ABRIR.xlsx", r"\\10.0.150.241\c$\Users\user\Documents\scripts\logs\pyMail\Relatorio_Supervisor.xlsx")
        except:
            writeLogs(msg="Erro ao copiar o relatório do supervisor para a pasta do .241...")
        writeLogs(msg="Relatório do supervisor salvo com sucesso!")

def saveDB(insertData):
    nowTime = datetime.datetime.now()
    next7 = nowTime + datetime.timedelta(minutes=7)
    insertData += "(1, '0', '0', '" + str(next7) + "')"
    try:
        insertIntoDB(insertData)
    except Exception as e:
        writeLogs(f"Erro ao salvar no banco de dados... {e}")

def __checkTemp():
    writeLogs("Verificando se existe arquivos temporários...")
    listFiles = os.listdir("relatorio/temp")
    writeLogs(f"Arquivos temporários encontrados: {listFiles}")
    for file in listFiles:
        dfTemp = pd.read_excel(f"relatorio/temp/{file}")
        df = getRelatorio()
        df = pd.concat([df, dfTemp], ignore_index=True)
        try:
            df.to_excel(r"relatorio/Relatorio_NAO_ABRIR.xlsx", index=False)
        except Exception as e:
            writeLogs(f"Erro ao unir o arquivo temporário {file}... {e}")
        else:
            os.remove(f"relatorio/temp/{file}")
