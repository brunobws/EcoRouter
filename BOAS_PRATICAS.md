# 📚 Boas Práticas - Estrutura de Projeto Python

## 🎯 Por Que Essa Estrutura?

### 1️⃣ Ambiente Virtual (venv/)

**O que é**: Uma pasta isolada com Python + pacotes específicos do seu projeto

**Por que precisa**:
```
Sem venv:
  Seu PC → Python 3.10 (global)
    ├── Flask 2.0 (Projeto A precisa)
    ├── Flask 3.0 (Projeto B precisa)
    ├── Django 2.1
    ├── ... 50 pacotes misturados
    → CONFLITO! Qual Flask usar?

Com venv (✅):
  Seu PC → Python 3.10 (global)
  
  EcoRouter/ → venv/ → Python 3.10 (cópia)
    ├── Flask 2.3.3 (isolado)
    ├── requests 2.31.0 (isolado)
    └── ... tudo limpo!
  
  OutroProjeto/ → venv/ → Python 3.10 (outra cópia)
    ├── Flask 3.0 (sem conflito)
    └── ... limpo também!
```

**Benefícios**:
- ✅ Evita conflitos entre projetos
- ✅ Reproduzibilidade: mesmo ambiente para todos
- ✅ Fácil atualizar sem quebrar outros projetos
- ✅ Deploy: servidor cria seu próprio venv

**Como usar**:
```powershell
# Criar (uma vez)
python -m venv venv

# Ativar (toda vez que trabalhar)
.\venv\Scripts\Activate.ps1

# Verificar (deve aparecer "(venv)" no terminal)
# (venv) PS C:\...\EcoRouter>

# Desativar
deactivate
```

**NO GITIGNORE** (nunca commitar):
```
venv/
__pycache__/
*.pyc
```

---

### 2️⃣ requirements.txt

**O que é**: Lista de dependências com versões exatas

**Por que precisa**:
```
Seu PC (Dev):
  pip install Flask
  → Instala Flask 2.3.3 (versão atual)
  
Servidor de Prod:
  pip install Flask
  → Instala Flask 2.5.0 (nova versão!)
  → App quebra porque código esperava 2.3.3
  
COM requirements.txt:
  pip install -r requirements.txt
  → Instala EXATAMENTE Flask 2.3.3
  → App funciona igual em todo lugar
```

**Formato**:
```
Flask==2.3.3
requests==2.31.0
python-dotenv==1.0.0
Werkzeug==2.3.7
```

**Quando atualizar**:
```powershell
# Toda vez que instalar novo pacote
pip freeze > requirements.txt
```

---

### 3️⃣ .env (Arquivo de Configuração)

**O que é**: Variáveis sensíveis (não commitadas no Git)

**Por que precisa**:
```
ERRADO (❌):
app.py contém:
  API_KEY = "AIzaSyDOfhpMIiqWQvCrNeNpLXVLcU8TqoAR37c"
  → Commitado no GitHub público
  → Qualquer um pode usar sua chave
  → Sua conta fica comprometida

CERTO (✅):
app.py contém:
  API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
  
.env contém:
  GOOGLE_MAPS_API_KEY=sua_chave_aqui
  
.gitignore contém:
  .env
  → Arquivo .env NUNCA é commitado
  → Chave continua privada
```

**Exemplo .env**:
```
GOOGLE_MAPS_API_KEY=AIzaSyDOfhpMIiqWQvCrNeNpLXVLcU8TqoAR37c
FLASK_ENV=development
DEBUG=True
```

**Como usar em Python**:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega .env

api_key = os.getenv("GOOGLE_MAPS_API_KEY")
flask_env = os.getenv("FLASK_ENV", "production")  # default value
```

---

### 4️⃣ .gitignore

**O que é**: Diz ao Git quais arquivos NUNCA commitar

**Por que precisa**:
```
Sem .gitignore:
  .env (chave API exposta) ❌
  venv/ (3GB de dependências) ❌
  __pycache__/ (cache Python) ❌
  .pyc (compilados) ❌
  
