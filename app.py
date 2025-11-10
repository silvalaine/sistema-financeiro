from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session, g
import os
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import inspect, text
from functools import wraps
import io
import secrets

app = Flask(__name__)
# Use SECRET_KEY and DATABASE_URL from environment when available (useful in hosting)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
# Make sqlite path absolute by default so WSGI processes can find the DB reliably
basedir = os.path.abspath(os.path.dirname(__file__))
default_sqlite = f"sqlite:///{os.path.join(basedir, 'sistema_financeiro.db')}"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default_sqlite)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Receita, CategoriaDespesa, SubcategoriaDespesa, TipoPagamento, Despesa, Usuario
from pdf_generator import generate_pdf_report

db.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_user():
    user_id = session.get('user_id')
    if user_id:
        g.user = Usuario.query.get(user_id)
    else:
        g.user = None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, faça login para acessar esta página.', 'warning')
            return redirect(url_for('login', next=request.url))
        
        if not g.user or not g.user.is_admin:
            flash('Acesso negado. Você precisa ser administrador.', 'danger')
            return redirect(url_for('index'))
            
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/usuarios')
@admin_required
def usuarios():
    usuarios_list = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios_list)

@app.route('/api/usuarios', methods=['POST'])
@admin_required
def adicionar_usuario():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        is_admin = data.get('is_admin', False)
        
        if Usuario.query.filter_by(username=username).first():
            return jsonify({'success': False, 'message': 'Nome de usuário já existe!'})
        
        novo_usuario = Usuario(username=username, is_admin=is_admin)
        novo_usuario.set_password(password)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Usuário criado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/usuarios/<username>', methods=['DELETE'])
@admin_required
def deletar_usuario(username):
    try:
        if username == 'admin':
            return jsonify({'success': False, 'message': 'Não é possível deletar o usuário admin!'})
        
        usuario = Usuario.query.filter_by(username=username).first()
        if not usuario:
            return jsonify({'success': False, 'message': 'Usuário não encontrado!'})
        
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Usuário deletado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/usuarios/alterar-senha', methods=['POST'])
@login_required
def alterar_senha():
    try:
        data = request.get_json()
        senha_atual = data['senha_atual']
        nova_senha = data['nova_senha']
        
        usuario = Usuario.query.get(session['user_id'])
        if not usuario.check_password(senha_atual):
            return jsonify({'success': False, 'message': 'Senha atual incorreta!'})
        
        usuario.set_password(nova_senha)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Senha alterada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/receitas')
@login_required
def receitas():
    receitas_list = Receita.query.order_by(Receita.data.desc()).all()
    return render_template('receitas.html', receitas=receitas_list)

@app.route('/despesas')
@login_required
def despesas():
    despesas_list = Despesa.query.order_by(Despesa.data.desc()).all()
    categorias_list = CategoriaDespesa.query.all()
    tipos_pagamento_list = TipoPagamento.query.filter_by(ativo=True).all()
    return render_template('despesas.html', 
                       despesas=despesas_list, 
                       categorias=categorias_list,
                       tipos_pagamento=tipos_pagamento_list)

@app.route('/relatorios')
@login_required
def relatorios():
    categorias_list = CategoriaDespesa.query.all()
    tipos_pagamento_list = TipoPagamento.query.filter_by(ativo=True).all()
    return render_template('relatorios.html', 
                       categorias=categorias_list,
                       tipos_pagamento=tipos_pagamento_list)

@app.route('/categorias')
@login_required
def categorias():
    categorias_list = CategoriaDespesa.query.all()
    return render_template('categorias.html', categorias=categorias_list)

@app.route('/tipos-pagamento')
@login_required
def tipos_pagamento():
    tipos_list = TipoPagamento.query.order_by(TipoPagamento.nome).all()
    return render_template('tipos_pagamento.html', tipos_pagamento=tipos_list)

