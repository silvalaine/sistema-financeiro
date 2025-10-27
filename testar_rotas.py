#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se todas as rotas estão funcionando
"""

import requests
import time

def testar_rotas():
    base_url = "http://localhost:5000"
    
    rotas = [
        "/",
        "/receitas", 
        "/despesas",
        "/relatorios",
        "/categorias"
    ]
    
    print("Testando rotas do sistema financeiro...")
    print("=" * 50)
    
    for rota in rotas:
        try:
            response = requests.get(f"{base_url}{rota}", timeout=5)
            if response.status_code == 200:
                print(f"OK {rota} - Status 200")
            else:
                print(f"ERRO {rota} - Status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"ERRO {rota} - Conexao: {e}")
    
    print("=" * 50)
    print("Teste concluido!")

if __name__ == "__main__":
    # Aguardar um pouco para a aplicação inicializar
    print("Aguardando aplicacao inicializar...")
    time.sleep(3)
    testar_rotas()
