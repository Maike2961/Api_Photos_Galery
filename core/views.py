from django.shortcuts import render
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
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
    return render(request, 'core/index.html',content)
    

def autorizacao():
    return {'Authorization': API_KEY}

def pegar_detalhes(request, foto, id):
    header = autorizacao()
    try:
        response = requests.get(f"{DETALHE_SITE}/photos/{id}", headers=header)
        print(response.url)
        print(response.status_code)
        if response.status_code == 200:
            imagem = response.json()
            content = {
                'imagem': imagem['src']['medium'],
                'busca': foto,
                'fotografo': imagem['photographer'],
                'perfil': imagem['photographer_url'],
                'alt': imagem['alt']
            }
            print(content)
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
