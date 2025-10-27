from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .models import Semestre

## por enquanto, essas views não estão sendo usadas
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Redireciona para a página após o login (pode ser alterado conforme necessário)
            next_url = request.GET.get('next', 'core:criar_semestre')
            return redirect(next_url)
        else:
            messages.error(request, 'Matrícula/usuário ou senha inválidos.')
    
    return render(request, 'core/login.html')

@login_required
def criar_semestre(request):
    if request.method == 'POST':
        try:
            # The Semestre model in `core.models` uses the field name `semestre` (not `periodo`),
            # and uses `iniciado_em` / `encerrado_em` for start/end dates. Map form fields to model fields.
            semestre = Semestre(
                ano=int(request.POST['ano']),
                semestre=int(request.POST['periodo']),
                iniciado_em=request.POST.get('data_inicio') or None,
                encerrado_em=request.POST.get('data_fim') or None,
            )
            semestre.save()
            messages.success(request, 'Semestre criado com sucesso!')
            # core.urls defines an app_name='core', so use the namespaced name when reversing
            return redirect('core:criar_semestre')
        except Exception as e:
            messages.error(request, f'Erro ao criar semestre: {str(e)}')
    
    return render(request, 'core/criar_semestre.html')
