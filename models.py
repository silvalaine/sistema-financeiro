from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(100))

class CategoriaDespesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    subcategorias = db.relationship('SubcategoriaDespesa', backref='categoria', lazy=True)

class SubcategoriaDespesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria_despesa.id'), nullable=False)

class TipoPagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    despesas = db.relationship('Despesa', backref='tipo_pagamento', lazy=True)

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(100))
    subcategoria = db.Column(db.String(100))
    parcelas = db.Column(db.Integer, default=1)
    parcela_atual = db.Column(db.Integer, default=1)
    compra_parcelada_id = db.Column(db.Integer, nullable=True)
    tipo_pagamento_id = db.Column(db.Integer, db.ForeignKey('tipo_pagamento.id'))