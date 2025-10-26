from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    Semestre, PerfilUsuario, Sala, Disciplina, HorarioAula
)


# Inline para mostrar PerfilUsuario junto com User
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfil do Usuário'
    fields = ['tipo', 'matricula', 'departamento', 'telefone']


# Extende o UserAdmin para incluir PerfilUsuario
class UserAdmin(BaseUserAdmin):
    inlines = [PerfilUsuarioInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_tipo', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'perfil__tipo']
    
    def get_tipo(self, obj):
        try:
            return obj.perfilusuario.get_tipo_display()
        except PerfilUsuario.DoesNotExist:
            return '-'
    get_tipo.short_description = 'Tipo'


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
    list_filter = ['tipo', 'ativa']
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
    list_filter = ['ativa']
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


@admin.register(HorarioAula)
class HorarioAulaAdmin(admin.ModelAdmin):
    list_display = [
        'get_disciplina_codigo', 
        'disciplina', 
        'sala', 
        'get_dia_semana', 
        'hora_inicio', 
        'hora_fim',
        'numero_alunos',
        'ativo'
    ]
    list_filter = [
        'semestre', 
        'dia_semana', 
        'ativo', 
        'sala__tipo',
        'disciplina'
    ]
    search_fields = [
        'disciplina__codigo', 
        'disciplina__nome', 
        'sala__nome'
    ]
    ordering = ['semestre', 'dia_semana', 'hora_inicio']
    
    fieldsets = (
        ('Período', {
            'fields': ('semestre', 'ativo')
        }),
        ('Alocação', {
            'fields': ('sala', 'disciplina', 'dia_semana')
        }),
        ('Horário', {
            'fields': ('hora_inicio', 'hora_fim')
        }),
        ('Informações Adicionais', {
            'fields': ('numero_alunos', 'desligamento_excepcional')
        }),
        ('Metadados', {
            'fields': ('criada_em', 'atualizada_em'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['criada_em', 'atualizada_em']
    
    # Filtros horizontais para melhor UX
    autocomplete_fields = ['disciplina', 'sala']
    
    def get_disciplina_codigo(self, obj):
        return obj.disciplina.codigo
    get_disciplina_codigo.short_description = 'Código'
    get_disciplina_codigo.admin_order_field = 'disciplina__codigo'
    
    def get_dia_semana(self, obj):
        return obj.get_dia_semana_display()
    get_dia_semana.short_description = 'Dia'
    get_dia_semana.admin_order_field = 'dia_semana'
    
    # Validação para evitar conflitos de horário
    def save_model(self, request, obj, form, change):
        # Verifica conflitos na mesma sala
        conflitos = HorarioAula.objects.filter(
            semestre=obj.semestre,
            sala=obj.sala,
            dia_semana=obj.dia_semana,
            ativo=True
        ).exclude(pk=obj.pk)
        
        for horario in conflitos:
            # Verifica sobreposição de horários
            if (obj.hora_inicio < horario.hora_fim and 
                obj.hora_fim > horario.hora_inicio):
                from django.contrib import messages
                messages.error(
                    request, 
                    f'Conflito de horário! A sala {obj.sala} já está ocupada '
                    f'com {horario.disciplina} no mesmo horário.'
                )
                return
        
        super().save_model(request, obj, form, change)


# Customização do site admin
admin.site.site_header = 'Luminoff - Gestão de Energia'
admin.site.site_title = 'Luminoff Admin'
admin.site.index_title = 'Painel de Controle'