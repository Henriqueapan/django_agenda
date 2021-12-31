from django.shortcuts import render, get_object_or_404
from django.http import Http404 as _404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat

def index(request):
    contatos = Contato.objects.order_by('-id').filter(mostrar=True)
    paginator = Paginator(contatos, 15)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    for contato in contatos:
        if len(contato.descricao) > 95:
            contato.descricao = contato.descricao[:95] + '...'

    return render(request, 'contatos/index.html', {'contatos': contatos})

def ver_contato(request, contato_id):
    # contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise _404('Página não encontrada')

    return render(request, 'contatos/ver_contato.html', {'contato': contato})
    # except Contato.DoesNotExist as e:
    #     raise Http404(f'{e}')

def busca(request):
    if request.GET.get('termo') is None:
        raise _404()

    termo = request.GET.get('termo').lower()
    campo = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(nome_completo=campo).filter(
        Q(mostrar=True) &
        (Q(nome_completo__icontains=termo) | Q(nome_completo__icontains=termo.capitalize()) |
         Q(telefone__icontains=termo))
    ).order_by('-id')

    paginator = Paginator(contatos, 15)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    for contato in contatos:
        if len(contato.descricao) > 95:
            contato.descricao = contato.descricao[:95] + '...'

    return render(request, 'contatos/index.html', {'contatos': contatos})
