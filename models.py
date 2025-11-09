from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def init_default_user():
        """Cria o usuário admin padrão se não existir"""
        admin = Usuario.query.filter_by(username='admin').first()
        if not admin:
            admin = Usuario(username='admin', is_admin=True)
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

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