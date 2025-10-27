#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar e recriar o banco de dados
"""

import os
from app import app, db, Despesa, Receita, CategoriaDespesa, SubcategoriaDespesa, TipoPagamento

def limpar_e_recriar_banco():
    with app.app_context():
        try:
            # Deletar arquivo do banco se existir
            db_path = 'sistema_financeiro.db'
            if os.path.exists(db_path):
                os.remove(db_path)
                print("Banco antigo removido.")
            
            # Criar todas as tabelas
            db.create_all()
            print("Banco de dados criado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao criar banco: {e}")

if __name__ == "__main__":
    limpar_e_recriar_banco()
