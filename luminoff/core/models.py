from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    """Perfil estendido para todos os usuários do sistema"""
    TIPO_CHOICES = [
        ('PROF', 'Professor'),
        ('SEC', 'Secretário'),
        ('COORD', 'Coordenador'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    matricula = models.CharField(max_length=20, unique=True)
    departamento = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15, blank=True)
    
    class Meta:
        verbose_name = "Perfil de Usuário"
        verbose_name_plural = "Perfis de Usuários"
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_tipo_display()})"


class Semestre(models.Model):
    """Modelo para representar um semestre letivo"""
    PERIODO_CHOICES = [
        (1, '1º Semestre'),
        (2, '2º Semestre'),
    ]
    
    ano = models.IntegerField()
    semestre = models.IntegerField(choices=PERIODO_CHOICES)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    ativo = models.BooleanField(default=False)
    iniciado_em = models.DateField(null=True, blank=True)
    encerrado_em = models.DateField(null=True, blank=True)
    criada_em = models.DateField(auto_now_add=True)
    atualizada_em = models.DateField(auto_now=True)
    
    class Meta:
        unique_together = ('ano', 'semestre')
        ordering = ['-ano', '-semestre']
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
    
    def __str__(self):
        return f"{self.ano}.{self.semestre}"


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
    
    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"


class Disciplina(models.Model):
    """Disciplinas ofertadas"""
    codigo = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=200)
    carga_horaria = models.IntegerField(help_text="Carga horária total")
    ativa = models.BooleanField(default=True)
    criada_em = models.DateField(auto_now_add=True)
    atualizada_em = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"


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
    professor = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, 
                                   related_name='horarios', 
                                   limit_choices_to={'tipo': 'PROF'})
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIA_SEMANA)
    hora_inicio = models.TimeField()  # ← CORRIGIDO: era DateTimeField
    hora_fim = models.TimeField()     # ← CORRIGIDO: era DateTimeField
    numero_alunos = models.IntegerField(default=0, help_text="Número de alunos matriculados")
    ativo = models.BooleanField(default=True)
    desligamento_excepcional = models.DateField(null=True, blank=True)  # ← CORRIGIDO: removido default=False
    criada_em = models.DateField(auto_now_add=True)
    atualizada_em = models.DateField(auto_now=True)
    
    class Meta:
        verbose_name = "Horário de Aula"
        verbose_name_plural = "Horários de Aula"
        ordering = ['semestre', 'dia_semana', 'hora_inicio']
        unique_together = ['semestre', 'sala', 'dia_semana', 'hora_inicio']
    
    def __str__(self):
        return f"{self.disciplina.codigo} - {self.sala.nome} - {self.get_dia_semana_display()}"