Com .gitignore:
  Automaticamente ignored ✅
  Repo fica 100x menor ✅
```

**Essencial para Python**:
```
# Ambiente virtual
venv/
env/
.venv/

# Compilados
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/

# Variáveis sensíveis
.env
.env.local
secrets.txt

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Sistema
.DS_Store
Thumbs.db
```

---

### 5️⃣ setup.py

**O que é**: Script para instalar seu projeto como pacote

**Por que precisa**:
```
Sem setup.py:
  Outro dev precisa:
  1. Clone seu repo
  2. Crie venv manualmente
  3. pip install -r requirements.txt
  4. Configure variáveis
  5. Rode app.py
  → Manual, confuso, propenso a erros

Com setup.py:
  pip install -e .
  → Instala seu projeto + deps automaticamente
  → Profissional
```

**Exemplo setup.py**:
```python
from setuptools import setup

setup(
    name="ecorouter",
    version="2.0.0",
    description="Calculadora inteligente de rotas ecológicas",
    author="Bruno Silva",
    author_email="bruno@example.com",
    url="https://github.com/brunobws/EcoRouter",
    install_requires=[
        "Flask==2.3.3",
        "requests==2.31.0",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.8",
)
```

---

### 6️⃣ README.md

**O que é**: Documentação principal do projeto

**Por que precisa**:
```
Sem README:
  Outro dev vê seu repo no GitHub
  → "O que é isso?"
  → "Como instalo?"
  → "Como uso?"
  → Abandona o projeto

Com README (✅):
  Escreve no README:
  - O que é o projeto
  - Como instalar (passo a passo)
  - Como usar (exemplos)
  - Tecnologias
  - Licença
  → Dev consegue usar em 5 minutos
```

**Essencial incluir**:
- 📝 Descrição clara
- 🚀 Instalação passo-a-passo
- 📖 Como usar
- 🔧 Tecnologias
- 📄 Licença
- 👤 Autor

---

### 7️⃣ CHANGELOG.md

**O que é**: Histórico de mudanças do projeto

**Por que precisa**:
```
Usuário vê v2.0 vs v1.0
→ "O que mudou?"
→ CHANGELOG.md responde:
  - Bugs corrigidos
  - Novas features
  - Mudanças técnicas
  - Compatibilidade
```

**Formato (Keep a Changelog)**:
```markdown
## [2.0.0] - 2025-11-10
### Added
- Seleção inteligente de rotas

### Fixed
- Geocoding agora usa Google Maps

### Changed
- Emissões agora usam 15% eco factor

## [1.0.0] - 2025-10-01
### Added
- Versão inicial
```

---

## 📁 Estrutura Profissional Completa

```
meu-projeto/
│
├── README.md                    ← Documentação (obrigatório)
├── CHANGELOG.md                 ← Histórico (recomendado)
├── setup.py                     ← Setup script (recomendado)
├── requirements.txt             ← Dependências (obrigatório)
├── .gitignore                   ← Git config (obrigatório)
├── .env                         ← Variáveis privadas (NEVER commit)
│
├── src/ ou app.py               ← Código principal
│   ├── __init__.py
│   ├── app.py                   ← Flask app
│   └── config.py                ← Configurações
│
├── templates/                   ← HTML
│   └── index.html
│
├── static/                      ← CSS, JS, imagens
│   ├── css/
│   ├── js/
│   └── images/
│
├── tests/                       ← Testes (recomendado)
│   └── test_app.py
│
├── venv/                        ← Ambiente virtual (IGNORE)
│
└── .git/                        ← Controle versão (git init)
```

---

## 🚀 Workflow Profissional

### Inicio do Projeto (primeira vez)
```powershell
1. mkdir meu-projeto
2. cd meu-projeto
3. python -m venv venv              # Criar venv
4. .\venv\Scripts\Activate.ps1      # Ativar
5. pip install flask requests       # Instalar deps
6. pip freeze > requirements.txt    # Gerar lista
7. echo "venv/" > .gitignore        # Criar .gitignore
8. echo "CHAVE_API=..." > .env      # Criar .env
9. echo ".env" >> .gitignore        # Adicionar .env ao ignore
10. git init                         # Iniciar Git
11. git add .                        # Adicionar tudo (menos ignored)
12. git commit -m "Initial commit"  # Primeiro commit
```

### Trabalhar no Projeto (rotina)
```powershell
1. .\venv\Scripts\Activate.ps1      # Ativar venv (SIM, toda vez!)
2. python app.py                    # Rodar
3. Fazer mudanças no código
4. git add .                        # Stage mudanças
5. git commit -m "description"      # Commit
6. git push origin main             # Push
```

### Instalar Novo Pacote
```powershell
1. pip install novo-pacote          # Instalar
2. pip freeze > requirements.txt    # Atualizar lista
3. git add requirements.txt
4. git commit -m "Add novo-pacote"
5. git push
```

### Compartilhar Projeto
```
Outro dev clona seu repo:
1. git clone seu-repo
2. cd seu-repo
3. python -m venv venv
4. .\venv\Scripts\Activate.ps1
5. pip install -r requirements.txt
6. Pedir .env (não vem no Git)
7. python app.py
→ Tudo funciona igual ao seu PC
```

---

## ✅ Checklist - Antes de Publicar no GitHub

- [ ] `README.md` completo
- [ ] `requirements.txt` atualizado
- [ ] `setup.py` (se aplicável)
- [ ] `.gitignore` com venv, .env, __pycache__
- [ ] `.env` criado mas NÃO commitado
- [ ] `CHANGELOG.md` com histórico
- [ ] Sem arquivos temporários (`.pyc`, `__pycache__/`)
- [ ] Código comentado nos pontos complexos
- [ ] Testes funcionando
- [ ] Documentação clara
- [ ] Licença definida (MIT, Apache, GPL, etc)
- [ ] Autor/contribuidores listados

---

## 🎯 EcoRouter - Aplicando Boas Práticas

### ✅ Já Implementado
- ✅ `venv/` para isolamento
- ✅ `requirements.txt` com versões exatas
- ✅ `.env` para Google Maps API key
- ✅ `.gitignore` protegendo sensíveis
- ✅ `setup.py` para instalação
- ✅ `README.md` completo
- ✅ `CHANGELOG.md` documentando v2.0

### 📁 Estrutura Final
```
EcoRouter/
├── README.md                ← Documentação principal ✨
├── CHANGELOG.md             ← Histórico de mudanças ✨
├── MUDANCAS_CODIGO.md       ← Detalhes técnicos
├── setup.py                 ← Setup script
├── requirements.txt         ← Dependências exatas
├── .env                     ← Chave API (NÃO commitar)
├── .gitignore               ← Git rules
├── app.py                   ← Backend
├── templates/index.html     ← Frontend
├── static/                  ← CSS + JS
└── venv/                    ← Ambiente isolado
```

---

## 💡 Tips Finais

**Sempre**:
- ✅ Use venv para CADA projeto Python
- ✅ Atualize requirements.txt quando instalar novo pacote
- ✅ Nunca commite `.env`, `venv/`, `__pycache__/`
- ✅ Mantenha README atualizado
- ✅ Documente mudanças no CHANGELOG

**Nunca**:
- ❌ Instale pacotes globalmente para production
- ❌ Commite chaves API no Git
- ❌ Delete venv sem backup (reimplante depois)
- ❌ Esqueça de ativar venv
- ❌ Use diferentes Python versions entre dev/prod

---

**Essa estrutura = Profissionalismo = Código pronto para trabalho real**

