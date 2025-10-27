from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
import io
from datetime import datetime

def generate_pdf_report(app, request, make_response, db, models):
    try:
        # Parâmetros do relatório
        categoria = request.args.get('categoria')
        subcategoria = request.args.get('subcategoria')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        tipo_pagamento_id = request.args.get('tipo_pagamento_id')

        # Configuração do buffer e canvas
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)  # width=841.89, height=595.27
        margin = 50  # Margem padrão

        # Título
        c.setFont('Helvetica-Bold', 20)
        c.drawString(width/2 - 80, height-margin, 'Relatório Financeiro')

        # Subtítulo com filtros
        c.setFont('Helvetica', 10)
        filtros = []
        if categoria:
            filtros.append(f'Categoria: {categoria}')
        if subcategoria:
            filtros.append(f'Subcategoria: {subcategoria}')
        if data_inicio:
            filtros.append(f'Período: {data_inicio}')
            if data_fim:
                filtros[-1] += f' a {data_fim}'
        elif data_fim:
            filtros.append(f'Até: {data_fim}')
        if tipo_pagamento_id:
            tipo_pagamento = models['TipoPagamento'].query.get(int(tipo_pagamento_id))
            if tipo_pagamento:
                filtros.append(f'Forma de Pagamento: {tipo_pagamento.nome}')
        
        filtros_text = ' | '.join(filtros) if filtros else 'Sem filtros aplicados'
        c.drawString(width/2 - len(filtros_text)*2.5, height-60, filtros_text)

        # Totais
        # Query receitas
        receitas_q = db.session.query(models['Receita'])
        if categoria:
            receitas_q = receitas_q.filter(models['Receita'].categoria == categoria)
        if data_inicio:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            receitas_q = receitas_q.filter(models['Receita'].data >= data_inicio_obj)
        if data_fim:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            receitas_q = receitas_q.filter(models['Receita'].data <= data_fim_obj)

        # Query despesas
        despesas_q = db.session.query(models['Despesa'])
        if categoria:
            despesas_q = despesas_q.filter(models['Despesa'].categoria == categoria)
        if subcategoria:
            despesas_q = despesas_q.filter(models['Despesa'].subcategoria == subcategoria)
        if data_inicio:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            despesas_q = despesas_q.filter(models['Despesa'].data >= data_inicio_obj)
        if data_fim:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            despesas_q = despesas_q.filter(models['Despesa'].data <= data_fim_obj)
        if tipo_pagamento_id:
            despesas_q = despesas_q.filter(models['Despesa'].tipo_pagamento_id == int(tipo_pagamento_id))

        receitas = receitas_q.order_by(models['Receita'].data).all()
        despesas = despesas_q.order_by(models['Despesa'].data).all()
        total_receitas = sum(r.valor for r in receitas)
        total_despesas = sum(d.valor for d in despesas)
        saldo = total_receitas - total_despesas

        # Quadro de totais
        box_width = 200
        box_height = 80
        box_x = width - box_width - margin
        box_y = height - margin - box_height - 10
        
        # Desenha o box
        c.setFillColor(colors.lightgrey)
        c.rect(box_x, box_y, box_width, box_height, fill=1)
        c.setFillColor(colors.black)
        
        # Títulos e valores
        c.setFont('Helvetica-Bold', 12)
        c.drawString(box_x + 10, box_y + box_height - 20, 'Resumo Financeiro')
        
        c.setFont('Helvetica', 10)
        c.drawString(box_x + 10, box_y + box_height - 40, f'Total Receitas:')
        c.drawRightString(box_x + box_width - 10, box_y + box_height - 40, f'R$ {total_receitas:,.2f}')
        
        c.drawString(box_x + 10, box_y + box_height - 55, f'Total Despesas:')
        c.drawRightString(box_x + box_width - 10, box_y + box_height - 55, f'R$ {total_despesas:,.2f}')
        
        c.setFillColor(colors.green if saldo >= 0 else colors.red)
        c.setFont('Helvetica-Bold', 11)
        c.drawString(box_x + 10, box_y + 15, f'Saldo:')
        c.drawRightString(box_x + box_width - 10, box_y + 15, f'R$ {saldo:,.2f}')
        c.setFillColor(colors.black)

        # Tabela de receitas
        if receitas:
            y_start_receitas = height-margin-box_height-50
            c.setFont('Helvetica-Bold', 12)
            c.drawString(margin, y_start_receitas, 'Receitas')

            # Cabeçalho da tabela
            data = [['Data', 'Descrição', 'Categoria', 'Valor']]
            
            # Dados da tabela
            for r in receitas:
                data.append([
                    r.data.strftime('%d/%m/%Y'),
                    r.descricao,
                    r.categoria,
                    f'R$ {r.valor:,.2f}'
                ])

            # Criar e estilizar a tabela
            col_widths = [80, width-360-2*margin, 120, 100]
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                # Cabeçalho
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Linhas de dados
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#EBEDEF')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (2, -1), 'LEFT'),  # Alinhar à esquerda
                ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),  # Valores à direita
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#2C3E50')),
                # Espaçamento
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            table.wrapOn(c, width, height)
            table.drawOn(c, margin, y_start_receitas-30-len(receitas)*16)

        # Tabela de despesas
        if despesas:
            # Calcula a posição Y para a tabela de despesas
            y_position = y_start_receitas-50-len(receitas)*16 if receitas else height-180
            
            # Verifica se há espaço suficiente na página atual
            min_space_needed = len(despesas)*16 + 100  # espaço necessário para a tabela + margens
            if y_position - min_space_needed < margin:
                c.showPage()  # Nova página
                y_position = height - margin - 50  # Recomeça do topo com margem
                
            c.setFont('Helvetica-Bold', 12)
            c.drawString(margin, y_position, 'Despesas')

            # Cabeçalho da tabela
            data = [['Data', 'Descrição', 'Categoria', 'Subcategoria', 'Forma Pagto', 'Parcela', 'Valor']]
            
            # Dados da tabela
            for d in despesas:
                tipo_pagto = models['TipoPagamento'].query.get(d.tipo_pagamento_id)
                tipo_pagto_nome = tipo_pagto.nome if tipo_pagto else ''
                
                parcela = f'{d.parcela_atual}/{d.parcelas}' if d.parcelas > 1 else '-'
                
                data.append([
                    d.data.strftime('%d/%m/%Y'),
                    d.descricao,
                    d.categoria,
                    d.subcategoria or '-',
                    tipo_pagto_nome,
                    parcela,
                    f'R$ {d.valor:,.2f}'
                ])

            # Criar e estilizar a tabela
            available_width = width - 2*margin
            desc_width = available_width - 80 - 100 - 100 - 100 - 60 - 100  # Restante para descrição
            col_widths = [80, desc_width, 100, 100, 100, 60, 100]
            table = Table(data, colWidths=col_widths)
            table.setStyle(TableStyle([
                # Cabeçalho
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C0392B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Linhas de dados
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FADBD8')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (4, -1), 'LEFT'),  # Alinhar à esquerda
                ('ALIGN', (5, 1), (5, -1), 'CENTER'),  # Parcela centralizada
                ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),  # Valores à direita
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#C0392B')),
                # Espaçamento
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            table.wrapOn(c, width, height)
            table.drawOn(c, margin, y_position-30-len(despesas)*16)

        # Linha divisória
        c.setStrokeColor(colors.grey)
        c.line(margin, margin, width-margin, margin)

        # Data do relatório e numeração de página
        c.setFont('Helvetica-Oblique', 8)
        data_geracao = f'Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}'
        c.drawString(margin, margin-15, data_geracao)
        
        # Numeração de página centralizada
        c.setFont('Helvetica', 8)
        pagina = 'Página 1'
        c.drawString(width/2 - 20, margin-15, pagina)
        
        # Logo ou identificação à direita
        c.setFont('Helvetica-Bold', 8)
        c.drawRightString(width-margin, margin-15, 'Sistema Financeiro Doméstico')

        # Salvar o PDF
        c.save()
        buffer.seek(0)
        
        # Criar resposta PDF
        response = make_response(buffer.getvalue())
        response.mimetype = 'application/pdf'
        
        # Nome do arquivo
        filename = 'relatorio_financeiro'
        if categoria:
            filename += f'_{categoria}'
        if subcategoria:
            filename += f'_{subcategoria}'
        if data_inicio:
            filename += f'_{data_inicio}'
        if data_fim:
            filename += f'_{data_fim}'
        if tipo_pagamento_id:
            tipo = models['TipoPagamento'].query.get(int(tipo_pagamento_id))
            if tipo:
                filename += f'_{tipo.nome}'
        filename += '.pdf'
        
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        app.logger.exception('Erro ao gerar PDF:')
        raise e  # Re-lança a exceção para ser capturada pela rota