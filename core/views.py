from django.shortcuts import render
from dotenv import load_dotenv
import requests
import os

load_dotenv(override=True)

API_KEY = os.getenv("API_KEY")

SITE = 'https://api.pexels.com/v1/search'

def index(request):
    imagens = []
    content = {}
    if(request.POST):
        picture = request.POST.dict()
        foto = picture.get('query')
        print(foto)
        responses = pegar_imagem(foto)
        
        for response in responses:
            imagens.append({
                "imagem": response['src']['original'],
                "fotografo": response['photographer'],
                "alt": response['alt']
            })
        content = {"images": imagens}
        print(content)
    return render(request, 'index.html',content)


def autorizacao():
    return {'Authorization': API_KEY}

def pegar_imagem(query):
    headers = autorizacao()
    params = {'query': query, 'per_page': 10}
    try:
        response = requests.get(SITE, headers=headers, params=params)
        if response.status_code == 200:
            imagens = response.json()
            return imagens['photos']
        else:
            print("Erro no response")
    except Exception as e:
        print(e)
        return []