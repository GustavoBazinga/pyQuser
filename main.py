import sys
import os
from functions.core import verifyIPStart
from functions.utils import *
from functions.saveData import saveExcel, saveDB
from functions.supervisorMessage import superMessage
from functions.prints import *
import time

def main():
    try:
        start = time.time()
        printRunning()
        IPComErro, crErrados, dictAppend, insertData, dictSup = verifyIPStart()

        writeIPErrado(IPComErro)
        if len(dictAppend['Horario']) >= 2:
            saveExcel(dictAppend)

            superMessage(crErrados, dictSup)

            saveDB(insertData)

        end = time.time()
        diff = end - start
        writeLogs(msg=f"Tempo de execucao: {diff} segundos")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        writeLogs("===============================")
        writeLogs("FALHA NAO TRATADA")
        writeLogs(f"Tipo de falha: {type(exc_type)}")
        writeLogs(f"Falha: {e} ")
        writeLogs(f"Arquivo: {fname}")
        writeLogs(f"Linha: {exc_tb.tb_lineno}")
        writeLogs("===============================")

if __name__ == "__main__":
    while True:
        main()
