#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar problemas com o sistema
"""

import sys
import os

def verificar_importacoes():
    """Verifica se todas as dependências estão instaladas"""
    print("=" * 60)
    print("1. VERIFICANDO DEPENDÊNCIAS")
    print("=" * 60)
    
    dependencias = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'sqlalchemy': 'SQLAlchemy',
        'dateutil': 'python-dateutil',
        'reportlab': 'ReportLab'
    }
    
    faltando = []
    for modulo, nome in dependencias.items():
        try:
            __import__(modulo)
            print(f"[OK] {nome}")
        except ImportError:
            print(f"[ERRO] {nome} - FALTANDO")
            faltando.append(nome)
    
    if faltando:
        print(f"\n[AVISO] Instale as dependencias faltantes:")
        print(f"pip install {' '.join(faltando)}")
        return False
    return True

def verificar_arquivos():
    """Verifica se os arquivos necessários existem"""
    print("\n" + "=" * 60)
    print("2. VERIFICANDO ARQUIVOS")
    print("=" * 60)
    
    arquivos_necessarios = [
        'app.py',
        'models.py',
        'pdf_generator.py',
        'requirements.txt'
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"[OK] {arquivo}")
        else:
            print(f"[ERRO] {arquivo} - NAO ENCONTRADO")
            todos_ok = False
    
    # Verificar templates
    print("\nVerificando templates:")
    templates = ['index.html', 'receitas.html', 'despesas.html', 'relatorios.html', 
                 'categorias.html', 'tipos_pagamento.html', 'base.html']
    for template in templates:
        caminho = os.path.join('templates', template)
        if os.path.exists(caminho):
            print(f"[OK] templates/{template}")
        else:
            print(f"[ERRO] templates/{template} - NAO ENCONTRADO")
            todos_ok = False
    
    return todos_ok

def verificar_sintaxe():
    """Verifica se há erros de sintaxe no app.py"""
    print("\n" + "=" * 60)
    print("3. VERIFICANDO SINTAXE DO CÓDIGO")
    print("=" * 60)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            codigo = f.read()
        compile(codigo, 'app.py', 'exec')
        print("[OK] app.py - Sem erros de sintaxe")
        return True
    except SyntaxError as e:
        print(f"[ERRO] app.py - Erro de sintaxe na linha {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"[ERRO] Erro ao verificar app.py: {e}")
        return False

def verificar_importacoes_app():
    """Tenta importar o app para verificar erros"""
    print("\n" + "=" * 60)
    print("4. VERIFICANDO IMPORTAÇÕES DO APP")
    print("=" * 60)
    
    try:
        # Adicionar o diretório atual ao path
        sys.path.insert(0, os.getcwd())
        
        # Tentar importar módulos
        print("Tentando importar models...")
        from models import db, Receita, Despesa
        print("[OK] models.py")
        
        print("Tentando importar pdf_generator...")
        from pdf_generator import generate_pdf_report
        print("[OK] pdf_generator.py")
        
        print("Tentando importar app...")
        import app
        print("[OK] app.py - Importado com sucesso")
        
        return True
    except ImportError as e:
        print(f"[ERRO] Erro de importacao: {e}")
        return False
    except Exception as e:
        print(f"[ERRO] Erro: {e}")
        return False

def verificar_porta():
    """Verifica se a porta 5000 está disponível"""
    print("\n" + "=" * 60)
    print("5. VERIFICANDO PORTA 5000")
    print("=" * 60)
    
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        resultado = sock.connect_ex(('localhost', 5000))
        sock.close()
        
        if resultado == 0:
            print("[AVISO] Porta 5000 esta EM USO")
            print("  -> Outro processo pode estar usando a porta")
            print("  -> Ou o servidor ja esta rodando")
            print("  -> Solucao: Feche outros processos ou altere a porta no app.py")
            return False
        else:
            print("[OK] Porta 5000 esta DISPONIVEL")
            return True
    except Exception as e:
        print(f"[ERRO] Erro ao verificar porta: {e}")
        return True  # Assumir que está OK se não conseguir verificar

def main():
    print("\n" + "=" * 60)
    print("DIAGNÓSTICO DO SISTEMA FINANCEIRO")
    print("=" * 60 + "\n")
    
    resultados = []
    
    resultados.append(("Dependências", verificar_importacoes()))
    resultados.append(("Arquivos", verificar_arquivos()))
    resultados.append(("Sintaxe", verificar_sintaxe()))
    resultados.append(("Importações", verificar_importacoes_app()))
    resultados.append(("Porta", verificar_porta()))
    
    print("\n" + "=" * 60)
    print("RESUMO")
    print("=" * 60)
    
    todos_ok = True
    for nome, resultado in resultados:
        status = "[OK]" if resultado else "[ERRO]"
        print(f"{nome}: {status}")
        if not resultado:
            todos_ok = False
    
    print("\n" + "=" * 60)
    if todos_ok:
        print("[OK] TUDO OK! Voce pode iniciar o servidor com:")
        print("  python app.py")
        print("\nDepois acesse: http://localhost:5000")
    else:
        print("[AVISO] HA PROBLEMAS! Corrija os erros acima antes de iniciar.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()

