from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    HorarioTurma, Professor, Semestre, Professor, Sala, Disciplina, Turma
)


# Inline para mostrar Professor junto com User
class ProfessorInline(admin.StackedInline):
    model = Professor
    can_delete = False
    verbose_name = 'Professor'
    verbose_name_plural = 'Professores'
    fields = ['matricula', 'departamento', 'telefone']


# Extende o UserAdmin para incluir PerfilUsuario
'''class UserAdmin(BaseUserAdmin):
    inlines = [PerfilUsuarioInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_tipo', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'perfil__tipo']'''

# Customiza o Admin do Professor
@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['get_nome_completo', 'matricula', 'departamento', 'telefone', 'get_email']
    search_fields = ['user__first_name', 'user__last_name', 'matricula', 'departamento']
    ordering = ['user__first_name', 'user__last_name']
    
    def get_nome_completo(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_nome_completo.short_description = 'Nome'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

# Customiza o Admin do User para incluir o Professor inline
class UserAdmin(BaseUserAdmin):
    inlines = [ProfessorInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    
# Re-registra o User com o novo admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'ano', 'get_periodo', 'data_inicio', 'data_fim', 'ativo', 'criada_em']
    list_filter = ['ativo', 'ano', 'semestre']
    search_fields = ['ano']
    ordering = ['-ano', '-semestre']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('ano', 'semestre', 'ativo')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_fim', 'iniciado_em', 'encerrado_em')
        }),
    )
    
    readonly_fields = ['criada_em', 'atualizada_em']
    
    def get_periodo(self, obj):
        return obj.get_semestre_display()
    get_periodo.short_description = 'Período'
    
    # Validação personalizada
    def save_model(self, request, obj, form, change):
        # Garante que apenas 1 semestre esteja ativo
        if obj.ativo:
            Semestre.objects.filter(ativo=True).exclude(pk=obj.pk).update(ativo=False)
        super().save_model(request, obj, form, change)


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'get_tipo_display', 'capacidade', 'localizacao', 'ativa']
    list_filter = [
        'ativa',           # Ativa/Inativa
        'tipo',            # Tipo de sala (Lab, Sala de Aula, etc)
        'criada_em',       # Filtro por data de criação
    ]
    search_fields = ['nome', 'localizacao']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações da Sala', {
            'fields': ('nome', 'tipo', 'capacidade', 'localizacao', 'ativa')
        }),
        ('Metadados', {
            'fields': ('criada_em', 'atualizada_em'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['criada_em', 'atualizada_em']
    
    def get_tipo_display(self, obj):
        return obj.get_tipo_display()
    get_tipo_display.short_description = 'Tipo (legível)'


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'carga_horaria', 'ativa', 'criada_em']
    list_filter = [
        'ativa',           # Ativa/Inativa
        'carga_horaria',   # Filtro por carga horária
        'criada_em',       # Filtro por data
    ]
    search_fields = ['codigo', 'nome']
    ordering = ['codigo']
    
    fieldsets = (
        ('Informações da Disciplina', {
            'fields': ('codigo', 'nome', 'carga_horaria', 'ativa')
        }),
        ('Metadados', {
            'fields': ('criada_em', 'atualizada_em'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['criada_em', 'atualizada_em']


class HorarioTurmaInline(admin.TabularInline):
    model = HorarioTurma
    extra = 2
    fields = ['sala', 'dia_semana', 'hora_inicio', 'hora_fim']


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'disciplina', 'professor', 'semestre', 'numero_alunos', 'ativo']
    list_filter = ['semestre', 'disciplina', 'professor', 'ativo']
    search_fields = ['disciplina__codigo', 'disciplina__nome', 'codigo_turma']
    inlines = [HorarioTurmaInline]  # ← Edita horários inline!
    
    fieldsets = (
        ('Informações da Turma', {
            'fields': ('semestre', 'disciplina', 'professor', 'codigo_turma', 'numero_alunos', 'ativo')
        }),
    )


@admin.register(HorarioTurma)
class HorarioTurmaAdmin(admin.ModelAdmin):
    list_display = ['turma', 'sala', 'get_dia_semana', 'hora_inicio', 'hora_fim']
    list_filter = ['turma__semestre', 'dia_semana', 'sala']
    search_fields = ['turma__disciplina__codigo', 'turma__disciplina__nome']
    
    def get_dia_semana(self, obj):
        return obj.get_dia_semana_display()
    get_dia_semana.short_description = 'Dia'


# Customização do site admin
admin.site.site_header = 'Luminoff - Gestão de Energia'
admin.site.site_title = 'Luminoff Admin'
admin.site.index_title = 'Painel de Controle'