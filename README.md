# luminoff
Este projeto propõe um sistema inteligente para otimizar o consumo de energia na UFRPE. A solução integra software e hardware para automatizar o controle de luzes e ar-condicionados nos prédios, com base nos horários de aula cadastrados pelos professores. Dessa forma, os equipamentos são desligados automaticamente fora do período de uso, reduzindo o desperdício de energia, os custos operacionais e a necessidade de desligamento manual pela equipe de manutenção.

### instalação
+ pip install requirements.txt
+ python3 manage.py migrate (criar banco)
+ python3 manage.py createsuperuser (criar admin)

### parar rodar o projeto
+ python3 manage.py runserver
+ acessar localhost:8000/admin
