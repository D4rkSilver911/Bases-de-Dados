# BD
projeto em html, css, e sql relacionado com base de dados

Para ligar à Base de dados:
1. Criar uma nova base de dados no pgAdmin4
2. Abrir o ficheiro: projeto_bd\settings.py
3. Ir à linha 78, onde diz DATABASES
4. Alterar os valores:
	NAME igual ao nome da sua nova base de dados
	USER e PASSWORD de acordo com os utilizados no pgAdmin4


Para correr a aplicação:
1. Abrir o CMD na pasta deste file README
2. Correr no cmd "py manage.py makemigrations"
3. Correr no cmd "py manage.py migrate"
4. Correr no cmd "py manage.py runserver"
5. No browser ir ao link "127.0.0.1:8000"
