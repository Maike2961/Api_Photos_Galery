from django.shortcuts import render, redirect
from django.core.files import File
from django.http import HttpResponse
from dotenv import load_dotenv
import requests
import os

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")


SITE = 'https://api.pexels.com/v1/search'
DETALHE_SITE = 'https://api.pexels.com/v1'

def index(request):
    imagens = request.session.get('imagens', [])
    content = {"images": imagens}
    
    if(request.POST):
        print(os.path.abspath(__file__))
        picture = request.POST.dict()
        foto = picture.get('query')
        responses = pegar_imagem(foto)  
        imagens = []   
        for response in responses:
            imagens.append({
                "id": response['id'],
                "imagem": response['src']['original'],
                "alt": response['alt'],
                "query": foto
            })
        content = {
            "images": imagens,
            }
        request.session['imagens'] = imagens
        sessions = list(request.session.keys())
        print(sessions)
    return render(request, 'core/index.html',content)
    
def limpar(request):
    sessions = list(request.session.keys())
    for session in sessions:
        del request.session[session]
    return redirect("index")

def autorizacao():
    return {'Authorization': API_KEY}

def pegar_detalhes(request, foto, id):
    header = autorizacao()
    try:
        response = requests.get(f"{DETALHE_SITE}/photos/{id}", headers=header)
        if response.status_code == 200:
            imagem = response.json()
            content = {
                'imagem': imagem['src']['medium'],
                'busca': foto,
                'fotografo': imagem['photographer'],
                'perfil': imagem['photographer_url'],
                'alt': imagem['alt'],
                'button': ''
            }
            return render(request, "core/detalhes.html", content)
        else:
            print("erro no response")
        return render(request, "core/detalhes.html")        
    except Exception as e:
        print(e)
    return render(request, "core/detalhes.html")

def pegar_imagem(query):
    headers = autorizacao()
    params = {'query': query, 'per_page': 12}
    try:
        response = requests.get(SITE, headers=headers, params=params)
        print(response.url)
        if response.status_code == 200:
            imagens = response.json()
            print(imagens)
            return imagens['photos']
        else:
            print("Erro no response")
    except Exception as e:
        print(e)
        return []
