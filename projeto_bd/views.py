from django.shortcuts import render
from projeto.models import utilizador
from projeto.models import torneio
from projeto.models import equipa
from projeto.models import jogo
from projeto.models import notificacao
from projeto.models import movimentos
from projeto.models import jogador_equipa
from projeto.models import jogador
from projeto.models import reserva_torneio
from projeto.models import substituicao
from projeto.models import classificacao
import operator
import math
from datetime import date, timedelta
import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.core.exceptions import MultipleObjectsReturned
import decimal
import random
from os import path

id = ''
torneio_nome = ''
nome_jogador = ''
nome_equipa = ''
id_jogo = ''
# --------------- ANTONIO ---------------


def meusjogos(request):
    user = utilizador.objects.get(username=id)
    #SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" FROM "projeto_utilizador" WHERE "projeto_utilizador"."username" = \'silcodon\''
    equipas = jogador_equipa.objects.filter(jogador_utilizador_cc=user)
    #SELECT "projeto_jogador_equipa"."id", "projeto_jogador_equipa"."jogador_utilizador_cc_id", "projeto_jogador_equipa"."posicao", "projeto_jogador_equipa"."estatuto", "projeto_jogador_equipa"."equipa_nome_id" FROM "projeto_jogador_equipa" WHERE "projeto_jogador_equipa"."jogador_utilizador_cc_id" = b
    equipas_nomes = equipas.values_list('equipa_nome', flat=True).distinct()
    #SELECT DISTINCT "projeto_jogador_equipa"."equipa_nome_id" FROM "projeto_jogador_equipa" WHERE "projeto_jogador_equipa"."jogador_utilizador_cc_id" = b
    query_results = jogo.objects.filter(nome_equipa_a__in=equipas_nomes, data_inicio__lte=(datetime.datetime.now(
    )+timedelta(days=7))) | jogo.objects.filter(nome_equipa_b__in=equipas_nomes, data_inicio__lte=(datetime.datetime.now()+timedelta(days=7)))
    #SELECT "projeto_jogo"."id", "projeto_jogo"."data_inicio", "projeto_jogo"."golos_equipa_a", "projeto_jogo"."golos_equipa_b", "projeto_jogo"."nome_equipa_a_id", "projeto_jogo"."nome_equipa_b_id", "projeto_jogo"."nome_torneio_id", "projeto_jogo"."campo" FROM "projeto_jogo" WHERE (("projeto_jogo"."data_inicio" >= 2019-12-07 AND "projeto_jogo"."nome_equipa_a_id" IN (SELECT DISTINCT U0."equipa_nome_id" FROM "projeto_jogador_equipa" U0 WHERE U0."jogador_utilizador_cc_id" = b)) OR ("projeto_jogo"."data_inicio" >= 2019-12-07 AND "projeto_jogo"."nome_equipa_b_id" IN (SELECT DISTINCT U0."equipa_nome_id" FROM "projeto_jogador_equipa" U0 WHERE U0."jogador_utilizador_cc_id" = b)))
    context = {
        'query_results': query_results,
    }
    return render(request, 'JogosJogador.html', context)


def proximosjogos(request, equipanome):
    equipaver = equipa.objects.get(nome=equipanome)
    #'SELECT "projeto_equipa"."nome", "projeto_equipa"."torneio_nome_id", "projeto_equipa"."isfull", "projeto_equipa"."n_jogadores", "projeto_equipa"."jogador_utilizador_cc_id" FROM "projeto_equipa" WHERE "projeto_equipa"."nome" = \'ab\''
    query_results = jogo.objects.filter(
        nome_equipa_a=equipaver) | jogo.objects.filter(nome_equipa_b=equipaver)
    #SELECT * FROM "projeto_jogo" WHERE "projeto_jogo"."nome_equipa_a" = "\'ab\'" OR "projeto_jogo"."nome_equipa_b" = "\'ab\'"
    context = {
        'equipaver': equipaver,
        'query_results': query_results,
    }
    return render(request, 'ProximosJogos.html', context)


def listaequip(request, torneionome):
    query2 = torneio.objects.get(nome=torneionome)
    #'SELECT "projeto_torneio"."nome", "projeto_torneio"."data_inicio", "projeto_torneio"."data_fim", "projeto_torneio"."dias", "projeto_torneio"."hora_inicio", "projeto_torneio"."campos", "projeto_torneio"."dia_sem_jogo", "projeto_torneio"."gestor_utilizador_cc_id", "projeto_torneio"."n_jogos" FROM "projeto_torneio" WHERE "projeto_torneio"."nome" = \'a\''
    query_results = equipa.objects.filter(torneio_nome=query2)
    #'SELECT "projeto_equipa"."nome", "projeto_equipa"."torneio_nome_id", "projeto_equipa"."isfull", "projeto_equipa"."n_jogadores", "projeto_equipa"."jogador_utilizador_cc_id" FROM "projeto_equipa" WHERE "projeto_equipa"."torneio_nome_id" = \'a\''
    if len(query_results) < 16 and id != '':
        size = 1
    else:
        size = 0
    return render(request, 'ListaEquipas2.html', {"query_results": query_results, "size": size, "query2": query2})


