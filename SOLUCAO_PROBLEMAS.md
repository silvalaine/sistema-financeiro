# 🔧 Solução de Problemas - Sistema Financeiro

## ❌ Problema: "URL não localizada" ou servidor não inicia

### Passo 1: Verificar se o servidor está rodando

Abra o **Prompt de Comando** ou **PowerShell** e execute:

```bash
cd "C:\Users\layne\Documents\Trabalho 2025\Elaine\Pessoal\Sistema Financeiro"
python app.py
```

**O que você deve ver:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

Se você ver isso, o servidor está rodando! ✅

---

### Passo 2: Se aparecer erro de porta ocupada

**Erro:** `Address already in use` ou `Port 5000 is already in use`

**Solução 1:** Feche outros processos usando a porta
```bash
# No PowerShell (como Administrador):
netstat -ano | findstr :5000
# Anote o PID (último número)
taskkill /PID <numero_do_pid> /F
```

**Solução 2:** Use outra porta
Edite o arquivo `app.py`, linha 504:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude para 5001
```

Depois acesse: `http://localhost:5001`

---

### Passo 3: Se aparecer erro de módulo não encontrado

**Erro:** `ModuleNotFoundError: No module named 'xxx'`

**Solução:** Instale as dependências
```bash
pip install -r requirements.txt
```

Ou instale manualmente:
```bash
pip install Flask Flask-SQLAlchemy Werkzeug python-dateutil reportlab
```

---

### Passo 4: Verificar se tudo está OK

Execute o diagnóstico:
```bash
python diagnostico.py
```

Todos os itens devem mostrar `[OK]`

---

### Passo 5: Testar o servidor

1. **Inicie o servidor:**
   ```bash
   python app.py
   ```

2. **Mantenha a janela do terminal aberta** (não feche!)

3. **Abra o navegador** e acesse:
   ```
   http://localhost:5000
   ```

4. **Se não funcionar**, tente:
   ```
   http://127.0.0.1:5000
   ```

---

## 🐛 Problemas Comuns

### Problema 1: "This site can't be reached"

**Causa:** O servidor não está rodando

**Solução:**
1. Verifique se você executou `python app.py`
2. Verifique se a janela do terminal está aberta
3. Verifique se não há erros no terminal

---

### Problema 2: Página em branco ou erro 404

**Causa:** Problema com templates ou rotas

**Solução:**
1. Verifique se a pasta `templates/` existe
2. Execute: `python diagnostico.py`
3. Verifique se todos os arquivos estão presentes

---

### Problema 3: Erro ao carregar CSS/JavaScript

**Causa:** Arquivos estáticos não encontrados

**Solução:**
1. Verifique se a pasta `static/` existe
2. Verifique se os arquivos `style.css` e `script.js` estão lá

---

### Problema 4: Erro de banco de dados

**Causa:** Banco de dados corrompido ou não criado

**Solução:**
1. Delete o arquivo `instance/sistema_financeiro.db` (se existir)
2. Execute novamente: `python app.py`
3. O banco será criado automaticamente

---

## 📋 Checklist Rápido

Antes de reportar problemas, verifique:

- [ ] Python 3.7+ está instalado (`python --version`)
- [ ] Dependências estão instaladas (`pip list`)
- [ ] Você está na pasta correta do projeto
- [ ] O servidor está rodando (janela do terminal aberta)
- [ ] A porta 5000 está disponível
- [ ] Não há erros no terminal

---

## 🆘 Ainda não funciona?

Execute estes comandos e envie a saída:

```bash
# 1. Verificar Python
python --version

# 2. Verificar dependências
pip list | findstr -i "flask sqlalchemy"

# 3. Executar diagnóstico
python diagnostico.py

# 4. Tentar iniciar servidor
python app.py
```

---

## ✅ Comandos Úteis

### Iniciar servidor
```bash
python app.py
```

### Verificar diagnóstico
```bash
python diagnostico.py
```

### Verificar rotas
```bash
python testar_rotas.py
```

### Limpar e recriar banco
```bash
python limpar_banco.py
```

---

## 📞 URLs do Sistema

Quando o servidor estiver rodando, acesse:

- **Página Inicial:** http://localhost:5000/
- **Receitas:** http://localhost:5000/receitas
- **Despesas:** http://localhost:5000/despesas
- **Relatórios:** http://localhost:5000/relatorios
- **Categorias:** http://localhost:5000/categorias
- **Tipos de Pagamento:** http://localhost:5000/tipos-pagamento

---

**Última atualização:** Janeiro 2025

