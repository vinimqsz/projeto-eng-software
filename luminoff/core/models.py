from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PerfilUsuario(models.Model):
    TIPO_CHOICES = [
        ('PROF', 'Professor'),
        ('SEC', 'Secretário'),
        ('COORD', 'Coordenador'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    matricula = models.CharField(max_length=20, unique=True)
    departamento = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, blank=True)

class Semestre(models.Model):
    """Modelo para representar um semestre letivo"""
    ano = models.IntegerField()
    semestre = models.IntegerField(choices=[(1, '1º Semestre'), (2, '2º Semestre')])
    ativo = models.BooleanField(default=False)
    iniciado_em = models.DateField(null=True, blank=True)
    encerrado_em = models.DateField(null=True, blank=True)  
    criada_em = models.DateField(auto_now_add=True)
    atualizada_em = models.DateField(auto_now=True) 
    class Meta:
        unique_together = ('ano', 'semestre')
        ordering = ['-ano', '-semestre']    

class TipoSala(models.TextChoices):
    """Tipos de sala disponíveis"""
    LABORATORIO = 'LAB', 'Laboratório'
    SALA_AULA = 'SAL', 'Sala de Aula'
    AUDITORIO = 'AUD', 'Auditório'
    OUTROS = 'OUT', 'Outros'

class Sala(models.Model):
    """Modelo para cadastro de salas (RF001)"""
    nome = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=3, choices=TipoSala.choices)
    capacidade = models.IntegerField(help_text="Número máximo de alunos")
    localizacao = models.CharField(max_length=200, help_text="Prédio/Andar/Número")
    ativa = models.BooleanField(default=True)
    criada_em = models.DateField(auto_now_add=True)
    atualizada_em = models.DateField(auto_now=True)

class Disciplina(models.Model):
    """Disciplinas ofertadas"""
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=200)
    carga_horaria = models.IntegerField(help_text="Carga horária total")
    ativa = models.BooleanField(default=True)
    criada_em = models.DateField(auto_now_add=True)
    atualizada_em = models.DateField(auto_now=True)

class HorarioAula(models.Model):
    """Gerenciamento de horários de aula (RF002)"""
    DIA_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name='horarios')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='horarios')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIA_SEMANA)
    hora_inicio = models.DateTimeField()
    hora_fim = models.DateTimeField()
    numero_alunos = models.IntegerField(default=0, help_text="Número de alunos matriculados")
    ativo = models.BooleanField(default=True)
    desligamento_excepcional = models.DateField(null=True, blank=True, default=False)
    criada_em = models.DateField(auto_now_add=True)
    atualizada_em = models.DateField(auto_now=True)