def verequip(request, equipa_nome):
    query_results = equipa.objects.get(nome=equipa_nome)
    #'SELECT "projeto_equipa"."nome", "projeto_equipa"."torneio_nome_id", "projeto_equipa"."isfull", "projeto_equipa"."n_jogadores", "projeto_equipa"."jogador_utilizador_cc_id" FROM "projeto_equipa" WHERE "projeto_equipa"."nome" = \'ab\''
    jogadores_equipa = jogador_equipa.objects.filter(equipa_nome=query_results)
    #'SELECT "projeto_jogador_equipa"."id", "projeto_jogador_equipa"."jogador_utilizador_cc_id", "projeto_jogador_equipa"."posicao", "projeto_jogador_equipa"."estatuto", "projeto_jogador_equipa"."equipa_nome_id" FROM "projeto_jogador_equipa" WHERE ("projeto_jogador_equipa"."equipa_nome_id" = \'ab\' AND "projeto_jogador_equipa"."jogador_utilizador_cc_id" = \'b\')'

    if id != '':
        loggado = utilizador.objects.get(username=id)
	#'SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" FROM "projeto_utilizador" WHERE "projeto_utilizador"."username" = \'silcodon\''
        if jogador_equipa.objects.filter(equipa_nome=query_results, jogador_utilizador_cc=loggado).exists():
	#'SELECT (1) AS "a" FROM "projeto_jogador_equipa" WHERE ("projeto_jogador_equipa"."equipa_nome_id" = \'ab\' AND "projeto_jogador_equipa"."jogador_utilizador_cc_id" = \'a\')  LIMIT 1'
            jogador_equipa_loggado = 1
        else:
            jogador_equipa_loggado = 2
    else:
        loggado = 1
        jogador_equipa_loggado = 0

    context = {
        'query_results': query_results,
        'jogadores_equipa': jogadores_equipa,
        'loggado': loggado,
        'jogador_equipa_loggado': jogador_equipa_loggado,
    }
    if request.method == "POST" and 'sairequipa' in request.POST:
        jogador_equipa.objects.get(
            equipa_nome=query_results, jogador_utilizador_cc=loggado).delete()
	#'SELECT "projeto_jogador_equipa"."id", "projeto_jogador_equipa"."jogador_utilizador_cc_id", "projeto_jogador_equipa"."posicao", "projeto_jogador_equipa"."estatuto", "projeto_jogador_equipa"."equipa_nome_id" FROM "projeto_jogador_equipa" WHERE ("projeto_jogador_equipa"."equipa_nome_id" = \'ab\' AND "projeto_jogador_equipa"."jogador_utilizador_cc_id" = \'b\')'
	#'DELETE FROM "projeto_jogador_equipa" WHERE "projeto_jogador_equipa"."id" IN (100)'
        query_results.n_jogadores -= 1
        query_results.save()
	#'UPDATE "projeto_equipa" SET "torneio_nome_id" = \'a\', "isfull" = false, "n_jogadores" = 0, "jogador_utilizador_cc_id" = \'a\' WHERE "projeto_equipa"."nome" = \'ab\''
        request.method = 'GET'
        return verequip(request, equipa_nome)
    return render(request, 'PerfilEquipa.html', context)


def editarequip(request, equipa_nome):
    editaequipa = equipa.objects.get(nome=equipa_nome)
    #'SELECT "projeto_equipa"."nome", "projeto_equipa"."torneio_nome_id", "projeto_equipa"."isfull", "projeto_equipa"."n_jogadores", "projeto_equipa"."jogador_utilizador_cc_id" FROM "projeto_equipa" WHERE "projeto_equipa"."nome" = \'ab\''
    jogadores_equipa = jogador_equipa.objects.filter(equipa_nome=editaequipa)
    #'SELECT "projeto_jogador_equipa"."id", "projeto_jogador_equipa"."jogador_utilizador_cc_id", "projeto_jogador_equipa"."posicao", "projeto_jogador_equipa"."estatuto", "projeto_jogador_equipa"."equipa_nome_id" FROM "projeto_jogador_equipa" WHERE ("projeto_jogador_equipa"."equipa_nome_id" = \'ab\')'
    context = {
        'jogadores_equipa': jogadores_equipa,
        'editaequipa': editaequipa,
    }
    if request.method == "POST" and 'tornarcapitao' in request.POST:
        cc_jogador = utilizador.objects.get(
            username=request.POST['tornarcapitao'])
	#'SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" FROM "projeto_utilizador" WHERE "projeto_utilizador"."username" = \'s\''	
        editaequipa.jogador_utilizador_cc = cc_jogador
        editaequipa.save()
	#'UPDATE "projeto_equipa" SET "torneio_nome_id" = \'a\', "isfull" = false, "n_jogadores" = 0, "jogador_utilizador_cc_id" = \'s\' WHERE "projeto_equipa"."nome" = \'ab\''
	
        return verequip(request, equipa_nome)
    if request.method == "POST" and 'nomeperfil' in request.POST:
        cc_jogador = utilizador.objects.get(
            username=request.POST['nomeperfil'])
	#'SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" FROM "projeto_utilizador" WHERE "projeto_utilizador"."username" = \'s\''
        jogadorequipa = jogador_equipa.objects.get(
            equipa_nome=editaequipa, jogador_utilizador_cc=cc_jogador)
	#'SELECT "projeto_jogador_equipa"."id", "projeto_jogador_equipa"."jogador_utilizador_cc_id", "projeto_jogador_equipa"."posicao", "projeto_jogador_equipa"."estatuto", "projeto_jogador_equipa"."equipa_nome_id" FROM "projeto_jogador_equipa" WHERE ("projeto_jogador_equipa"."equipa_nome_id" = \'ab\' AND "projeto_jogador_equipa"."jogador_utilizador_cc_id" = \'b\')'
        jogadorequipa.delete()
	#'DELETE FROM "projeto_jogador_equipa" WHERE "projeto_jogador_equipa"."id" IN (100)'
        editaequipa.n_jogadores -= 1
        editaequipa.save()
	#'UPDATE "projeto_equipa" SET "torneio_nome_id" = \'a\', "isfull" = false, "n_jogadores" = 0, "jogador_utilizador_cc_id" = \'a\' WHERE "projeto_equipa"."nome" = \'ab\''
        return render(request, 'EditarEquipa.html', context)
    if request.method == "POST" and 'guardar' in request.POST:
        cc_jogador = utilizador.objects.get(username=request.POST['guardar'])
	#'SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" FROM "projeto_utilizador" WHERE "projeto_utilizador"."username" = \'s\''
        jogadorequipa = jogador_equipa.objects.get(
            equipa_nome=editaequipa, jogador_utilizador_cc=cc_jogador)
	#'SELECT "projeto_jogador_equipa"."id", "projeto_jogador_equipa"."jogador_utilizador_cc_id", "projeto_jogador_equipa"."posicao", "projeto_jogador_equipa"."estatuto", "projeto_jogador_equipa"."equipa_nome_id" FROM "projeto_jogador_equipa" WHERE ("projeto_jogador_equipa"."equipa_nome_id" = \'ab\' AND "projeto_jogador_equipa"."jogador_utilizador_cc_id" = \'b\')'
	
        jogadorequipa.posicao = request.POST['posicoes']
        jogadorequipa.estatuto = request.POST['estatuto']
        jogadorequipa.save()
	#'UPDATE "projeto_jogador_equipa" SET "jogador_utilizador_cc_id" = \'b\', "posicao" = \'DEF\', "estatuto" = \'Suplente\', "equipa_nome_id" = \'ab\' WHERE "projeto_jogador_equipa"."id" = 100'
        return render(request, 'EditarEquipa.html', context)
    return render(request, 'EditarEquipa.html', context)


def meuperfil(request):
    user = utilizador.objects.get(username=id)
    #'SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" 
	#FROM "projeto_utilizador" 
	#WHERE "projeto_utilizador"."username" = \'silcodon\''
    if user.isadmin == True:
        isAdmin = 1
    else:
        isAdmin = 0
    if request.method == "POST" and 'dinheiro' in request.POST:
        return add_money(request)
    if request.method == "POST" and 'pedirsubstituicao' in request.POST:
        return substituicao1(request)
    return render(request, 'MeuPerfil.html', {'user': user, "isAdmin": isAdmin})


