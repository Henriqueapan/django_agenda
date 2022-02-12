from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404 as _404
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):

    user = request.user

    contatos = Contato.objects.order_by('-id_by_user').filter(Q(user=user.id) & Q(mostrar=True))
    paginator = Paginator(contatos, 15)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    page_diff_lower = 1 - (contatos.number - 2)
    page_diff_upper = (contatos.number + 2) - (contatos.paginator.num_pages)
    up_range = (page_diff_lower + 2) if page_diff_lower > 0 else 2 if page_diff_upper <= 0 else 2 - page_diff_upper
    low_range = (page_diff_upper + 2) if page_diff_upper > 0 else 2 if page_diff_lower <= 0 else 2 - page_diff_lower
    print(str(up_range) + ' ' + str(low_range))
    cond_list = []
    for pagina in contatos.paginator.page_range:
        cond_list.append((abs(pagina - contatos.number) <= up_range and abs(pagina - contatos.number) > 0) or ((abs(pagina - contatos.number) <= low_range) and abs(pagina - contatos.number) < 14))

    print(cond_list)

    cond_list = list(enumerate(cond_list))

    for contato in contatos:
        if len(contato.descricao) > 95:
            contato.descricao = contato.descricao[:95] + '...'

    return render(request, 'contatos/index.html', {'contatos': contatos, 'lista': cond_list})

@login_required(redirect_field_name='login')
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
        Q(mostrar=True) & Q(user=request.user.id) &
        (Q(nome_completo__icontains=termo) | Q(nome_completo__icontains=termo.capitalize()) |
         Q(telefone__icontains=termo)) | Q(categoria__nome__icontains=termo.capitalize())
    ).order_by('-id')

    paginator = Paginator(contatos, 15)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    page_diff_lower = 1 - (contatos.number - 2)
    page_diff_upper = (contatos.number + 2) - (contatos.paginator.num_pages)
    up_range = (page_diff_lower + 2) if page_diff_lower > 0 else 2 if page_diff_upper <= 0 else 2 - page_diff_upper
    low_range = (page_diff_upper + 2) if page_diff_upper > 0 else 2 if page_diff_lower <= 0 else 2 - page_diff_lower
    print(str(up_range) + ' ' + str(low_range))
    cond_list = []
    for pagina in contatos.paginator.page_range:
        cond_list.append((abs(pagina - contatos.number) <= up_range and abs(pagina - contatos.number) > 0) or (
                    (abs(pagina - contatos.number) <= low_range) and abs(pagina - contatos.number) < 14))

    print(cond_list)

    cond_list = list(enumerate(cond_list))

    for contato in contatos:
        if len(contato.descricao) > 95:
            contato.descricao = contato.descricao[:95] + '...'

    if not contatos.object_list:
        messages.add_message(request, messages.WARNING, 'Não foram encontrados contatos com os termos da busca.')
        return redirect('index')

    messages.add_message(request, messages.SUCCESS, 'Busca concluída')
    return render(request, 'contatos/busca.html', {'contatos': contatos, 'lista': cond_list})

def deletar_contato(request, contato_id):
    contato = Contato.objects.get(id=contato_id)
    nome = contato.nome
    sobrenome = contato.sobrenome
    if not sobrenome:
        sobrenome = ''
    contato.delete()

    cont_user = Contato.objects.filter(user=request.user.id)
    count_cont = len(cont_user)
    counter = 0

    for contatos in Contato.objects.order_by("-id").filter(user=request.user.id):
        contatos.id_by_user = (count_cont - counter)
        counter = (counter + 1)
        contatos.save()

    messages.warning(request, f"Contato {nome} {sobrenome} deletado com sucesso!");

    return redirect('index')

