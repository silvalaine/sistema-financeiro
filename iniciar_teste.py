#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simples para iniciar o servidor e ver erros
"""

print("Iniciando servidor...")
print("=" * 60)

try:
    # Importar o app
    import app
    
    print("[OK] App importado com sucesso")
    print(f"[OK] {len(list(app.app.url_map.iter_rules()))} rotas carregadas")
    print()
    print("Iniciando servidor Flask...")
    print("Acesse: http://localhost:5000")
    print("Pressione CTRL+C para parar")
    print("=" * 60)
    print()
    
    # Iniciar o servidor
    app.app.run(debug=True, host='0.0.0.0', port=5000)
    
except KeyboardInterrupt:
    print("\n\nServidor parado pelo usuario")
except Exception as e:
    print(f"\n[ERRO] Erro ao iniciar servidor: {e}")
    import traceback
    traceback.print_exc()
    input("\nPressione ENTER para sair...")