def perfiljogador(request, nome):
    if request.method == "POST" and 'expulsao' in request.POST:
        nomeexpulsar = request.POST['expulsao']
        utilizador.objects.get(username=nomeexpulsar).delete()
        return home(request)

    user = utilizador.objects.get(username=nome)
	#'SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" FROM "projeto_utilizador" WHERE "projeto_utilizador"."username" = \'s\''
    if id != '':
        loggado = utilizador.objects.get(username=id)
    else:
        loggado = 1

    context = {
        'user': user,
        'loggado': loggado,
    }
    return render(request, 'PerfilJogador.html', context)


def editarperfil(request):
    user = utilizador.objects.get(username=id)
    #'SELECT "projeto_utilizador"."cc", "projeto_utilizador"."username", "projeto_utilizador"."password", "projeto_utilizador"."nome", "projeto_utilizador"."apelido", "projeto_utilizador"."email", "projeto_utilizador"."isadmin", "projeto_utilizador"."contacto", "projeto_utilizador"."n_vitorias", "projeto_utilizador"."saldo", "projeto_utilizador"."dinheiroGasto", "projeto_utilizador"."pagamentosRegularizados", "projeto_utilizador"."posicao_preferida", "projeto_utilizador"."bio", "projeto_utilizador"."isgestor", "projeto_utilizador"."isOnline", "projeto_utilizador"."pedidoSubs" FROM "projeto_utilizador" WHERE "projeto_utilizador"."username" = \'silcodon\''
    if request.method == 'POST' and 'confirmar' in request.POST:
        if not request.POST['tel'].isnumeric():
            messages.info(request, 'Insira apenas dígitos', extra_tags='tlm')
            return render(request, 'EditarPerfil.html', {'user': user})
        else:
            user.contacto = request.POST['tel']
            user.email = request.POST['email']
            user.bio = request.POST['bio']
            user.posicao_preferida = request.POST['posicoes']
            user.save()
	    #'UPDATE "projeto_utilizador" SET "username" = \'silcodon\', "password" = \'a\', "nome" = \'antonio\', "apelido" = \'maria\', "email" = \'antoniomaria100@outlook.pt\', "isadmin" = false, "contacto" = 916479356, "n_vitorias" = 0, "saldo" = \'0.00\', "dinheiroGasto" = \'0.00\', "pagamentosRegularizados" = false, "posicao_preferida" = \'None\', "bio" = \'Ola\', "isgestor" = false, "isOnline" = true, "pedidoSubs" = false WHERE "projeto_utilizador"."cc" = \'a\''
            return render(request, 'MeuPerfil.html', {'user': user})
    if request.method == 'POST' and 'apagar' in request.POST:
        user.delete()
	#'DELETE FROM "projeto_utilizador" WHERE "projeto_utilizador"."cc" IN (\'a\')'
        return render(request, 'MainMenu.html')
    return render(request, 'EditarPerfil.html', {'user': user})

# -----------------CARLOS----------------


def notificacoes(request, nometorneio):
    #Select * From projeto_torneio
    #Where nome = nometorneio
    torneioo = torneio.objects.get(nome=nometorneio)
    #Select * From projeto_torneio
    #Where nome = nometorneio
    query_results2 = torneio.objects.filter(nome=nometorneio)
    nomee = torneioo.nome
    #Select * From projeto_notificacao
    #Where nome_torneio_id = torneioo
    query_results = notificacao.objects.filter(nome_torneio=torneioo)
    if request.method == "POST" and "conf" in request.POST:
        golos = request.POST.get('golosA')
        print("Golos = " + golos)

    return render(request, 'notificacoes.html', {"query_results": query_results2, "notificacoes": query_results})


def editar_resultado(request, idjogo):

    #Select * From projeto_torneio
    #Where nome = torneionome;
    torneioo = torneio.objects.get(nome=torneio_nome)
    torneio2 = torneio.objects.filter(nome=torneio_nome)

    #Select * From projeto_jogo
    #Where id = idjogo
    query_results = jogo.objects.filter(id=idjogo)

    #Select *
    #from projeto_jogo jogo, projeto_torneio torneio
    #where jogo.nome_torneio_id = torneioo
    query_results2 = jogo.objects.filter(nome_torneio=torneioo)

    soma = 0
    if request.method == "POST" and "guardar" in request.POST:



        if not request.POST.get('golos_casa').isnumeric():
            soma += 1
            messages.info(request, 'Insira apenas dígitos',
                          extra_tags='golosAerr')

        if not request.POST.get('golos_fora').isnumeric():
            soma += 1
            messages.info(request, 'Insira apenas dígitos',
                          extra_tags='golosBerr')
        if soma > 0:
            return render(request, 'editar_resultado.html', {"query_results": query_results})
        else:

            #Select * From projeto_jogo
            #Where id = idjogo
            jogos = jogo.objects.get(id=idjogo)

        #Select * From projeto_classificacao
        #Where cTorneio_id = torneioo and cEquipa_id = jogos.nome_equipa_a
        classifA = classificacao.objects.get(
            cTorneio=torneioo, cEquipa=jogos.nome_equipa_a)
        #Select * From projeto_classificacao
        #Where cTorneio_id = torneioo and cEquipa_id = jogos.nome_equipa_b
        classifB = classificacao.objects.get(
            cTorneio=torneioo, cEquipa=jogos.nome_equipa_b)


        classifA.cMarcados += int(request.POST.get('golos_casa'))
        classifA.cSofridos += int(request.POST.get('golos_fora'))
        classifB.cMarcados += int(request.POST.get('golos_fora'))
        classifB.cSofridos += int(request.POST.get('golos_casa'))

        if request.POST.get('golos_casa') > request.POST.get('golos_fora'):
            classifA.cPontos += 3
            classifB.cPontos += 0
        if request.POST.get('golos_casa') < request.POST.get('golos_fora'):
            classifA.cPontos += 0
            classifB.cPontos += 3
        if request.POST.get('golos_casa') == request.POST.get('golos_fora'):
            classifA.cPontos += 1
            classifB.cPontos += 1

        if jogos.golos_equipa_a != None and jogos.golos_equipa_b != None:
            if jogos.golos_equipa_a != request.POST.get('golos_casa') and jogos.golos_equipa_b != request.POST.get('golos_fora'):
                nova_not = notificacao()
                nova_not.texto = "O resultado inserido por ambos os capitães foi diferente!"
                nova_not.nome_torneio = torneioo
                nova_not.nome_equipa_a = jogos.nome_equipa_a
                nova_not.nome_equipa_b = jogos.nome_equipa_b
                #Insert into projeto_notificacao (texto, nome_equipa_a_id, nome_equipa_b_id, nome_torneio_id)
                #Values
                #(nova_not.texto, nova_not.nome_equipa_a, nova_not.nome_equipa_b, nova_not.nome_torneio)
                nova_not.save()
        else:
            #Update projeto_classificacao
            #set cMarcados = cMarcados + classifA.cMarcados, cSofridos = cSofridos + classifA.cSofridos,cPontos = cPontos + classifA.cPontos
            #Where cTorneio_id = torneioo and cEquipa_id = jogos.nome_equipa_a
            classifA.save()

            #Update projeto_classificacao
            #set cMarcados = cMarcados + classifB.cMarcados, cSofridos = cSofridos + classifB.cSofridos,cPontos = cPontos + classifB.cPontos
            #Where cTorneio_id = torneioo and cEquipa_id = jogos.nome_equipa_b
            classifB.save()

            #Update projeto_torneio
            #set n_jogos = n_jogos + 1
            #Where nome = torneio_nome
            torneio3 = torneio.objects.get(nome = torneio_nome)
            torneio3.n_jogos += 1
            torneio3.save()


        #Update projeto_jogo
        #set golos_equipa_a = request.POST.get('golos_casa'), golos_equipa_b = request.POST.get('golos_fora')
        #Where id = idjogo
        jogos.golos_equipa_a = request.POST.get('golos_casa')

        jogos.golos_equipa_b = request.POST.get('golos_fora')

        jogos.save()

        if id != '':
            user = utilizador.objects.get(username=id)
            loggado = 1
            cc1 = user.cc
        else:
            cc1 = 0
            loggado = 0

        context = {
            "query_results": query_results2,
            "torneio": torneio2,
            "cc": cc1,
            "loggado": loggado
        }

        return render(request, 'Resultado_jogos.html', context)

    return render(request, 'editar_resultado.html', {"query_results": query_results})


