import subprocess
from functions.utils import getMatr
import sys
from functions.prints import printStop

def quserListBasic(ip, allCR):
    # Create a list with the matr you collumns of the ip address

    listResult = []
    # Create a list with the matr you collumns of the ip address
    try:
        completed = subprocess.run(["quser", f"/server:{ip}"], capture_output=True, timeout=30, shell=True)
    except subprocess.TimeoutExpired:
        listResult.append("Timeout")
    except KeyboardInterrupt:
        printStop()
        sys.exit()

    else:
        if completed.returncode == 0:
            output = completed.stdout.decode('unicode_escape')
            output = output.splitlines()
            output = output[1:]
            for line in output:
                line = line.split(" ")
                line = [line for line in line if line.strip() != ""]
                if not "console" in str(line[1]).lower() and "tivo" in str(line[3]).lower():
                    if line[0].isnumeric():
                        listResult.append(line[0])
                    else:
                        mat = getMatr(line[0])
                        if mat:
                            listResult.append(mat)
            for cr in listResult:
                try:
                    del allCR[str(cr).replace("#", "")]
                except:
                    pass
        else:
            if "RPC" in completed.stderr.decode('unicode_escape'):
                listResult.append("RPC Error")
            else:
                listResult.append("Vazio")

    return listResult, allCR

def quserListByUserAll(ip, user):
    # Create a list with the matr you collumns of the ip address
    listResult = []
    # Create a list with the matr you collumns of the ip address
    try:
        completed = subprocess.run(["quser", f"/server:{ip}"], capture_output=True, timeout=30, shell=True)
    except subprocess.TimeoutExpired:
        listResult.append("Timeout")
    except KeyboardInterrupt:
        printStop()
        sys.exit()
    else:
        if completed.returncode == 0:
            output = completed.stdout.decode('unicode_escape')
            output = output.splitlines()
            output = output[1:]
            for line in output:
                if "tivo" in line and str(user).lower() in str(line).lower():
                    return True
        else:
            return False

def quserListByUserRDP(ip, user):
    # Create a list with the matr you collumns of the ip address
    listResult = []
    # Create a list with the matr you collumns of the ip address
    try:
        completed = subprocess.run(["quser", f"/server:{ip}"], capture_output=True, timeout=30,
                                   shell=True)
    except subprocess.TimeoutExpired:
        listResult.append("Timeout")
    except KeyboardInterrupt:
        print("   _____ _                             _ ")
        print("  / ____| |                           | |")
        print(" | (___ | |_ ___  _ __  _ __   ___  __| |")
        print("  \___ \| __/ _ \| '_ \| '_ \ / _ \/ _` |")
        print("  ____) | || (_) | |_) | |_) |  __/ (_| |")
        print(" |_____/ \__\___/| .__/| .__/ \___|\__,_|")
        print("                 | |   | |               ")
        print("                 |_|   |_|               ")
        sys.exit()
    else:
        if completed.returncode == 0:
            output = completed.stdout.decode('unicode_escape')
            output = output.splitlines()
            output = output[1:]
            for line in output:
                if not "onsole" in line and "tivo" in line and str(user).lower() in str(line).lower():
                    return True
        else:
            return False