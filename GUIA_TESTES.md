# 🧪 Guia de Testes - Sistema Financeiro

## 📋 Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Iniciar o Sistema](#iniciar-o-sistema)
3. [Testes Manuais](#testes-manuais)
4. [Testes Automatizados](#testes-automatizados)
5. [Checklist de Funcionalidades](#checklist-de-funcionalidades)

---

## 🔧 Pré-requisitos

Antes de testar, certifique-se de que:

1. **Python 3.7+ está instalado**
   ```bash
   python --version
   ```

2. **Dependências estão instaladas**
   ```bash
   pip install -r requirements.txt
   ```

3. **Porta 5000 está disponível** (ou altere a porta no `app.py`)

---

## 🚀 Iniciar o Sistema

### Passo 1: Iniciar o servidor
```bash
python app.py
```

Você deve ver uma mensagem similar a:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### Passo 2: Acessar no navegador
Abra seu navegador e acesse:
```
http://localhost:5000
```

---

## 🖱️ Testes Manuais

### 1. Teste da Página Inicial (`/`)
- [ ] A página carrega sem erros
- [ ] O menu de navegação está visível
- [ ] Os cards de resumo aparecem (mesmo que vazios)
- [ ] Não há erros no console do navegador (F12)

### 2. Teste de Receitas (`/receitas`)

#### 2.1. Adicionar Receita
- [ ] Clicar em "Nova Receita" abre o modal
- [ ] Preencher todos os campos:
  - Descrição: "Salário Janeiro"
  - Valor: 5000.00
  - Data: 2025-01-15
  - Categoria: "Salário"
- [ ] Clicar em "Adicionar Receita"
- [ ] Verificar mensagem de sucesso
- [ ] Verificar se a receita aparece na tabela

#### 2.2. Validações de Receita
- [ ] Tentar adicionar receita sem descrição → Deve mostrar erro
- [ ] Tentar adicionar receita com valor 0 → Deve mostrar erro
- [ ] Tentar adicionar receita com valor negativo → Deve mostrar erro
- [ ] Tentar adicionar receita com data inválida → Deve mostrar erro

#### 2.3. Deletar Receita
- [ ] Clicar no ícone de lixeira de uma receita
- [ ] Confirmar a exclusão
- [ ] Verificar se a receita foi removida da tabela

### 3. Teste de Despesas (`/despesas`)

#### 3.1. Adicionar Despesa Simples
- [ ] Clicar em "Nova Despesa" abre o modal
- [ ] Preencher campos:
  - Descrição: "Supermercado"
  - Valor: 350.50
  - Data: 2025-01-20
  - Categoria: Selecionar uma categoria
  - Parcelas: 1
- [ ] Clicar em "Adicionar Despesa"
- [ ] Verificar mensagem de sucesso
- [ ] Verificar se a despesa aparece na tabela

#### 3.2. Adicionar Despesa Parcelada
- [ ] Preencher formulário:
  - Descrição: "Notebook"
  - Valor: 3000.00
  - Data: 2025-01-15
  - Categoria: Selecionar categoria
  - Parcelas: 6
- [ ] Verificar informações de parcelamento (valor por parcela, período)
- [ ] Adicionar a despesa
- [ ] Verificar se 6 despesas foram criadas
- [ ] Verificar se as datas estão corretas (mensais)
- [ ] Verificar se os valores estão corretos (última parcela pode ter ajuste)

#### 3.3. Validações de Despesa
- [ ] Tentar adicionar despesa sem descrição → Erro
- [ ] Tentar adicionar despesa com valor 0 → Erro
- [ ] Tentar adicionar despesa com valor negativo → Erro
- [ ] Tentar adicionar despesa com mais de 120 parcelas → Erro
- [ ] Tentar adicionar despesa com data inválida → Erro

#### 3.4. Deletar Despesa Parcelada
- [ ] Adicionar uma despesa parcelada (ex: 3 parcelas)
- [ ] Tentar deletar a primeira parcela
- [ ] Verificar opções:
  - [ ] Opção 1: Deletar apenas esta parcela
  - [ ] Opção 2: Deletar esta e parcelas futuras
  - [ ] Opção 3: Deletar todas as parcelas
- [ ] Testar cada opção e verificar resultado

### 4. Teste de Categorias (`/categorias`)

#### 4.1. Adicionar Categoria
- [ ] Clicar em "Nova Categoria"
- [ ] Preencher:
  - Nome: "Transporte"
  - Descrição: "Gastos com transporte"
- [ ] Adicionar categoria
- [ ] Verificar se aparece na lista

#### 4.2. Adicionar Subcategoria
- [ ] Selecionar uma categoria
- [ ] Clicar em "Nova Subcategoria"
- [ ] Preencher nome e descrição
- [ ] Adicionar subcategoria
- [ ] Verificar se aparece na lista da categoria

#### 4.3. Deletar Categoria/Subcategoria
- [ ] Deletar uma subcategoria
- [ ] Deletar uma categoria (verificar se subcategorias são removidas)

### 5. Teste de Tipos de Pagamento (`/tipos-pagamento`)

#### 5.1. Adicionar Tipo de Pagamento
- [ ] Clicar em "Novo Tipo de Pagamento"
- [ ] Preencher nome e descrição
- [ ] Adicionar tipo
- [ ] Verificar se aparece na lista

#### 5.2. Alternar Status (Ativo/Inativo)
- [ ] Clicar no botão de alternar status
- [ ] Verificar se o status muda
- [ ] Verificar se tipos inativos não aparecem no formulário de despesas

#### 5.3. Deletar Tipo de Pagamento
- [ ] Tentar deletar tipo que está em uso → Deve mostrar erro
- [ ] Deletar tipo que não está em uso → Deve funcionar

### 6. Teste de Relatórios (`/relatorios`)

#### 6.1. Relatório Sem Filtros
- [ ] Acessar página de relatórios
- [ ] Clicar em "Gerar Relatório" sem filtros
- [ ] Verificar se os dados aparecem corretamente
- [ ] Verificar totais de receitas e despesas
- [ ] Verificar saldo atual

#### 6.2. Relatório com Filtros
- [ ] Selecionar categoria específica
- [ ] Selecionar período (data início e fim)
- [ ] Selecionar tipo de pagamento
- [ ] Gerar relatório
- [ ] Verificar se os dados filtrados estão corretos

#### 6.3. Validações de Filtros
- [ ] Tentar usar data inválida → Deve mostrar erro
- [ ] Tentar usar data fim anterior à data início → Verificar comportamento

#### 6.4. Gerar PDF
- [ ] Clicar em "Gerar PDF"
- [ ] Verificar se o PDF é baixado
- [ ] Abrir o PDF e verificar:
  - [ ] Título e filtros aplicados
  - [ ] Tabelas de receitas e despesas
  - [ ] Totais corretos
  - [ ] Formatação adequada

### 7. Teste de API (Endpoints)

#### 7.1. Testar Endpoints via Navegador/Postman

**GET `/api/relatorios/resumo`**
```
http://localhost:5000/api/relatorios/resumo
```
- [ ] Retorna JSON com dados do resumo

**GET `/api/relatorios/resumo?categoria=Alimentação&data_inicio=2025-01-01&data_fim=2025-01-31`**
- [ ] Retorna dados filtrados corretamente

**GET `/api/subcategorias/1`** (onde 1 é um ID de categoria)
- [ ] Retorna lista de subcategorias da categoria

**GET `/api/tipos-pagamento`**
- [ ] Retorna lista de tipos de pagamento ativos

#### 7.2. Testar POST (Adicionar dados)

**POST `/api/receita`**
```json
{
  "descricao": "Teste API",
  "valor": 100.00,
  "data": "2025-01-20",
  "categoria": "Salário"
}
```
- [ ] Retorna sucesso
- [ ] Verificar se receita foi criada

**POST `/api/despesa`**
```json
{
  "descricao": "Teste API Despesa",
  "valor": 50.00,
  "data": "2025-01-20",
  "categoria": "Alimentação",
  "parcelas": 1
}
```
- [ ] Retorna sucesso
- [ ] Verificar se despesa foi criada

---

## 🤖 Testes Automatizados

### Teste 1: Verificar Rotas
```bash
# Em um terminal, inicie o servidor
python app.py

# Em outro terminal, execute:
python testar_rotas.py
```

**Resultado esperado:**
- Todas as rotas devem retornar status 200

### Teste 2: Verificar Categorias
```bash
# Com o servidor rodando, execute:
python testar_categorias.py
```

**Resultado esperado:**
- Categorias devem aparecer no select

### Teste 3: Verificar Banco de Dados
```bash
python verificar_banco.py
```

**Resultado esperado:**
- Banco de dados deve estar acessível
- Tabelas devem existir

---

## ✅ Checklist de Funcionalidades

### Funcionalidades Básicas
- [ ] Sistema inicia sem erros
- [ ] Páginas carregam corretamente
- [ ] Navegação entre páginas funciona
- [ ] Banco de dados é criado automaticamente

### CRUD Receitas
- [ ] Criar receita
- [ ] Listar receitas
- [ ] Deletar receita
- [ ] Validações funcionam

### CRUD Despesas
- [ ] Criar despesa simples
- [ ] Criar despesa parcelada
- [ ] Listar despesas
- [ ] Deletar despesa (simples e parcelada)
- [ ] Validações funcionam

### Categorias e Subcategorias
- [ ] Criar categoria
- [ ] Criar subcategoria
- [ ] Listar categorias/subcategorias
- [ ] Deletar categoria/subcategoria
- [ ] Subcategorias aparecem no formulário de despesas

### Tipos de Pagamento
- [ ] Criar tipo de pagamento
- [ ] Listar tipos de pagamento
- [ ] Alternar status (ativo/inativo)
- [ ] Deletar tipo de pagamento
- [ ] Validação: não deletar tipo em uso

### Relatórios
- [ ] Gerar relatório sem filtros
- [ ] Gerar relatório com filtros
- [ ] Filtros por categoria
- [ ] Filtros por período
- [ ] Filtros por tipo de pagamento
- [ ] Gerar PDF
- [ ] Validações de datas

### Validações e Segurança
- [ ] Validação de campos obrigatórios
- [ ] Validação de valores (positivos, não zero)
- [ ] Validação de datas
- [ ] Validação de número de parcelas
- [ ] Tratamento de erros adequado
- [ ] Mensagens de erro claras

### Interface
- [ ] Design responsivo
- [ ] Modais funcionam
- [ ] Mensagens de sucesso/erro aparecem
- [ ] Tabelas exibem dados corretamente
- [ ] Formulários limpam após submit

---

## 🐛 Problemas Comuns e Soluções

### Erro: "Porta 5000 já está em uso"
**Solução:** Altere a porta no `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erro: "ModuleNotFoundError"
**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "Database is locked"
**Solução:** Feche outras conexões com o banco ou reinicie o servidor

### Erro: "Template not found"
**Solução:** Verifique se está executando o `app.py` na pasta raiz do projeto

---

## 📊 Testes de Performance (Opcional)

### Teste com Muitos Dados
1. Adicione 100 receitas
2. Adicione 100 despesas
3. Verifique se:
   - [ ] Páginas carregam em tempo razoável (< 2 segundos)
   - [ ] Relatórios geram corretamente
   - [ ] PDFs são gerados sem erros

### Teste de Parcelas
1. Adicione uma despesa com 12 parcelas
2. Verifique se:
   - [ ] Todas as 12 parcelas são criadas
   - [ ] Datas estão corretas (mensais)
   - [ ] Valores estão corretos
   - [ ] Última parcela tem ajuste de arredondamento

---

## 📝 Notas Finais

- Sempre teste em um ambiente limpo primeiro
- Use dados de teste realistas
- Verifique o console do navegador (F12) para erros JavaScript
- Verifique os logs do servidor para erros Python
- Teste em diferentes navegadores (Chrome, Firefox, Edge)

---

**Última atualização:** Janeiro 2025