def login(request):

    soma = 0
    if request.method == 'POST':
        #Select * From projeto_utilizador
        #Where email = request.POST['inputEmail']
        if not utilizador.objects.filter(email=request.POST['inputEmail']).exists():
            soma += 1
            messages.info(request, 'Email não encontrado!',
                          extra_tags='erremail')
        else:
            #Select * From projeto_utilizador
            #Where email = request.POST['inputEmail']
            user = utilizador.objects.get(email=request.POST['inputEmail'])

            if (request.POST['inputPassword']) != user.password:
                soma += 1
                messages.info(
                    request, 'Combinação Email/Password não encontrado!', extra_tags='errpass')
        if soma > 0:
            return render(request, 'login2.html')
        else:
            #Select * From projeto_utilizador
            #Where email = request.POST['inputEmail']
            user = utilizador.objects.get(email=request.POST['inputEmail'])
            global id
            id = user.username

            #Update projeto_utilizador
            #set isOnline = True
            #Where email = request.POST['inputEmail']
            user.isOnline = True
            user.save()

            #Select * From projeto_utilizador
            #Where username = id
            query_results = utilizador.objects.filter(username=id)
            #Select * From projeto_utilizador
            #Where username = id
            user = utilizador.objects.get(username=id)
            #Select * From projeto_torneio
            #Where gestor_utilizador_cc_id = user
            gestor_de = torneio.objects.filter(gestor_utilizador_cc=user)
            number = len(gestor_de)
            if user.isadmin:
                return render(request, 'MainMenuAdmin.html', {"query_results": query_results, "number": number})
            if not user.isadmin:
                return render(request, 'MainMenu_user.html', {"query_results": query_results, "number": number})

    return render(request, 'login2.html')


def criar_torneio(request):
    #Select * From projeto_utilizador
    #Where username = id
    query_results = utilizador.objects.filter(username=id)
    #Select * From projeto_utilizador
    #Where username = id
    user2 = utilizador.objects.get(username=id)
    #Select * From projeto_utilizador
    #Where username = id
    user = utilizador.objects.get(username=id)
    if user.isadmin == True:
        eAdmin = 1
    else:
        eAdmin = 0

    if 'criar' in request.POST:
        post = torneio()
        soma = 0
        #Select * From projeto_torneio
        #Where nome = request.POST['name']
        if torneio.objects.filter(nome=request.POST['name']).exists():
            soma += 1
            messages.info(request, 'O nome já foi utilizado!',
                          extra_tags='mnome')
        if soma > 0:
            return render(request, 'criar_torneios.html')
        else:
            post.nome = request.POST['name']
            post.data_inicio = request.POST['date_inicio']
            post.data_fim = request.POST['date_fim']
            post.dias = request.POST['dia_jogo']
            post.hora_inicio = request.POST['hora_jogo']
            post.campos = request.POST['campo']
            post.dia_sem_jogo = request.POST['dia_sem_jogo']
            post.gestor_utilizador_cc = user2
            post.n_jogos = 0
            post.isGestor = True
            #Insert into projeto_torneio (nome, data_inicio, data_fim, dias, hora_inicio, campos, dia_sem_jogo, gestor_utilizador_cc_id, n_jogos, isGestor)
            #values
            #(request.POST['name'], request.POST['date_inicio'], request.POST['date_fim'],
            #request.POST['dia_jogo'], request.POST['hora_jogo'], request.POST['campo'], request.POST['dia_sem_jogo'], user2, 0, True)

            post.save()
    if 'cancelar' in request.POST:
        if eAdmin == 1:
            return render(request, 'MainMenuAdmin.html', {"query_results": query_results})
        else:
            return render(request, 'MainMenu_user.html', {"query_results": query_results})

    return render(request, 'criar_torneios.html', {"query_results": query_results, "eAdmin": eAdmin})


def listatorneio(request):
    if id != "":
        #Select * from projeto_utilizador
        #Where username = id
        user = utilizador.objects.filter(username=id)
        #Select * from projeto_utilizador
        #Where username = id
        isadminn = utilizador.objects.get(username=id).isadmin

        if isadminn == True:
            isAdmin = 1
        else:
            isAdmin = 0

        size = 1
    else:
        size = 0
        isAdmin = 0
    #Select * From projeto_torneio
    query_results = torneio.objects.all()
    return render(request, 'ListaTorneios2.html', {"query_results": query_results, "size": size, "isAdmin": isAdmin})


def resultado_jogos(request, torneionome):
    global torneio_nome
    torneio_nome = torneionome
    #Select * From projeto_torneio
    #Where nome = torneionome
    torneioo = torneio.objects.get(nome=torneionome)
    #Select * From projeto_torneio
    #Where nome = torneionome
    torneio2 = torneio.objects.filter(nome=torneionome)
    #Select * From projeto_jogo
    #Where nome_torneio_id = torneioo
    query_results = jogo.objects.filter(nome_torneio=torneioo)
    if id != '':
        #Select * From projeto_utilizador
        #Where username = id
        user = utilizador.objects.get(username=id)
        loggado = 1
        cc1 = user.cc
    else:
        cc1 = 0
        loggado = 0

    context = {
        "query_results": query_results,
        "torneio": torneio2,
        "cc": cc1,
        "loggado": loggado
    }

    return render(request, 'resultado_jogos.html', context)


