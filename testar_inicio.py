#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar se o servidor inicia corretamente
"""

import sys
import traceback

print("=" * 60)
print("TESTANDO INICIO DO SERVIDOR")
print("=" * 60)
print()

try:
    print("1. Importando app...")
    import app
    print("   [OK] App importado")
    print()
    
    print("2. Verificando se app Flask foi criado...")
    if hasattr(app, 'app'):
        print("   [OK] Flask app existe")
    else:
        print("   [ERRO] Flask app nao encontrado")
        sys.exit(1)
    print()
    
    print("3. Verificando rotas...")
    rotas = []
    for rule in app.app.url_map.iter_rules():
        rotas.append(str(rule))
    print(f"   [OK] {len(rotas)} rotas encontradas")
    print()
    
    print("4. Testando se o servidor pode iniciar...")
    print("   (Isso vai tentar iniciar o servidor por 2 segundos)")
    print()
    
    # Tentar iniciar o servidor em modo de teste
    import threading
    import time
    import requests
    
    def iniciar_servidor():
        try:
            app.app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
        except Exception as e:
            print(f"   [ERRO] Erro ao iniciar servidor: {e}")
    
    # Iniciar servidor em thread separada
    server_thread = threading.Thread(target=iniciar_servidor, daemon=True)
    server_thread.start()
    
    # Aguardar servidor iniciar
    print("   Aguardando servidor iniciar...")
    time.sleep(3)
    
    # Tentar fazer uma requisição
    try:
        response = requests.get('http://127.0.0.1:5000/', timeout=2)
        if response.status_code == 200:
            print("   [OK] Servidor esta respondendo!")
            print(f"   Status: {response.status_code}")
        else:
            print(f"   [AVISO] Servidor respondeu com status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   [ERRO] Nao foi possivel conectar ao servidor")
        print("   O servidor pode nao ter iniciado corretamente")
    except Exception as e:
        print(f"   [ERRO] Erro ao testar servidor: {e}")
    
    print()
    print("=" * 60)
    print("TESTE CONCLUIDO")
    print("=" * 60)
    print()
    print("Se o servidor nao iniciou, verifique:")
    print("1. Se a porta 5000 esta disponivel")
    print("2. Se ha erros no console")
    print("3. Execute: python app.py")
    print()
    
except ImportError as e:
    print(f"[ERRO] Erro de importacao: {e}")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"[ERRO] Erro inesperado: {e}")
    traceback.print_exc()
    sys.exit(1)

