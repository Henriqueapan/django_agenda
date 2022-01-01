from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404 as _404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages

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
    # if request.GET.get('termo') is None:
    #     raise _404()
    if not request.GET.get('termo') or request.GET.get('termo') is None:
        messages.add_message(request, messages.ERROR, 'O campo de busca não pode ficar vazio!')
        return redirect('index')

    termo = request.GET.get('termo').lower()
    campo = Concat('nome', Value(' '), 'sobrenome')

    contatos = Contato.objects.annotate(nome_completo=campo).filter(
        Q(mostrar=True) &
        (Q(nome_completo__icontains=termo) | Q(nome_completo__icontains=termo.capitalize()) |
         Q(telefone__icontains=termo)) | Q(categoria__nome__icontains=termo.capitalize())
    ).order_by('-id')

    paginator = Paginator(contatos, 15)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    for contato in contatos:
        if len(contato.descricao) > 95:
            contato.descricao = contato.descricao[:95] + '...'

    if not contatos.object_list:
        messages.add_message(request, messages.WARNING, 'Não foram encontrados contatos com os termos da busca.')
        return redirect('index')

    messages.add_message(request, messages.SUCCESS, 'Busca concluída')
    return render(request, 'contatos/index.html', {'contatos': contatos})