def gerar_jogos(request, torneionome):
    #Select * From projeto_torneio
    #Where nome = torneionome
    query_results = torneio.objects.filter(nome=torneionome)
    #Select * From projeto_utilizador
    #Where username = id
    user = utilizador.objects.get(username=id)
    #Select * From projeto_torneio
    #Where nome = torneionome
    torneioo = torneio.objects.get(nome=torneionome)
    #Delete From projeto_jogo
    #Where nome_torneio_id = torneioo
    jogo.objects.filter(nome_torneio=torneioo).delete()
    #Select * From projeto_equipa
    #Where torneio_nome = torneionome
    query_equipas = equipa.objects.filter(torneio_nome=torneionome)
    teams = list()
    isadminn = user.isadmin
    #Select * From projeto_torneio
    #Where nome = torneionome

    #Update projeto_torneio
    #Set n_jogos = 0
    #Where nome = torneionome
    torneio4 = torneio.objects.get(nome = torneionome)
    torneio4.n_jogos = 0
    torneio4.save()

    #Update projeto_classificacao
    #set cPontos = 0, cMarcados = 0, cSofridos = 0
    #where cTorneio_id = torneio4
    classif = classificacao.objects.filter(cTorneio = torneio4)
    for classi in classif:
        classi.cPontos = 0
        classi.cMarcados = 0
        classi.cSofridos = 0
        classi.save()


    if isadminn == True:
        isAdmin = 1
    else:
        isAdmin = 0

    for elem in query_equipas:
        teams.append(elem.nome)

    n = len(teams)
    matchs = []
    fixtures = []
    return_matchs = []
    for fixture in range(1, n):
        for i in range(int(n/2)):
            matchs.append((teams[i], teams[n - 1 - i]))
            return_matchs.append((teams[n - 1 - i], teams[i]))
        teams.insert(1, teams.pop())
        fixtures.insert(int(len(fixtures)/2), matchs)
        fixtures.append(return_matchs)
        matchs = []
        return_matchs = []

    n_jogos = 0
    data_in = torneioo.data_inicio
    data_fin = torneioo.data_fim

    ano_in = str(data_in).split("-")[0]
    mes_in = str(data_in).split("-")[1]
    dia_in = str(data_in).split("-")[2]
    ano_fin = str(data_fin).split("-")[0]
    mes_fin = str(data_fin).split("-")[1]
    dia_fin = str(data_fin).split("-")[2]

    d1 = date(int(ano_in), int(mes_in), int(dia_in))
    d2 = date(int(ano_fin), int(mes_fin), int(dia_fin)+1)

    intervalo = diff_dates(d1, d2)  # Numero de dias do torneio

    #print("Data de Inicio: " +  "Dia " + dia_in + " do " + mes_in + " de " + ano_in)
    #print("Data de Fim: " + "Dia " + dia_fin + " do " + mes_fin + " de " + ano_fin)
    #print("Total de dias: " + str(intervalo))

    for fixtur in fixtures:  # Este ciclo é para saber o numero de jogos
        for jogoo in fixtur:  # Cada tuplo na lista (Equipa 1 vs Equipa 2)
            n_jogos += 1

    print(n_jogos)
    jogos_por_dia = math.ceil(n_jogos / intervalo)

    i = 0
    aux = 1
    data_jogo = data_in

    #print("Vai haver " +  str(jogos_por_dia) + " jogos por dia!")
    for fixtur in fixtures:
        # print (str(fixtur)+"\n") #Conjunto de 2 (tuplos numa lista) jogos neste caso
        for jogoo in fixtur:  # Cada tuplo na lista (Equipa 1 vs Equipa 2)

            #Select * From projeto_equipa
            #Where nome = jogoo[0]
            equipa_a = equipa.objects.get(nome=jogoo[0])
            #Select * From projeto_equipa
            #Where nome = jogoo[1]
            equipa_b = equipa.objects.get(nome=jogoo[1])
            #print (jogo)
            i += 1

            #Insert into projeto_jogo
            #Values(equipa_a, equipa_b, torneioo, torneioo.campos, campoo, data_jogo)
            game = jogo()
            game.nome_equipa_a = equipa_a
            game.nome_equipa_b = equipa_b
            game.nome_torneio = torneioo
            campoo = torneioo.campos
            game.campo = campoo
            game.data_inicio = data_jogo
            game.save()

            aux += 1
            #print(str(i) + "º jogo: "+ equipa_a.nome + " vs "+ equipa_b.nome + " no dia " +  str(data_jogo))
            if aux == jogos_por_dia:
                datee = datetime.datetime.strptime(
                    str(data_jogo), "%Y-%m-%d").date()
                data_jogo = datee + timedelta(days=1)
                aux = 0

            #datetime.strftime(data_jogo, "%Y-%m-%d")

    return render(request, 'gerarjogos.html', {"query_results": query_results, "user": user, "isAdmin": isAdmin})


def diff_dates(date1, date2):
    return abs(date2-date1).days


def fixtures(teams):
    if len(teams) % 2:
        # if team number is odd - use 'day off' as fake team
        teams.append('Day off')

    rotation = list(teams)       # copy the list

    fixtures = []
    for i in range(0, len(teams)-1):
        fixtures.append(rotation)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    return fixtures


# -------------DIOGO---------------------
def home(request):
    global id
    id = ""
    return render(request, 'MainMenu.html')


