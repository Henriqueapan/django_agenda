# django_agenda
Projeto de agenda de contatos feito com base no framework Django, e utilizando Bootstrap para os templates.
# Rodando o projeto
 - Clone o repositório usando git clone https://github.com/Henriqueapan/django_agenda.git
 - Instale o Python (certifique-se de instalar o pip também), e, em seguida, instale o Django (pip install django)
 - Instale o Pillow para que o Django consiga manipular as Imagens dos contatos (sem isso, o projeto não vai rodar)
 - A partir do diretório Agenda, execute "python manage.py runserver" e, em seguida e clique no link exibido no terminal
# Banco de dados pré populado e superuser
O banco de dados no repositório foi populado para um superuser pré-existente através de um script python para que, caso o usuário não queira adicionar seus próprios contatos, ele possa pegar uma agenda feita.
Para logar com o superuser, basta acessar a página de login no site e usar "admin" tanto como usuário quanto como senha.
Em seguida, basta voltar para a página inicial (agenda) clicando no ícona no canto esquerdo da barra de navegação ou através do link no menu em cascata no lado direito da barra de navegação.
 
