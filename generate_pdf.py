from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import io

def generate_pdf(app, query_results, filters):
    try:
        # Extrair dados dos resultados da query
        resultados = query_results['resultados']
        total_geral = query_results['total_geral']
        receitas_categoria = query_results['receitas_categoria']
        despesas_categoria = query_results['despesas_categoria']
        total_receitas = query_results['total_receitas']
        total_despesas = query_results['total_despesas']
        ultimas_receitas = query_results['ultimas_receitas']
        ultimas_despesas = query_results['ultimas_despesas']
        
        # Extrair filtros
        categoria = filters['categoria']
        subcategoria = filters['subcategoria']
        data_inicio = filters['data_inicio']
        data_fim = filters['data_fim']
        tipo_pagamento_nome = filters['tipo_pagamento_nome']
        
        # Criar buffer para o PDF
        buffer = io.BytesIO()
        
        # Configurar documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            spaceBefore=20
        )
        
        # Conteúdo do PDF
        story = []
        
        # Título com filtros aplicados
        titulo = "Relatório Financeiro"
        if categoria:
            titulo += f"\nCategoria: {categoria}"
            if subcategoria:
                titulo += f" / {subcategoria}"
        if tipo_pagamento_nome:
            titulo += f"\nForma de Pagamento: {tipo_pagamento_nome}"
        if data_inicio or data_fim:
            titulo += "\nPeríodo: "
            if data_inicio:
                titulo += data_inicio.strftime('%d/%m/%Y')
            if data_inicio and data_fim:
                titulo += " a "
            if data_fim:
                titulo += data_fim.strftime('%d/%m/%Y')
        
        story.append(Paragraph(titulo, title_style))
        story.append(Spacer(1, 20))
        
        # Resumo Geral
        story.append(Paragraph("Resumo Geral", heading_style))
        
        resumo_data = [
            ['Item', 'Valor'],
            ['Total Receitas', f'R$ {total_receitas:,.2f}'],
            ['Total Despesas', f'R$ {total_despesas:,.2f}'],
            ['Saldo', f'R$ {(total_receitas - total_despesas):,.2f}']
        ]
        
        resumo_table = Table(resumo_data, colWidths=[3*inch, 2*inch])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(resumo_table)
        story.append(Spacer(1, 20))
        
        # Despesas por Categoria
        if despesas_categoria:
            story.append(Paragraph("Despesas por Categoria", heading_style))
            despesas_data = [['Categoria', 'Total']]
            for d in despesas_categoria:
                despesas_data.append([d.categoria, f'R$ {d.total:,.2f}'])
            
            despesas_table = Table(despesas_data, colWidths=[3*inch, 2*inch])
            despesas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.red),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(despesas_table)
            story.append(Spacer(1, 20))
        
        # Últimas Transações
        if ultimas_receitas or ultimas_despesas:
            story.append(Paragraph("Últimas Transações", heading_style))
            
            transacoes_data = [['Data', 'Tipo', 'Descrição', 'Subcategoria', 'Forma Pagto', 'Valor']]
            
            # Adicionar receitas
            for r in ultimas_receitas:
                transacoes_data.append([
                    r.data.strftime('%d/%m/%Y'),
                    'Receita',
                    r.descricao,
                    '-',
                    '-',
                    f'R$ {r.valor:,.2f}'
                ])
            
            # Adicionar despesas
            for d in ultimas_despesas:
                transacoes_data.append([
                    d.data.strftime('%d/%m/%Y'),
                    'Despesa',
                    d.descricao,
                    d.subcategoria or '-',
                    d.tipo_pagamento.nome if d.tipo_pagamento else '-',
                    f'R$ {d.valor:,.2f}'
                ])
            
            # Ordenar por data
            transacoes_data = [transacoes_data[0]] + sorted(
                transacoes_data[1:],
                key=lambda x: datetime.strptime(x[0], '%d/%m/%Y'),
                reverse=True
            )
            
            if len(transacoes_data) > 1:
                transacoes_table = Table(transacoes_data, colWidths=[0.8*inch, 0.8*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
                transacoes_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('ALIGN', (-1, 1), (-1, -1), 'RIGHT')  # Alinhar valores à direita
                ]))
                story.append(transacoes_table)
        
        # Rodapé
        story.append(Spacer(1, 30))
        story.append(Paragraph(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        return buffer
        
    except Exception as e:
        app.logger.exception('Erro ao gerar PDF:')
        raise e