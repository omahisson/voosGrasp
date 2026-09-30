# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 05:58:53 2026

@author: dev
"""

# 100;FEN;PFG;06:40;08:47;7
# 101;AJU;PFG;06:45;08:00;13
# 102;POA;PFG;06:08;08:06;4

PFG = []

# exercicio 1
# leitura de arquivo
with open("voosNovo.txt", "r") as arquivo:
    for linha in arquivo:
        voo = linha.strip().split(";")

        idVoo = int(voo[0])
        intervalo = int(voo[5])

        # define o horario em que o voo usa PFG
        if voo[1] == "PFG":
            horarioPFG = voo[3]
        else:
            horarioPFG = voo[4]

        # monta a lista com os dados
        PFG.append([idVoo, horarioPFG, intervalo])

for voo in PFG:
    print(voo)
    
# exercicio 2
def horaParaMinutos(hora):
    partes = hora.split(":")
    horas = int(partes[0])
    minutos = int(partes[1])
    totalMinutos = horas * 60 + minutos
    return totalMinutos


def minutosParaHora(totalMinutos):
    horas = totalMinutos // 60
    minutos = totalMinutos % 60
    hora = f"{horas:02d}:{minutos:02d}"
    return hora


# atraso do voo
def calculaAtraso(horaPrevista, horaReal):
    prevista = horaParaMinutos(horaPrevista)
    real = horaParaMinutos(horaReal)
    atraso = real - prevista
    return atraso


# quando a pista vai ta liberada
def calculaLiberacao(horaReal, intervalo):
    minutos = horaParaMinutos(horaReal)
    minutos = minutos + intervalo
    return minutosParaHora(minutos)

def calculaAtrasoTotal(P1, P2):
    atrasoTotal = 0

    for voo in P1:
        atrasoTotal += voo[2]
    for voo in P2:
        atrasoTotal += voo[2]
    return atrasoTotal

# exercicio 3
import random

P1 = []
P2 = []

liberadoP1 = "06:00"
liberadoP2 = "06:00"

# uso da pista
PFG.sort(key=lambda x: x[1])

# escolhe pista
for voo in PFG:
    idVoo = voo[0]
    horario = voo[1]
    intervalo = voo[2]
    pista = random.randint(1, 2)

    if pista == 1:
        if horaParaMinutos(horario) > horaParaMinutos(liberadoP1):
            horaReal = horario
        else:
            horaReal = liberadoP1

        atraso = calculaAtraso(horario, horaReal)
        P1.append([idVoo, horaReal, atraso, intervalo])
        liberadoP1 = calculaLiberacao(horaReal, intervalo)

    # pista 2
    else:

        if horaParaMinutos(horario) > horaParaMinutos(liberadoP2):
            horaReal = horario
        else:
            horaReal = liberadoP2

        atraso = calculaAtraso(horario, horaReal)
        P2.append([idVoo, horaReal, atraso, intervalo])
        liberadoP2 = calculaLiberacao(horaReal, intervalo)

print("\nPista 1")
for voo in P1:
    print(voo)

print("\nPista 2")
for voo in P2:
    print(voo)

print("\nAtraso total:", calculaAtrasoTotal(P1, P2))

# exercicio 5
P1 = []
P2 = []

liberadoP1 = "06:00"
liberadoP2 = "06:00"

# voosParaEscolherPista
voosRestantes = PFG[:]
while len(voosRestantes) > 0:

    # exercicio 4
    listaCandidatos = []

    for voo in voosRestantes:
        idVoo = voo[0]
        horario = voo[1]
        intervalo = voo[2]

        if horaParaMinutos(horario) > horaParaMinutos(liberadoP1):
            horaRealP1 = horario
        else:
            horaRealP1 = liberadoP1
        atrasoP1 = calculaAtraso(horario, horaRealP1)
        listaCandidatos.append(
            [idVoo, 1, horaRealP1, atrasoP1, intervalo, horario]
        )

        if horaParaMinutos(horario) > horaParaMinutos(liberadoP2):
            horaRealP2 = horario
        else:
            horaRealP2 = liberadoP2
        atrasoP2 = calculaAtraso(horario, horaRealP2)
        listaCandidatos.append(
            [idVoo, 2, horaRealP2, atrasoP2, intervalo, horario]
        )

    # atraso
    listaCandidatos.sort(key=lambda x: x[3])


    # LRC2
    tamListaMelhores = 2
    listaMelhoresCandidatos = listaCandidatos[0:tamListaMelhores]
    posicao = random.randint(0, len(listaMelhoresCandidatos) - 1)
    candidatoEscolhido = listaMelhoresCandidatos[posicao]

    # dadosDele
    idEscolhido = candidatoEscolhido[0]
    pistaEscolhida = candidatoEscolhido[1]
    horaReal = candidatoEscolhido[2]
    atraso = candidatoEscolhido[3]
    intervalo = candidatoEscolhido[4]

    if pistaEscolhida == 1:
        P1.append([idEscolhido, horaReal, atraso, intervalo])
        liberadoP1 = calculaLiberacao(horaReal, intervalo)
    else:
        P2.append([idEscolhido, horaReal, atraso, intervalo])
        liberadoP2 = calculaLiberacao(horaReal, intervalo)


    # tiramos o voo escalonado
    for voo in voosRestantes:
        if voo[0] == idEscolhido:
            voosRestantes.remove(voo)
            break


print("\nPista 1")
for voo in P1:
    print(voo)

print("\nPista 2")
for voo in P2:
    print(voo)

print("\nAtraso total:", calculaAtrasoTotal(P1, P2))