# API Routes
@app.route('/api/relatorios/resumo')
@login_required
def relatorio_resumo():
    try:
        categoria = request.args.get('categoria')
        subcategoria = request.args.get('subcategoria')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        status = request.args.get('status')
        tipo_pagamento_id = request.args.get('tipo_pagamento_id')

        # Parse date filters to date objects when provided
        data_inicio_obj = None
        data_fim_obj = None
        if data_inicio:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        if data_fim:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()

        # Total receitas
        receitas_q = db.session.query(func.sum(Receita.valor))
        if categoria:
            receitas_q = receitas_q.filter(Receita.categoria == categoria)
        if data_inicio_obj:
            receitas_q = receitas_q.filter(Receita.data >= data_inicio_obj)
        if data_fim_obj:
            receitas_q = receitas_q.filter(Receita.data <= data_fim_obj)
        if status:
            if status == 'efetivado':
                receitas_q = receitas_q.filter(Receita.efetivado == True)
            elif status == 'pendente':
                receitas_q = receitas_q.filter(Receita.efetivado == False)
        total_receitas = receitas_q.scalar() or 0

        # Total despesas
        despesas_q = db.session.query(func.sum(Despesa.valor))
        if categoria:
            despesas_q = despesas_q.filter(Despesa.categoria == categoria)
        if subcategoria:
            despesas_q = despesas_q.filter(Despesa.subcategoria == subcategoria)
        if data_inicio_obj:
            despesas_q = despesas_q.filter(Despesa.data >= data_inicio_obj)
        if data_fim_obj:
            despesas_q = despesas_q.filter(Despesa.data <= data_fim_obj)
        if tipo_pagamento_id:
            despesas_q = despesas_q.filter(Despesa.tipo_pagamento_id == int(tipo_pagamento_id))
        if status:
            if status == 'efetivado':
                despesas_q = despesas_q.filter(Despesa.efetivado == True)
            elif status == 'pendente':
                despesas_q = despesas_q.filter(Despesa.efetivado == False)
        total_despesas = despesas_q.scalar() or 0

        # Saldo atual
        saldo_atual = total_receitas - total_despesas

        # Receitas por categoria
        receitas_categoria_q = db.session.query(
            Receita.categoria,
            func.sum(Receita.valor).label('total')
        )
        if categoria:
            receitas_categoria_q = receitas_categoria_q.filter(Receita.categoria == categoria)
        if data_inicio_obj:
            receitas_categoria_q = receitas_categoria_q.filter(Receita.data >= data_inicio_obj)
        if data_fim_obj:
            receitas_categoria_q = receitas_categoria_q.filter(Receita.data <= data_fim_obj)
        if status:
            if status == 'efetivado':
                receitas_categoria_q = receitas_categoria_q.filter(Receita.efetivado == True)
            elif status == 'pendente':
                receitas_categoria_q = receitas_categoria_q.filter(Receita.efetivado == False)
        receitas_categoria = receitas_categoria_q.group_by(Receita.categoria).all()

        # Despesas por categoria
        despesas_categoria_q = db.session.query(
            Despesa.categoria,
            func.sum(Despesa.valor).label('total')
        )
        if categoria:
            despesas_categoria_q = despesas_categoria_q.filter(Despesa.categoria == categoria)
        if subcategoria:
            despesas_categoria_q = despesas_categoria_q.filter(Despesa.subcategoria == subcategoria)
        if data_inicio_obj:
            despesas_categoria_q = despesas_categoria_q.filter(Despesa.data >= data_inicio_obj)
        if data_fim_obj:
            despesas_categoria_q = despesas_categoria_q.filter(Despesa.data <= data_fim_obj)
        if status:
            if status == 'efetivado':
                despesas_categoria_q = despesas_categoria_q.filter(Despesa.efetivado == True)
            elif status == 'pendente':
                despesas_categoria_q = despesas_categoria_q.filter(Despesa.efetivado == False)
        if tipo_pagamento_id:
            despesas_categoria_q = despesas_categoria_q.filter(Despesa.tipo_pagamento_id == int(tipo_pagamento_id))
        despesas_categoria = despesas_categoria_q.group_by(Despesa.categoria).all()

        # Últimas transações
        ultimas_receitas_q = db.session.query(Receita).order_by(Receita.data.desc())
        if categoria:
            ultimas_receitas_q = ultimas_receitas_q.filter(Receita.categoria == categoria)
        if data_inicio_obj:
            ultimas_receitas_q = ultimas_receitas_q.filter(Receita.data >= data_inicio_obj)
        if data_fim_obj:
            ultimas_receitas_q = ultimas_receitas_q.filter(Receita.data <= data_fim_obj)
        if status:
            if status == 'efetivado':
                ultimas_receitas_q = ultimas_receitas_q.filter(Receita.efetivado == True)
            elif status == 'pendente':
                ultimas_receitas_q = ultimas_receitas_q.filter(Receita.efetivado == False)
        ultimas_receitas = ultimas_receitas_q.limit(5).all()

        ultimas_despesas_q = db.session.query(Despesa).order_by(Despesa.data.desc())
        if categoria:
            ultimas_despesas_q = ultimas_despesas_q.filter(Despesa.categoria == categoria)
        if subcategoria:
            ultimas_despesas_q = ultimas_despesas_q.filter(Despesa.subcategoria == subcategoria)
        if data_inicio_obj:
            ultimas_despesas_q = ultimas_despesas_q.filter(Despesa.data >= data_inicio_obj)
        if data_fim_obj:
            ultimas_despesas_q = ultimas_despesas_q.filter(Despesa.data <= data_fim_obj)
        if tipo_pagamento_id:
            ultimas_despesas_q = ultimas_despesas_q.filter(Despesa.tipo_pagamento_id == int(tipo_pagamento_id))
        if status:
            if status == 'efetivado':
                ultimas_despesas_q = ultimas_despesas_q.filter(Despesa.efetivado == True)
            elif status == 'pendente':
                ultimas_despesas_q = ultimas_despesas_q.filter(Despesa.efetivado == False)
        ultimas_despesas = ultimas_despesas_q.limit(5).all()
        
        return jsonify({
            'total_receitas': total_receitas,
            'total_despesas': total_despesas,
            'saldo_atual': saldo_atual,
            'receitas_categoria': [{'categoria': r.categoria, 'total': r.total} for r in receitas_categoria],
            'despesas_categoria': [{'categoria': d.categoria, 'total': d.total} for d in despesas_categoria],
            'ultimas_receitas': [{'descricao': r.descricao, 'valor': r.valor, 'data': r.data.strftime('%d/%m/%Y'), 'categoria': r.categoria, 'efetivado': bool(r.efetivado)} for r in ultimas_receitas],
            'ultimas_despesas': [{'descricao': d.descricao, 'valor': d.valor, 'data': d.data.strftime('%d/%m/%Y'), 'categoria': d.categoria, 'subcategoria': d.subcategoria, 'efetivado': bool(d.efetivado)} for d in ultimas_despesas]
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/relatorio/pdf')
@login_required
def gerar_relatorio_pdf():
    try:
        if not hasattr(app, 'logger'):
            import logging
            app.logger = logging.getLogger('flask.app')
            app.logger.setLevel(logging.DEBUG)
        
        models = {
            'Receita': Receita,
            'Despesa': Despesa,
            'TipoPagamento': TipoPagamento
        }
        
        return generate_pdf_report(app, request, make_response, db, models)
    except Exception as e:
        app.logger.exception('Erro ao gerar PDF:')
        return jsonify({'error': f'Erro ao gerar PDF: {str(e)}'}), 500

@app.route('/api/receita', methods=['POST'])
@login_required
def adicionar_receita():
    try:
        data = request.get_json()
        valor_previsto = float(data['valor_previsto'])
        # Se valor efetivo não foi informado, usa o valor previsto quando efetivado=True, senão usa 0
        valor = float(data['valor']) if data.get('valor') else (valor_previsto if data.get('efetivado') else 0.0)
        efetivado = data.get('efetivado', False)
        
        receita = Receita(
            descricao=data['descricao'],
            valor_previsto=valor_previsto,
            valor=valor,  # Agora sempre terá um valor (previsto, efetivo ou 0)
            data=datetime.strptime(data['data'], '%Y-%m-%d').date(),
            categoria=data['categoria'],
            efetivado=efetivado
        )
        
        db.session.add(receita)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Receita adicionada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/despesa', methods=['POST'])
@login_required
def adicionar_despesa():
    try:
        data = request.get_json()
        num_parcelas = int(data.get('parcelas', 1))
        valor_previsto_total = float(data['valor_previsto'])
        # Se valor efetivo não foi informado, usa o valor previsto quando efetivado=True, senão usa 0
        valor_efetivo = float(data['valor']) if data.get('valor') else (valor_previsto_total if data.get('efetivado') else 0.0)
        valor_previsto_parcela = round(valor_previsto_total / num_parcelas, 2)
        valor_efetivo_parcela = round(valor_efetivo / num_parcelas, 2)
        data_inicial = datetime.strptime(data['data'], '%Y-%m-%d').date()
        efetivado = data.get('efetivado', False)
        
        compra_parcelada_id = None
        if num_parcelas > 1:
            compra_parcelada_id = int(datetime.now().timestamp())
        
        for i in range(num_parcelas):
            data_parcela = data_inicial.replace(year=data_inicial.year + ((data_inicial.month + i) - 1) // 12,
                                           month=((data_inicial.month + i - 1) % 12) + 1)
            
            # Calcular valor previsto desta parcela
            valor_previsto_desta = valor_previsto_parcela
            if i == num_parcelas - 1:  # Ajustar última parcela para evitar centavos
                valor_previsto_desta = round(valor_previsto_total - (valor_previsto_parcela * (num_parcelas - 1)), 2)
            
            # Calcular valor efetivo desta parcela
            valor_efetivo_desta = valor_efetivo_parcela
            if i == num_parcelas - 1:  # Ajustar última parcela
                valor_efetivo_desta = round(valor_efetivo - (valor_efetivo_parcela * (num_parcelas - 1)), 2)
            
            descricao = data['descricao']
            if num_parcelas > 1:
                descricao = f"{descricao} ({i+1}/{num_parcelas})"
            
            despesa = Despesa(
                descricao=descricao,
                valor_previsto=valor_previsto_desta,
                valor=valor_efetivo_desta,
                data=data_parcela,
                categoria=data['categoria'],
                subcategoria=data.get('subcategoria'),
                tipo_pagamento_id=data.get('tipo_pagamento_id'),
                parcelas=num_parcelas,
                parcela_atual=i+1,
                compra_parcelada_id=compra_parcelada_id,
                efetivado=efetivado
            )
            db.session.add(despesa)
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': f'Despesa {("parcelada em " + str(num_parcelas) + "x") if num_parcelas > 1 else ""} adicionada com sucesso!'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/receita/<int:id>', methods=['DELETE', 'PUT'])
@login_required
def gerenciar_receita(id):
    try:
        receita = Receita.query.get_or_404(id)
        
        if request.method == 'DELETE':
            db.session.delete(receita)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Receita deletada com sucesso!'})
        
        elif request.method == 'PUT':
            data = request.get_json()
            if 'efetivado' in data:
                receita.efetivado = data['efetivado']
                # Se marcado como efetivado e não tem valor, usa o previsto
                if receita.efetivado and (not receita.valor or receita.valor == 0):
                    receita.valor = receita.valor_previsto
            
            # Atualiza valor se fornecido
            if 'valor' in data:
                receita.valor = float(data['valor'])
            
            db.session.commit()
            return jsonify({
                'success': True, 
                'message': 'Receita atualizada com sucesso!',
                'data': {
                    'id': receita.id,
                    'efetivado': receita.efetivado,
                    'valor': receita.valor,
                    'valor_previsto': receita.valor_previsto
                }
            })
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/despesa/<int:id>', methods=['DELETE', 'PUT'])
@login_required
def gerenciar_despesa(id):
    try:
        despesa = Despesa.query.get_or_404(id)
        
        if request.method == 'DELETE':
            compra_parcelada_id = request.args.get('compra_parcelada_id')
            opcao_delete = request.args.get('opcao_delete')
            
            if compra_parcelada_id and opcao_delete:
                compra_parcelada_id = int(compra_parcelada_id)
                
                if opcao_delete == '1':  # Deletar apenas esta parcela
                    db.session.delete(despesa)
                    mensagem = 'Parcela deletada com sucesso!'
                
                elif opcao_delete == '2':  # Deletar esta e parcelas futuras
                    parcelas_futuras = Despesa.query.filter(
                        Despesa.compra_parcelada_id == compra_parcelada_id,
                        Despesa.parcela_atual >= despesa.parcela_atual
                    ).all()
                    for p in parcelas_futuras:
                        db.session.delete(p)
                    mensagem = f'{len(parcelas_futuras)} parcela(s) futura(s) deletada(s) com sucesso!'
                
                elif opcao_delete == '3':  # Deletar todas as parcelas
                    todas_parcelas = Despesa.query.filter_by(
                        compra_parcelada_id=compra_parcelada_id
                    ).all()
                    for p in todas_parcelas:
                        db.session.delete(p)
                    mensagem = f'Todas as {len(todas_parcelas)} parcela(s) foram deletadas com sucesso!'
                
                else:
                    return jsonify({'success': False, 'message': 'Opção inválida!'})
            
            else:  # Despesa normal (não parcelada)
                db.session.delete(despesa)
                mensagem = 'Despesa deletada com sucesso!'
            
            db.session.commit()
            return jsonify({'success': True, 'message': mensagem})
            
        elif request.method == 'PUT':
            data = request.get_json()
            compra_parcelada_id = data.get('compra_parcelada_id')
            
            # Se tem ID de compra parcelada, pergunta se quer atualizar todas as parcelas
            if compra_parcelada_id and data.get('atualizar_todas_parcelas'):
                despesas = Despesa.query.filter_by(compra_parcelada_id=compra_parcelada_id).all()
                for d in despesas:
                    if 'efetivado' in data:
                        d.efetivado = data['efetivado']
                        # Se marcado como efetivado e não tem valor, usa o previsto
                        if d.efetivado and (not d.valor or d.valor == 0):
                            d.valor = d.valor_previsto
                    if 'valor' in data:
                        # Calcula proporcionalmente baseado no valor_previsto
                        proporcao = d.valor_previsto / despesa.valor_previsto if despesa.valor_previsto != 0 else 0
                        d.valor = float(data['valor']) * proporcao
            else:
                # Atualiza apenas a despesa atual
                if 'efetivado' in data:
                    despesa.efetivado = data['efetivado']
                    # Se marcado como efetivado e não tem valor, usa o previsto
                    if despesa.efetivado and (not despesa.valor or despesa.valor == 0):
                        despesa.valor = despesa.valor_previsto
                if 'valor' in data:
                    despesa.valor = float(data['valor'])
            
            db.session.commit()
            return jsonify({
                'success': True, 
                'message': 'Despesa atualizada com sucesso!',
                'data': {
                    'id': despesa.id,
                    'efetivado': despesa.efetivado,
                    'valor': despesa.valor,
                    'valor_previsto': despesa.valor_previsto
                }
            })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/categoria', methods=['POST'])
@login_required
def adicionar_categoria():
    try:
        data = request.get_json()
        categoria = CategoriaDespesa(
            nome=data['nome'],
            descricao=data.get('descricao', '')
        )
        db.session.add(categoria)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Categoria adicionada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/categoria/<int:id>', methods=['DELETE'])
@login_required
def deletar_categoria(id):
    try:
        categoria = CategoriaDespesa.query.get_or_404(id)
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Categoria deletada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subcategoria', methods=['POST'])
@login_required
def adicionar_subcategoria():
    try:
        data = request.get_json()
        subcategoria = SubcategoriaDespesa(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            categoria_id=data['categoria_id']
        )
        db.session.add(subcategoria)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subcategoria adicionada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subcategoria/<int:id>', methods=['DELETE'])
@login_required
def deletar_subcategoria(id):
    try:
        subcategoria = SubcategoriaDespesa.query.get_or_404(id)
        db.session.delete(subcategoria)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Subcategoria deletada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/subcategorias/<int:categoria_id>')
@login_required
def obter_subcategorias(categoria_id):
    try:
        subcategorias = SubcategoriaDespesa.query.filter_by(categoria_id=categoria_id).all()
        return jsonify([{'id': s.id, 'nome': s.nome} for s in subcategorias])
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/tipo-pagamento', methods=['POST'])
@login_required
def adicionar_tipo_pagamento():
    try:
        data = request.get_json()
        tipo = TipoPagamento(
            nome=data['nome'],
            descricao=data.get('descricao', '')
        )
        db.session.add(tipo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Tipo de pagamento adicionado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/tipo-pagamento/<int:id>', methods=['DELETE'])
@login_required
def deletar_tipo_pagamento(id):
    try:
        tipo = TipoPagamento.query.get_or_404(id)
        if len(tipo.despesas) > 0:
            return jsonify({'success': False, 'message': 'Não é possível excluir um tipo de pagamento que está sendo usado em despesas.'})
        db.session.delete(tipo)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Tipo de pagamento deletado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/tipo-pagamento/<int:id>/toggle', methods=['POST'])
@login_required
def alternar_status_tipo_pagamento(id):
    try:
        tipo = TipoPagamento.query.get_or_404(id)
        tipo.ativo = not tipo.ativo
        db.session.commit()
        return jsonify({'success': True, 'message': 'Status alterado com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/tipos-pagamento')
@login_required
def obter_tipos_pagamento():
    try:
        tipos = TipoPagamento.query.filter_by(ativo=True).all()
        return jsonify([{'id': t.id, 'nome': t.nome} for t in tipos])
    except Exception as e:
        return jsonify({'error': str(e)})

def _ensure_columns():
    """Verifica se todas as colunas necessárias existem nas tabelas e as adiciona se necessário."""
    try:
        inspector = inspect(db.engine)
        
        # Colunas para a tabela despesa
        if 'despesa' in inspector.get_table_names():
            cols_despesa = [c['name'] for c in inspector.get_columns('despesa')]
            colunas_despesa = {
                'subcategoria': 'VARCHAR(100)',
                'parcelas': 'INTEGER DEFAULT 1',
                'parcela_atual': 'INTEGER DEFAULT 1',
                'compra_parcelada_id': 'INTEGER',
                'tipo_pagamento_id': 'INTEGER',
                'valor_previsto': 'FLOAT',
                'efetivado': 'BOOLEAN DEFAULT 0'
            }
            
            for col_name, col_type in colunas_despesa.items():
                if col_name not in cols_despesa:
                    with db.engine.begin() as conn:
                        conn.execute(text(f"ALTER TABLE despesa ADD COLUMN {col_name} {col_type}"))
                    print(f"Coluna '{col_name}' adicionada na tabela 'despesa'.")
                    
                    # Se for coluna valor_previsto, copiar valor inicial da coluna valor
                    if col_name == 'valor_previsto':
                        with db.engine.begin() as conn:
                            conn.execute(text("UPDATE despesa SET valor_previsto = valor WHERE valor_previsto IS NULL"))
            
            if 'tipo_pagamento_id' in cols_despesa:
                try:
                    with db.engine.begin() as conn:
                        conn.execute(text("DROP INDEX IF EXISTS ix_despesa_tipo_pagamento_id"))
                        conn.execute(text("CREATE INDEX ix_despesa_tipo_pagamento_id ON despesa (tipo_pagamento_id)"))
                except Exception as e:
                    print('Aviso: Falha ao criar índice tipo_pagamento_id:', e)
        
        # Colunas para a tabela receita
        if 'receita' in inspector.get_table_names():
            cols_receita = [c['name'] for c in inspector.get_columns('receita')]
            colunas_receita = {
                'valor_previsto': 'FLOAT',
                'efetivado': 'BOOLEAN DEFAULT 0'
            }
            
            for col_name, col_type in colunas_receita.items():
                if col_name not in cols_receita:
                    with db.engine.begin() as conn:
                        conn.execute(text(f"ALTER TABLE receita ADD COLUMN {col_name} {col_type}"))
                    print(f"Coluna '{col_name}' adicionada na tabela 'receita'.")
                    
                    # Se for coluna valor_previsto, copiar valor inicial da coluna valor
                    if col_name == 'valor_previsto':
                        with db.engine.begin() as conn:
                            conn.execute(text("UPDATE receita SET valor_previsto = valor WHERE valor_previsto IS NULL"))
                    
    except Exception as e:
        print('Falha ao garantir colunas:', e)

with app.app_context():
    db.create_all()
    _ensure_columns()
    Usuario.init_default_user()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)