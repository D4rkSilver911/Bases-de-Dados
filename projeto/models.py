from django.db import models

# Create your models here.


class utilizador(models.Model):
    cc = models.CharField(max_length=512, primary_key=True, unique=True)
    username = models.CharField(max_length=512, default='', unique=True)
    password = models.CharField(max_length=512, default='')
    nome = models.CharField(max_length=512, default='')
    apelido = models.CharField(max_length=512, default='')
    email = models.EmailField(max_length=254, default='', unique=True)
    isadmin = models.BooleanField(default=False)
    contacto = models.IntegerField(default=1, unique=True)
    n_vitorias = models.IntegerField(null=True, default = 0)
    saldo = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    dinheiroGasto = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)
    pagamentosRegularizados = models.BooleanField(default=False)
    posicao_preferida = models.TextField(max_length=512, null=True)
    bio = models.TextField(max_length=512, null=True)
    isgestor = models.BooleanField(default=False)
    isOnline = models.BooleanField(default=False)
    pedidoSubs = models.BooleanField(default=False)


class movimentos(models.Model):
    cc = models.ForeignKey(utilizador, on_delete=models.CASCADE)
    ano = models.IntegerField(default='', unique=False)
    pago = models.TextField(max_length=512, null=True)
    montante = models.IntegerField(null=True)


class jogador(models.Model):
    estatuto = models.TextField(
        max_length=512, null=True, default='Sem estatuto')
    iscaptain = models.BooleanField(default=False)
    utilizador_cc = models.ForeignKey(utilizador, on_delete=models.CASCADE)


class torneio(models.Model):
    nome = models.CharField(max_length=512, primary_key=True, unique=True)
    data_inicio = models.DateField(default=None)
    data_fim = models.DateField(default=None)
    dias = models.CharField(max_length=512)
    hora_inicio = models.CharField(max_length=512)
    campos = models.CharField(max_length=512)
    dia_sem_jogo = models.DateField(default=None)
    gestor_utilizador_cc = models.ForeignKey(
        utilizador, on_delete=models.CASCADE)
    n_jogos = models.IntegerField()


class equipa(models.Model):
    nome = models.CharField(
        max_length=512, primary_key=True, unique=True, default='')
    torneio_nome = models.ForeignKey(
        torneio, max_length=512, on_delete=models.CASCADE)
    isfull = models.BooleanField(default=False)
    n_jogadores = models.IntegerField(default=0)
    jogador_utilizador_cc = models.ForeignKey(
        utilizador, max_length=512, on_delete=models.CASCADE, default="")


class jogador_equipa(models.Model):
    jogador_utilizador_cc = models.ForeignKey(
        utilizador, on_delete=models.CASCADE)
    posicao = models.CharField(max_length=512)
    estatuto = models.TextField(max_length=512, default='')
    equipa_nome = models.ForeignKey(equipa, on_delete=models.CASCADE)


class jogo(models.Model):
    data_inicio = models.DateField(default=None)
    golos_equipa_a = models.IntegerField(default=None, null=True)
    golos_equipa_b = models.IntegerField(default=None, null=True)
    nome_equipa_a = models.ForeignKey(
        equipa, on_delete=models.CASCADE, related_name='equipaA', unique=False)
    nome_equipa_b = models.ForeignKey(
        equipa, on_delete=models.CASCADE, related_name='equipaB', unique=False)
    nome_torneio = models.ForeignKey(
        torneio, on_delete=models.CASCADE, unique=False)
    campo = models.CharField(max_length=512, default="", unique=False)


class notificacao(models.Model):
    nome_torneio = models.ForeignKey(torneio, on_delete=models.CASCADE)
    nome_equipa_a = models.ForeignKey(
        equipa, on_delete=models.CASCADE, related_name='EquipaA', unique=False, default="-")
    nome_equipa_b = models.ForeignKey(
        equipa, on_delete=models.CASCADE, related_name='EquipaB', unique=False, default="-")
    texto = models.CharField(max_length=512)


class reserva_torneio(models.Model):
    cc = models.ForeignKey(utilizador, on_delete=models.CASCADE)
    posicao = models.CharField(max_length=512, default='')
    pedidoSubs = models.BooleanField(default=False)
    torneio = models.ForeignKey(torneio, on_delete=models.CASCADE)


class substituicao(models.Model):
    deUser = models.ForeignKey(
        utilizador, on_delete=models.CASCADE, related_name='deUser')
    paraUser = models.ForeignKey(
        utilizador, on_delete=models.CASCADE, related_name='paraUser')
    equipaDest = models.CharField(max_length=512)
    duracao = models.IntegerField(default=0, unique=False)


class classificacao(models.Model):
    cEquipa = models.ForeignKey(equipa, on_delete=models.CASCADE)
    cTorneio = models.ForeignKey(torneio, on_delete=models.CASCADE)
    cPontos = models.IntegerField(default=0)
    cMarcados = models.IntegerField(default=0)
    cSofridos = models.IntegerField(default=0)