def register(request):
    if request.method == 'POST':
        post = utilizador()
        soma = 0
        if not request.POST['contacto'].isnumeric():
            messages.info(request, 'Insira apenas dígitos', extra_tags='tlm')
            soma += 1
        #SELECT * FROM projeto_utilizador WHERE contacto = request.POST['contacto'] 
        elif utilizador.objects.filter(contacto=request.POST['contacto']).exists():
            messages.info(
                request, 'O contacto telefónico já foi utilizado', extra_tags='tlm')
            soma += 1    
        if request.POST['password'] != request.POST['repassword']:
            soma += 1
            messages.info(request, 'As passwords não coincidem', extra_tags='pw')
        #SELECT * FROM projeto_utilizador WHERE cc = request.POST['cc']
        if utilizador.objects.filter(cc=request.POST['cc']).exists():
            soma += 1
            messages.info(
                request, 'O cartão de cidadão já foi utilizado', extra_tags='carc')
        #SELECT * FROM projeto_utilizador WHERE username = request.POST['username']
        if utilizador.objects.filter(username=request.POST['username']).exists():
            messages.info(request, 'O username já foi utilizado',
                          extra_tags='uname')
            soma += 1
        #SELECT * FROM projeto_utilizador WHERE email = request.POST['email']
        if utilizador.objects.filter(email=request.POST['email']).exists():
            messages.info(request, 'O email já foi utilizado',
                          extra_tags='mail')
            soma += 1
        if soma > 0:
            return render(request, 'register2.html')
        else:
            exists = path.exists('user.txt')
            if not exists:
                post.isadmin = True
            post.cc = request.POST['cc']
            post.username = request.POST['username']
            post.nome = request.POST['nome']
            post.apelido = request.POST['apelido']
            post.contacto = request.POST['contacto']
            post.email = request.POST['email']
            post.password = request.POST['password']
            post.save()
            #INSERT INTO projeto_utilizador 
            #VALUES (request.POST['cc'], request.POST['username'], request.POST['password'], request.POST['nome'], request.POST['apelido'], request.POST['email'], true, request.POST['contacto'], 0, 0.00, 0.00, false, NULL, NULL, false, false, false)
    return render(request, 'register2.html')


