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

# uso da pista
PFG.sort(key=lambda x: x[1])

# exercicio 7

# exercicio 5
def constroiSolucao():
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
            listaCandidatos.append([idVoo, 1, horaRealP1, atrasoP1, intervalo, horario])

            if horaParaMinutos(horario) > horaParaMinutos(liberadoP2):
                horaRealP2 = horario
            else:
                horaRealP2 = liberadoP2

            atrasoP2 = calculaAtraso(horario, horaRealP2)
            listaCandidatos.append([idVoo, 2, horaRealP2, atrasoP2, intervalo, horario])

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
            liberadoP2 = calculaLiberacao(horaReal,intervalo)

        # tiramos o voo escalonado
        for voo in voosRestantes:
            if voo[0] == idEscolhido:
                voosRestantes.remove(voo)
                break

    return P1, P2

# exercicio 6
def buscaVoo(idVoo):
    for voo in PFG:
        if voo[0] == idVoo:
            return voo

# recalcula os horarios e atrasos de uma pista
def recalculaCronogramaPista(pista):
    novaPista = []
    horarioLiberado = "06:00"

    for voo in pista:
        idVoo = voo[0]
        dadosVoo = buscaVoo(idVoo)
        horario = dadosVoo[1]
        intervalo = dadosVoo[2]

        if horaParaMinutos(horario) > horaParaMinutos(horarioLiberado):
            horaReal = horario
        else:
            horaReal = horarioLiberado

        atraso = calculaAtraso(horario, horaReal)
        novaPista.append([idVoo, horaReal, atraso, intervalo])
        horarioLiberado = calculaLiberacao(horaReal, intervalo)
    return novaPista

# melhor local
def refinaSolucao(P1, P2):

    # guarda a solucao ex5
    melhorP1 = [voo[:] for voo in P1]
    melhorP2 = [voo[:] for voo in P2]
    melhorAtraso = calculaAtrasoTotal(melhorP1, melhorP2)
    
    maxRefinamentos = 30
    for _ in range(maxRefinamentos):
        encontrouMelhora = False
        P1Atual = [voo[:] for voo in melhorP1]
        P2Atual = [voo[:] for voo in melhorP2]
        
        # melhor Local troca p1xp2
        for i in range(len(P1Atual)):
            for j in range(len(P2Atual)):
                novaP1 = [voo[:] for voo in P1Atual]
                novaP2 = [voo[:] for voo in P2Atual]
                novaP1[i], novaP2[j] = novaP2[j], novaP1[i]
        
                novaP1 = recalculaCronogramaPista(novaP1)
                novaP2 = recalculaCronogramaPista(novaP2)
                atrasoNovo = calculaAtrasoTotal(novaP1, novaP2)
        
                if atrasoNovo < melhorAtraso:
                    melhorAtraso = atrasoNovo
                    melhorP1 = [voo[:] for voo in novaP1]
                    melhorP2 = [voo[:] for voo in novaP2]
                    encontrouMelhora = True

        if encontrouMelhora == False:
            break

    return melhorP1, melhorP2

# grasp completo
melhorP1Global = []
melhorP2Global = []
melhorAtrasoGlobal = 999999999

tentativas = 10
for tentativa in range(tentativas):
    print(tentativa)
    # ex5 fase construtiva
    P1, P2 = constroiSolucao()

    # ex6 refinamento
    P1, P2 = refinaSolucao(P1, P2)
    atrasoAtual = calculaAtrasoTotal(P1, P2)

    if atrasoAtual < melhorAtrasoGlobal:
        melhorAtrasoGlobal = atrasoAtual
        melhorP1Global = [voo[:] for voo in P1]
        melhorP2Global = [voo[:] for voo in P2]

print("\nMelhor Pista 1")
for voo in melhorP1Global:
    print(voo)

print("\nMelhor Pista 2")
for voo in melhorP2Global:
    print(voo)

print("\nMelhor atraso encontrado:", melhorAtrasoGlobal)