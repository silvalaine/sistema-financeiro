# Sistema Financeiro Doméstico

Um sistema web simples e eficiente para gerenciar receitas e despesas pessoais, desenvolvido em Python com Flask.

## 🚀 Funcionalidades

- **Receitas**: Cadastro e gerenciamento de receitas por categoria
- **Despesas**: Controle de gastos organizados por categoria
- **Relatórios**: Análise detalhada das finanças com resumos e estatísticas
- **Interface Web**: Interface moderna e responsiva
- **Banco de Dados**: Armazenamento local com SQLite

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se estiver usando git
   git clone <url-do-repositorio>
   cd sistema-financeiro
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**
   ```bash
   python app.py
   ```

4. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 📱 Como Usar

### Página Inicial
- Visualize um resumo das suas finanças
- Veja o saldo atual, total de receitas e despesas
- Acesse rapidamente as últimas transações

### Receitas
- Clique em "Nova Receita" para adicionar uma receita
- Preencha: descrição, valor, data e categoria
- Categorias disponíveis: Salário, Freelance, Investimentos, Vendas, Outros
- Visualize todas as receitas em uma tabela organizada
- Delete receitas clicando no ícone da lixeira

### Despesas
- Clique em "Nova Despesa" para adicionar uma despesa
- Preencha: descrição, valor, data e categoria
- Categorias disponíveis: Alimentação, Transporte, Moradia, Saúde, Educação, Lazer, Roupas, Outros
- Visualize todas as despesas em uma tabela organizada
- Delete despesas clicando no ícone da lixeira

### Relatórios
- Visualize análises detalhadas das suas finanças
- Veja totais por categoria
- Analise o saldo atual com recomendações
- Visualize as últimas transações

## 🗄️ Banco de Dados

O sistema usa SQLite como banco de dados local. O arquivo `sistema_financeiro.db` será criado automaticamente na primeira execução.

### Estrutura das Tabelas

**Receitas**
- id (chave primária)
- descricao (texto)
- valor (decimal)
- data (data)
- categoria (texto)
- created_at (timestamp)

**Despesas**
- id (chave primária)
- descricao (texto)
- valor (decimal)
- data (data)
- categoria (texto)
- created_at (timestamp)

## 🎨 Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Banco de Dados**: SQLite
- **Ícones**: Font Awesome

## 📁 Estrutura do Projeto

```
sistema-financeiro/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── receitas.html
│   ├── despesas.html
│   └── relatorios.html
├── static/               # Arquivos estáticos
│   ├── style.css
│   └── script.js
└── README.md             # Este arquivo
```

## 🔧 Personalização

### Adicionando Novas Categorias

Para adicionar novas categorias de receitas ou despesas, edite os arquivos HTML correspondentes:

- **Receitas**: `templates/receitas.html` (linha com as opções do select)
- **Despesas**: `templates/despesas.html` (linha com as opções do select)

### Modificando o Banco de Dados

Para adicionar novos campos ou tabelas, edite o arquivo `app.py` na seção dos modelos e execute novamente a aplicação.

## 🚨 Solução de Problemas

### Erro de Porta em Uso
Se a porta 5000 estiver em uso, modifique a última linha do `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude para outra porta
```

### Problemas com Dependências
Se houver problemas com as dependências, tente:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Banco de Dados Corrompido
Se o banco de dados estiver corrompido, delete o arquivo `sistema_financeiro.db` e execute novamente a aplicação.

## 📈 Próximas Funcionalidades

- [ ] Gráficos interativos
- [ ] Exportação de dados (CSV, PDF)
- [ ] Filtros por período
- [ ] Metas financeiras
- [ ] Backup automático
- [ ] Múltiplos usuários
- [ ] Aplicativo mobile

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório do projeto.

---

**Desenvolvido com ❤️ para facilitar o controle financeiro pessoal**