def home_user(request):
    query_results = utilizador.objects.filter(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id
    user = utilizador.objects.get(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id
    gestor_de = torneio.objects.filter(gestor_utilizador_cc=user)
    #SELECT * FROM projeto_torneio
    #WHERE  gestor_utilizador_cc = user
    number = len(gestor_de)
    print(number)
    return render(request, 'MainMenu_user.html', {"query_results": query_results, "number": number})


def home_admin(request):
    query_results = utilizador.objects.filter(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id
    user = utilizador.objects.get(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id
    gestor_de = torneio.objects.filter(gestor_utilizador_cc=user)
    #SELECT * FROM projeto_torneio
    #WHERE  gestor_utilizador_cc = user
    number = len(gestor_de)
    return render(request, 'MainMenuAdmin.html', {"query_results": query_results, "number": number})


def criareq(request, torneionome):

    query_results = utilizador.objects.filter(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id
    query2 = torneio.objects.filter(nome=torneionome)
    #SELECT * FROM projeto_torneio
    #WHERE nome = torneionome
    torneioo = torneio.objects.get(nome=torneionome)
    #SELECT * FROM projeto_torneio
    #WHERE nome = torneionome
    if request.method == 'POST' and 'cria' in request.POST:
    	#SELECT * FROM projeto_equipa
    	#WHERE nome = request.POST['nameq'] AND torneio_nome = torneioo
        if equipa.objects.filter(nome=request.POST['nameq']).filter(torneio_nome=torneioo).exists():
            messages.info(
                request, 'Já existe uma equipa com o nome inserido', extra_tags='nomeq')
        else:
            user = utilizador.objects.get(username=id)
            #SELECT * FROM projeto_utilizador
    		#WHERE username = id
            post1 = jogador_equipa()
            post2 = equipa()
            post3 = jogador()
            classif = classificacao()

            post3.utilizador_cc = user
            post3.iscaptain = True
            post3.estatuto = 'titular'
            post3.save()
            #INSERT INTO projeto_jogador
            #VALUES (user, True, 'titular')
            post2.nome = request.POST['nameq']
            post2.n_jogadores += 1
            post2.jogador_utilizador_cc = user
            post2.torneio_nome = torneioo
            post2.save()
            #INSERT INTO projeto_equipa
            #VALUES (request.POST['nameq'], n_jogadores + 1, user, torneioo)
            classif.cEquipa = post2
            classif.cTorneio = torneioo
            classif.save()
            #INSERT INTO projeto_classificacao
            #VALUES (post2, torneioo)
            equipaa = equipa.objects.get(nome=post2.nome)
            #SELECT * FROM projeto_equipa
    		#WHERE nome = post2.nome
            post1.equipa_nome = equipaa
            post1.posicao = request.POST['pos']
            post1.jogador_utilizador_cc = user
            post1.save()
            #INSERT INTO projeto_jogador_equipa
            #VALUES (equipaa, request.POST['pos'], user)


            return listaequip(request, torneionome)

    return render(request, 'CriarEquipa.html', {"query_results": query_results, "query2": query2})


def juntarequip(request, equipanome):
    query_results = utilizador.objects.filter(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id
    query_results2 = equipa.objects.filter(nome=equipanome)
    #SELECT * FROM projeto_equipa
    #WHERE nome = equipanome
    context = {
        "query_results": query_results,
        "query_results2": query_results2
    }
    user = utilizador.objects.get(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id
    equipaa = equipa.objects.get(nome=equipanome)
    #SELECT * FROM projeto_equipa
    #WHERE nome = equipanome
    if request.method == 'POST':
        soma = 0

        post1 = jogador_equipa()
        post2 = jogador()
        #SELECT * FROM projeto_jogador_equipa
    	#WHERE jogador_utilizador_cc = user.cc
        if jogador_equipa.objects.filter(jogador_utilizador_cc=user.cc).exists():
            messages.info(request, 'Já se encontra na equipa', extra_tags='je')
            soma += 1
        #SELECT isfull FROM projeto_equipa
        #WHERE nome = equipanome
        if equipaa.isfull:
            messages.info(
                request, 'A equipa já se encontra cheia', extra_tags='ft')
            soma += 1
        if soma > 0:
            return render(request, 'JuntarEquipa.html', context)
        else:
            post2.utilizador_cc = user
            post2.save()
            #INSERT INTO projeto_jogador
            #VALUES (user)
            equipaa.n_jogadores += 1
            equipaa.save()
            #INSERT INTO projeto_equipa
            #VALUES (n_jogadores += 1)
            if equipaa.n_jogadores == 16:
                equipaa.isfull = True
                equipaa.save()

            post1.equipa_nome = equipaa
            post1.posicao = request.POST['pos']
            post1.jogador_utilizador_cc = user
            post1.save()
            #INSERT INTO projeto_jogador_equipa
            #VALUES (equipaa, request.POST['pos'], user)
            

    return render(request, 'JuntarEquipa.html', context)


def editartor(request, nometorneio):
    user = utilizador.objects.filter(username=id)
    #SELECT * FROM projeto_utilizador
    #WHERE username = id

    torneiu = torneio.objects.filter(nome=nometorneio)
    #SELECT * FROM projeto_torneio
    #WHERE nome = nometorneio
    torneioo = torneio.objects.get(nome=nometorneio)
    #SELECT * FROM projeto_torneio
    #WHERE nome = nometorneio

    if request.method == 'POST' and 'conf' in request.POST:
        soma = 0

        if request.POST['datai'] != "":
            torneioo.data_inicio = request.POST['datai']
            soma += 1
        if request.POST['dataf'] != "":
            torneioo.data_fim = request.POST['dataf']
            soma += 1
        if request.POST['dias'] != "":
            torneioo.dias = request.POST['dias']
            soma += 1
        if request.POST['hora'] != "":
            torneioo.hora_inicio = request.POST['hora']
            soma += 1
        if request.POST['diasem'] != "":
            torneioo.dia_sem_jogo = request.POST['diasem']
            soma += 1
        if request.POST['campo'] != "":
            torneioo.campos = request.POST['campo']
            soma += 1
        if soma > 0:
            torneioo.save()
            #INSERT INTO projeto_torneio
            #VALUES (request.POST['datai'], request.POST['dataf'], request.POST['dias'], request.POST['hora'],  request.POST['diasem'],  request.POST['campo'])
        else:
            messages.info(
                request, 'Não efetuou nenhuma alteração!', extra_tags='noalt')
            torneiu = torneio.objects.filter(nome=nometorneio)
            #SELECT * FROM projeto_torneio
    		#WHERE nome = nometorneio
            return render(request, 'EditarTorneio.html', {"query_results": torneiu, "query_results2": user})

    return render(request, 'EditarTorneio.html', {"query_results": torneiu, "query_results2": user})

# -------------- DAVID --------------------


def add_money(request):
    #Select * From projeto_utilizador
    #Where username = id
    query_results = utilizador.objects.filter(username=id)
    #Select * From projeto_utilizador
    #Where username = id
    user = utilizador.objects.get(username=id)
    cc = user.cc
    #Select * From projeto_movimentos
    #Where cc = cc
    pagamentos = movimentos.objects.filter(cc=cc)
    try:
        #Select * From projeto_movimentos
        #Where cc = cc
        pagamentos2 = movimentos.objects.get(cc=cc)
    except MultipleObjectsReturned:
        #Select * From projeto_movimentos
        #Where cc = cc
        movimentos.objects.filter(cc=cc).first()
    except movimentos.DoesNotExist:
        pagamentos2 = movimentos()
        pagamentos2.cc = user
    soma = 0
    if 'montante' in request.POST:
        if request.POST['montante'] == "":
            soma += 1
            messages.info(request, 'Campo obrigatório',
                          extra_tags='montanteerr')
        if soma > 0:
            return render(request, 'add_money.html', {"query_results": query_results})
        else:
            #Update projeto_utilizador
            #set saldo = saldo + request.POST['montante']
            #where username = id
            user.saldo += decimal.Decimal(request.POST['montante'])
            user.save()
            now = datetime.datetime.now()
            #Insert into projeto_movimentos
            #values
            #(now.year, "Depósito", request.POST['montante'], user)
            pagamentos2 = movimentos()
            pagamentos2.cc = user
            pagamentos2.ano = now.year
            pagamentos2.montante = request.POST['montante']
            pagamentos2.pago = "Depósito"
            pagamentos2.save()
    if 'pay' in request.POST:
        #Update projeto_utilizador
        #set saldo = saldo - 20, dinheiroGasto = dinheiroGasto + 20, pagamentosRegularizados = True
        #where username = id
        user.pagamentosRegularizados = True
        user.dinheiroGasto += 20
        user.saldo -= 20
        user.save()
        now = datetime.datetime.now()
        #Insert into projeto_movimentos
        #values
        #(now.year, "pago", 20, user)
        pagamentos2 = movimentos()
        pagamentos2.ano = now.year

        pagamentos2.cc = user
        pagamentos2.pago = "pago"
        pagamentos2.montante = 20
        pagamentos2.save()
    return render(request, 'add_money.html', {"query_results": query_results, "pagamentos": pagamentos})


def substituicao1(request):
    #SELECT *
	#FROM projeto_utilizador
	#WHERE username=id;
    query_results = utilizador.objects.filter(username=id)
	#SELECT *
	#FROM projeto_utilizador
	#WHERE username=id;
    user = utilizador.objects.get(username=id)
    cc1 = user.cc
	#SELECT *
	#FROM projeto_jogador_equipa
	#WHERE jogador_utilizador_cc=cc1;
    jogadorEquipa = jogador_equipa.objects.filter(jogador_utilizador_cc=cc1)
	#SELECT *
	#FROM projeto_substituicao
	#WHERE deUser_id=user;
    Req = substituicao.objects.filter(deUser=user)

    try:
		#SELECT *
		#FROM projeto_jogador_equipa
		#WHERE jogador_utilizador_cc=cc1;
        jogadorEquipa2 = jogador_equipa.objects.get(jogador_utilizador_cc=cc1)
    except jogador_equipa.DoesNotExist:
        jogadorEquipa2 = jogador_equipa()
        jogadorEquipa2.cc = user
    except MultipleObjectsReturned:
		#SELECT *
		#FROM projeto_jogador_equipa
		#WHERE jogador_utilizador_cc=cc1;
        jogador_equipa.objects.filter(jogador_utilizador_cc=cc1).first()

    suplentes = None
    suplentesRes = None

    if 'equipas' in request.POST:
        equipa = request.POST['equipas']
		#SELECT *
		#FROM projeto_jogador_equipa
		#WHERE equipa_nome_id=equipa and estatudo='Suplente';
        if jogador_equipa.objects.filter(equipa_nome=equipa).filter(estatuto="Suplente").exists():
    		#SELECT *
			#FROM projeto_jogador_equipa
			#WHERE equipa_nome_id=equipa and estatudo='Suplente';
            suplentes = jogador_equipa.objects.filter(
                equipa_nome=equipa).filter(estatuto="Suplente")
			#SELECT *
			#FROM projeto_reser_torneio;
            suplentesRes = reserva_torneio.objects.all()
        else:
            suplentes = 1

    if 'pedido' in request.POST:
        user1 = request.POST.get('pedido')
        Equipa = request.POST.get('equipa')
		#SELECT *
		#FROM projeto_utilizador
		#WHERE cc_id=user1;
        user2 = utilizador.objects.get(cc=user1)
        user2.pedidoSubs = True
        user2.save()

        subs = substituicao()
        subs.deUser = user
		#SELECT *
		#FROM projeto_utilizador
		#WHERE cc_id=user1;
        subs.paraUser = utilizador.objects.get(cc=user1)
        subs.equipaDest = Equipa
		#INSERT into projeto_substituicao (deUser_id,paraUser_id,equipaDest)
		#Values(user,subs.paraUser,Equipa)
        subs.save()

    if 'submit1' in request.POST:
        post = utilizador()
        soma = 0
        if not request.POST['contacto'].isnumeric():
            messages.info(request, 'Insira apenas dígitos', extra_tags='tlm')
            soma += 1
		#SELECT *
		#FROM projeto_utilizador
		#WHERE contacto=request.POST['contacto'];
        elif utilizador.objects.filter(contacto=request.POST['contacto']).exists():
            messages.info(
                request, 'O contacto telefónico já foi utilizado', extra_tags='tlm')
            soma += 1
        if request.POST['password'] != request.POST['repassword']:
            soma += 1
            messages.info(request, 'As passwords não coincidem',
                          extra_tags='pw')
		#SELECT *
		#FROM projeto_utilizador
		#WHERE cc=request.POST['cc'];
        if utilizador.objects.filter(cc=request.POST['cc']).exists():
            soma += 1
            messages.info(
                request, 'O cartão de cidadão já foi utilizado', extra_tags='carc')
		#SELECT *
		#FROM projeto_utilizador
		#WHERE username=request.POST['username'];
        if utilizador.objects.filter(username=request.POST['username']).exists():
            messages.info(request, 'O username já foi utilizado',
                          extra_tags='uname')
            soma += 1
		#SELECT *
		#FROM projeto_utilizador
		#WHERE email=request.POST['email'];
        if utilizador.objects.filter(email=request.POST['email']).exists():
            messages.info(request, 'O email já foi utilizado',
                          extra_tags='mail')
            soma += 1
        if soma == 0:
            post.cc = request.POST['cc']
            post.username = request.POST['username']
            post.nome = request.POST['nome12']
            post.apelido = request.POST['apelido']
            post.contacto = request.POST['contacto']
            post.pedidoSubs = True
            post.email = request.POST['email']
            post.password = request.POST['password']
			#Insert into projeto_torneio (cc, username, nome, apelida, contacto, pedidoSubs, email, password)
            #values(request.POST['cc'], request.POST['username'], request.POST['nome12'], request.POST['apelido'],
			#request.POST['contacto'], True, request.POST['email'], request.POST['password'])
            post.save()

            subs = substituicao()
            subs.deUser = user
            subs.paraUser = post
            subs.equipaDest = request.POST['equipaSub']
			#INSERT into projeto_substituicao (deUser_id,paraUser_id,equipaDest)
			#Values(user,post,equest.POST['equipaSub'])
            subs.save()
    if 'anula' in request.POST:
        aux = request.POST.get('anula')
		#SELECT *
		#FROM projeto_substituicao
		#WHERE id=aux;
        anular = substituicao.objects.get(id=aux)
		#DELETE FROM projeto_substituicao WHERE id = aux;
        anular.delete()

    return render(request, 'substituicao.html', {"query_results": query_results, "jogadorEquipa": jogadorEquipa, "suplentes": suplentes, "suplentesRes": suplentesRes, "Req": Req})


def ver_torneio(request, torneionome):
    #SELECT *
	#FROM projeto_torneio
	#WHERE nome=torneionome;
    query = torneio.objects.filter(nome=torneionome)
	#SELECT *
	#FROM projeto_torneio
	#WHERE nome=torneionome;
    torneioo = torneio.objects.get(nome=torneionome)
    #SELECT *
	#FROM projeto_equipa
	#WHERE torneio_nome_id=torneionome;
    query_equipas = equipa.objects.filter(torneio_nome=torneionome)
    aux = 0
    if id == "":
        isLogged = 0
    else:
        isLogged = 1
    for equipaa in query_equipas:
        if equipaa.isfull == False:
            aux = 1
    if len(query_equipas) == 16 and aux == 0:
        haequipa = 1
    else:
        haequipa = 0

    if torneioo.gestor_utilizador_cc.username == id:
        eGestor = 1
    else:
        eGestor = 0

    return render(request, 'info_torneio2.html', {"query_results": query, "eGestor": eGestor, "haequipa": haequipa, "isLogged": isLogged})


def info_torneio(request, nometorneio):
    #SELECT *
	#FROM classificacao
	#WHERE cTorneio_id=nometorneio;
	#order by cPontos
    equipas = classificacao.objects.filter(
        cTorneio=nometorneio).order_by("cPontos")
	#SELECT *
	#FROM projeto_torneio
	#WHERE nome=nometorneio;
    query_results = torneio.objects.filter(nome=nometorneio)
    return render(request, 'info_torneio.html', {"equipas": equipas, "query_results": query_results})


def GerirPedidos(request):
    user = utilizador.objects.get(username=id)
    administrador = user.isadmin
    users = utilizador.objects.all()

    if 'pedido' in request.POST:
        aux = request.POST['pedido']
		#SELECT *
		#FROM projeto_utilizador
		#WHERE cc_id=aux;
        user = utilizador.objects.get(cc=aux)
		#DELETE FROM projeto_utilizador WHERE cc_id = aux;
        user.delete()

    return render(request, 'GerirPedidos.html', {"users": users, "administrador": administrador})


def insc_reserva(request, nometorneio):
    #SELECT *
	#FROM projeto_torneio
	#WHERE nome=nometorneio;
    torneioo = torneio.objects.get(nome=nometorneio)
	#SELECT *
	#FROM projeto_utilizador
	#WHERE username=id;
    user = utilizador.objects.get(username=id)
	#SELECT *
	#FROM projeto_torneio
	#WHERE username=id;
    query_results = torneio.objects.filter(nome=nometorneio)
	#SELECT *
	#FROM projeto_reserva_torneio
	#WHERE cc_id= user and torneio_id = torneioo;
    check = reserva_torneio.objects.filter(cc=user, torneio=torneioo)
    if len(check) == 0:
        isReserva = 0
    else:
        isReserva = 1

    if user.isadmin == True:
        isAdmin = 1
    else:
        isAdmin = 0

    if 'inscreve' in request.POST:
        post = reserva_torneio()
        post.cc = user
        post.torneio = torneioo
		#INSERT into projeto_reserva_torneio (cc_id,torneio_id)
		#Values(user,torneioo)
        post.save()
    if 'remove' in request.POST:
        try:
			#SELECT *
        	#FROM projeto_reserva_torneio
        	#WHERE cc_id= user and torneio_id = torneioo;
            post = reserva_torneio.objects.get(cc=user, torneio=torneioo)
        except MultipleObjectsReturned:
			#SELECT *
        	#FROM projeto_reserva_torneio
        	#WHERE cc_id= user and torneio_id = torneioo;
            post = reserva_torneio.objects.filter(
                cc=user, torneio=torneioo).first()
		#DELETE FROM projeto_reserva_torneio WHERE cc_id = user and torneio_id = torneioo;
        post.delete()

    return render(request, 'insc_reserva.html', {"query_results": query_results, "isAdmin": isAdmin, "isReserva": isReserva})
