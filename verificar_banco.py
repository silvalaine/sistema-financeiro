#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar o banco de dados
"""

from app import app, db, Despesa, Receita, CategoriaDespesa, SubcategoriaDespesa

def verificar_banco():
    with app.app_context():
        try:
            print("Verificando banco de dados...")
            
            # Verificar se as tabelas existem
            print("Tabelas:")
            print("- Receitas:", Receita.query.count())
            print("- Despesas:", Despesa.query.count())
            print("- Categorias:", CategoriaDespesa.query.count())
            print("- Subcategorias:", SubcategoriaDespesa.query.count())
            
            # Tentar buscar uma despesa
            despesas = Despesa.query.limit(1).all()
            if despesas:
                despesa = despesas[0]
                print(f"Primeira despesa: {despesa.descricao}")
                print(f"Categoria: {despesa.categoria}")
                print(f"Subcategoria: {despesa.subcategoria}")
            
            print("Banco de dados OK!")
            
        except Exception as e:
            print(f"Erro no banco: {e}")

if __name__ == "__main__":
    verificar_banco()
