"""projeto_bd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.home),
    #path('register.html', views.register),
    #path('', views.editarequip),
    #path('PerfilEquipa.html', views.verequip),
    path('editarequipa/<str:equipa_nome>',
         views.editarequip, name="editarequipa"),
    path('', views.home),
    path('MainMenu.html', views.home, name="mainmenu"),
    path('login2.html', views.login, name="login"),
    path('register2.html', views.register),
    path('editar_resultado/<str:idjogo>',
         views.editar_resultado, name="editarresultado"),
    path('notificacoes/<str:nometorneio>',
         views.notificacoes, name='notificacoes'),
    path('MainMenu_user.html', views.home_user, name="mainmenuuser"),
    path('MainMenuAdmin.html', views.home_admin, name="mainmenuadmin"),
    path('ListaTorneios2.html', views.listatorneio, name="listatorneio"),
    path('criar_torneios.html', views.criar_torneio),
    path('MeuPerfil.html', views.meuperfil, name="meuperfil"),
    path('add_money1', views.add_money, name='add_money1'),
    path('editar', views.editarperfil, name='editar'),
    path('proximosjogos', views.meusjogos, name='proximosjogos'),
    path('info_torneio2/<str:torneionome>',
         views.ver_torneio, name='vertorneio'),
    path('ListaEquipas2/<str:torneionome>',
         views.listaequip, name='listaequipa'),
    path('resultado_jogos/<str:torneionome>',
         views.resultado_jogos, name='resultadojogos'),
    path('substituir', views.substituicao1, name='substituir'),
    path('juntar/<str:equipanome>', views.juntarequip, name='juntar'),
    path('CriarEquipa/<str:torneionome>', views.criareq, name='criarequipa'),
    path('jogador/<str:nome>', views.perfiljogador, name='verperfiljogador'),
    path('equipa/<str:equipa_nome>', views.verequip, name='verequipa'),
    path('gerarjogos/<str:torneionome>', views.gerar_jogos, name='gerarjogo'),
    path('classificacao/<str:nometorneio>',
         views.info_torneio, name='classificacao'),
    path('jogos/<str:equipanome>', views.proximosjogos, name='jogosequipa'),
    path('editartorneio/<str:nometorneio>',
         views.editartor, name="editartorneio"),
    path('jogos/<str:equipanome>', views.proximosjogos, name='jogosequipa'),
    path('GerirPedidos.html', views.GerirPedidos, name="gerirpedidos"),
    path('insc_reserva/<str:nometorneio>', views.insc_reserva, name='reserva')
    #path('', views.meuperfil),
    #path('', views.perfiljogador),
    #path('', views.editarperfil),
]
