#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicializar o banco de dados
"""

from app import app, db, Despesa, Receita, CategoriaDespesa, SubcategoriaDespesa, TipoPagamento

def inicializar_banco():
    with app.app_context():
        try:
            print("Criando banco de dados...")
            
            # Criar todas as tabelas
            db.create_all()
            
            # Adicionar tipos de pagamento padrão
            if TipoPagamento.query.count() == 0:
                tipos_pagamento_padrao = [
                    TipoPagamento(nome="Dinheiro", descricao="Pagamento em espécie"),
                    TipoPagamento(nome="Cartão de Crédito", descricao="Pagamento com cartão de crédito"),
                    TipoPagamento(nome="Cartão de Débito", descricao="Pagamento com cartão de débito"),
                    TipoPagamento(nome="PIX", descricao="Transferência via PIX"),
                    TipoPagamento(nome="Transferência Bancária", descricao="Transferência entre contas"),
                    TipoPagamento(nome="Boleto", descricao="Pagamento via boleto bancário")
                ]
                
                for tipo in tipos_pagamento_padrao:
                    db.session.add(tipo)
                
                db.session.commit()
                print("Tipos de pagamento padrão adicionados:", len(tipos_pagamento_padrao))
            
            # Verificar se já existem categorias
            if CategoriaDespesa.query.count() == 0:
                # Adicionar algumas categorias de exemplo
                categorias_exemplo = [
                    CategoriaDespesa(nome="Alimentação", descricao="Gastos com comida"),
                    CategoriaDespesa(nome="Transporte", descricao="Gastos com transporte"),
                    CategoriaDespesa(nome="Moradia", descricao="Gastos com casa"),
                    CategoriaDespesa(nome="Saúde", descricao="Gastos com saúde"),
                    CategoriaDespesa(nome="Educação", descricao="Gastos com educação"),
                    CategoriaDespesa(nome="Lazer", descricao="Gastos com lazer"),
                    CategoriaDespesa(nome="Roupas", descricao="Gastos com roupas"),
                    CategoriaDespesa(nome="Outros", descricao="Outros gastos")
                ]
                
                for categoria in categorias_exemplo:
                    db.session.add(categoria)
                
                db.session.commit()
                print("Categorias de exemplo adicionadas:", len(categorias_exemplo))
            else:
                print("Categorias já existem no banco.")
            
            print("Banco de dados criado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao criar banco: {e}")

if __name__ == "__main__":
    inicializar_banco()
