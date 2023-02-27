import os
from functions.utils import now

def messageSemIp(login, ip):
    os.system(f"msg {login} /server:{ip} Atenção! Você não possui um IP dimensionado para você. Por favor, desconecte da máquina e entre em contato com a supervisão.")

def messageIpErrado(login, target, correct):
    os.system(f"msg {login} /server:{target} Você está conectado no IP errado! Se conecte no IP correto: {correct} ou entre em contato com a supervisão para verificar.")

def messageSupervisor(login, ip, cr):
    msgTime = now()
    os.system(
        f"msg {login} /server:{ip} Atenção! Há CRs em Home Office da sua supervisão que estão conectados no IP errado e/ou sem IP: {cr} Por favor entre em contato e solicite correção. Enviados às {msgTime}")