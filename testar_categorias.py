#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar se as categorias estão aparecendo na página de despesas
"""

import requests
from bs4 import BeautifulSoup

def testar_categorias_despesas():
    try:
        print("Testando categorias na página de despesas...")
        
        # Fazer requisição para a página de despesas
        response = requests.get("http://localhost:5000/despesas", timeout=5)
        
        if response.status_code == 200:
            # Parsear o HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Encontrar o select de categorias
            select_categoria = soup.find('select', {'id': 'categoriaDespesa'})
            
            if select_categoria:
                # Encontrar todas as opções
                opcoes = select_categoria.find_all('option')
                
                print(f"Total de opções encontradas: {len(opcoes)}")
                print("Categorias disponíveis:")
                
                for opcao in opcoes:
                    valor = opcao.get('value', '')
                    texto = opcao.get_text(strip=True)
                    if valor:  # Pular a opção vazia
                        print(f"  - {texto}")
                
                if len(opcoes) > 1:  # Mais que apenas a opção vazia
                    print("OK - Categorias estao aparecendo corretamente!")
                else:
                    print("ERRO - Nenhuma categoria encontrada!")
            else:
                print("ERRO - Select de categorias nao encontrado!")
        else:
            print(f"ERRO ao acessar pagina: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    testar_categorias_despesas()
