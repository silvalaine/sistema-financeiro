from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
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

        # Configuração do buffer e documento
        buffer = io.BytesIO()
        width, height = landscape(A4)  # width=841.89, height=595.27
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4),
                               rightMargin=50, leftMargin=50,
                               topMargin=50, bottomMargin=50)
        
        # Container para os elementos do PDF
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=10,
            spaceBefore=20
        )

        # Título
        elements.append(Paragraph('Relatório Financeiro', title_style))
        
        # Subtítulo com filtros
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
            try:
                tipo_pagamento = models['TipoPagamento'].query.get(int(tipo_pagamento_id))
                if tipo_pagamento:
                    filtros.append(f'Forma de Pagamento: {tipo_pagamento.nome}')
            except:
                pass
        
        filtros_text = ' | '.join(filtros) if filtros else 'Sem filtros aplicados'
        elements.append(Paragraph(filtros_text, subtitle_style))
        elements.append(Spacer(1, 20))

        # Totais
        # Query receitas
        receitas_q = db.session.query(models['Receita'])
        if categoria:
            receitas_q = receitas_q.filter(models['Receita'].categoria == categoria)
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                receitas_q = receitas_q.filter(models['Receita'].data >= data_inicio_obj)
            except ValueError:
                pass
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                receitas_q = receitas_q.filter(models['Receita'].data <= data_fim_obj)
            except ValueError:
                pass

        # Query despesas
        despesas_q = db.session.query(models['Despesa'])
        if categoria:
            despesas_q = despesas_q.filter(models['Despesa'].categoria == categoria)
        if subcategoria:
            despesas_q = despesas_q.filter(models['Despesa'].subcategoria == subcategoria)
        if data_inicio:
            try:
                data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                despesas_q = despesas_q.filter(models['Despesa'].data >= data_inicio_obj)
            except ValueError:
                pass
        if data_fim:
            try:
                data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
                despesas_q = despesas_q.filter(models['Despesa'].data <= data_fim_obj)
            except ValueError:
                pass
        if tipo_pagamento_id:
            try:
                despesas_q = despesas_q.filter(models['Despesa'].tipo_pagamento_id == int(tipo_pagamento_id))
            except ValueError:
                pass

        receitas = receitas_q.order_by(models['Receita'].data).all()
        despesas = despesas_q.order_by(models['Despesa'].data).all()
        total_receitas = sum(r.valor for r in receitas) if receitas else 0
        total_despesas = sum(d.valor for d in despesas) if despesas else 0
        saldo = total_receitas - total_despesas

        # Quadro de totais (tabela de resumo)
        resumo_data = [
            ['Resumo Financeiro', ''],
            ['Total Receitas:', f'R$ {total_receitas:,.2f}'],
            ['Total Despesas:', f'R$ {total_despesas:,.2f}'],
            ['Saldo:', f'R$ {saldo:,.2f}']
        ]
        
        resumo_table = Table(resumo_data, colWidths=[200, 150])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#ECF0F1')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.green if saldo >= 0 else colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#ECF0F1')]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(resumo_table)
        elements.append(Spacer(1, 30))

        # Tabela de receitas
        if receitas:
            elements.append(Paragraph('Receitas', heading_style))
            
            # Cabeçalho da tabela
            data = [['Data', 'Descrição', 'Categoria', 'Valor']]
            
            # Dados da tabela
            for r in receitas:
                data.append([
                    r.data.strftime('%d/%m/%Y'),
                    r.descricao[:50] if len(r.descricao) > 50 else r.descricao,  # Limitar tamanho
                    r.categoria or '-',
                    f'R$ {r.valor:,.2f}'
                ])

            # Criar e estilizar a tabela
            available_width = width - 100  # Largura disponível (margens)
            col_widths = [80, available_width - 300, 120, 100]
            table = Table(data, colWidths=col_widths, repeatRows=1)  # repeatRows=1 repete cabeçalho
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
                ('ALIGN', (0, 1), (2, -1), 'LEFT'),
                ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
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
                # Quebra de página
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))

        # Tabela de despesas
        if despesas:
            # Adicionar quebra de página se necessário (antes de despesas)
            if receitas and len(receitas) > 10:
                elements.append(PageBreak())
            
            elements.append(Paragraph('Despesas', heading_style))

            # Cabeçalho da tabela
            data = [['Data', 'Descrição', 'Categoria', 'Subcategoria', 'Forma Pagto', 'Parcela', 'Valor']]
            
            # Dados da tabela
            for d in despesas:
                try:
                    tipo_pagto = models['TipoPagamento'].query.get(d.tipo_pagamento_id) if d.tipo_pagamento_id else None
                    tipo_pagto_nome = tipo_pagto.nome if tipo_pagto else ''
                except:
                    tipo_pagto_nome = ''
                
                parcela = f'{d.parcela_atual}/{d.parcelas}' if d.parcelas and d.parcelas > 1 else '-'
                
                # Limitar tamanho das strings para evitar problemas de layout
                descricao = d.descricao[:40] if len(d.descricao) > 40 else d.descricao
                categoria = (d.categoria or '-')[:20] if d.categoria and len(d.categoria) > 20 else (d.categoria or '-')
                subcategoria = (d.subcategoria or '-')[:20] if d.subcategoria and len(d.subcategoria) > 20 else (d.subcategoria or '-')
                tipo_pagto_nome = tipo_pagto_nome[:15] if len(tipo_pagto_nome) > 15 else tipo_pagto_nome
                
                data.append([
                    d.data.strftime('%d/%m/%Y'),
                    descricao,
                    categoria,
                    subcategoria,
                    tipo_pagto_nome,
                    parcela,
                    f'R$ {d.valor:,.2f}'
                ])

            # Criar e estilizar a tabela
            available_width = width - 100  # Largura disponível
            # Calcular larguras das colunas proporcionalmente
            col_widths = [70, available_width * 0.25, available_width * 0.15, 
                         available_width * 0.15, available_width * 0.12, 50, 90]
            table = Table(data, colWidths=col_widths, repeatRows=1)  # repeatRows=1 repete cabeçalho
            table.setStyle(TableStyle([
                # Cabeçalho
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C0392B')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                # Linhas de dados
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FADBD8')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (4, -1), 'LEFT'),
                ('ALIGN', (5, 1), (5, -1), 'CENTER'),
                ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#C0392B')),
                # Espaçamento
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                # Quebra de página e alinhamento
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                # Quebra de página automática
                ('SPAN', (0, 0), (-1, 0)),  # Cabeçalho ocupa toda a largura
            ]))
            
            elements.append(table)

        # Rodapé com data e numeração de página
        def add_footer(canvas, doc):
            """Função para adicionar rodapé em cada página"""
            canvas.saveState()
            canvas.setFont('Helvetica-Oblique', 8)
            data_geracao = f'Gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}'
            canvas.drawString(50, 30, data_geracao)
            
            # Numeração de página
            canvas.setFont('Helvetica', 8)
            page_num = canvas.getPageNumber()
            canvas.drawCentredString(width/2, 30, f'Página {page_num}')
            
            # Identificação
            canvas.setFont('Helvetica-Bold', 8)
            canvas.drawRightString(width - 50, 30, 'Sistema Financeiro Doméstico')
            canvas.restoreState()
        
        # Construir o PDF
        doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
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
            try:
                tipo = models['TipoPagamento'].query.get(int(tipo_pagamento_id))
                if tipo:
                    filename += f'_{tipo.nome}'
            except:
                pass
        filename += '.pdf'
        
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    except Exception as e:
        app.logger.exception('Erro ao gerar PDF:')
        raise e  # Re-lança a exceção para ser capturada pela rota