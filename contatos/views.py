from django.shortcuts import render, get_object_or_404
from .models import Contato
from django.core.paginator import Paginator

def index(request):
    contatos = Contato.objects.all()
    paginator = Paginator(contatos, 15)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    for contato in contatos:
        if len(contato.descricao) > 95:
            contato.descricao = contato.descricao[:95] + '...'

    return render(request, 'contatos/index.html', {'contatos' : contatos})

def ver_contato(request, contato_id):
    # contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)
    return render(request, 'contatos/ver_contato.html', {'contato' : contato})
    # except Contato.DoesNotExist as e:
    #     raise Http404(f'{e}')
