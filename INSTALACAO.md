# 📥 Guia de Instalação - EcoRouter

## ⚠️ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.11+** — [Download aqui](https://www.python.org/downloads/)
- **Git** — [Download aqui](https://git-scm.com/)
- Conta no **Google Cloud Platform** para obter a chave da API

---

## 🚀 Passo 1: Clonar o Repositório

Abra seu terminal/PowerShell e execute:

```bash
git clone https://github.com/brunobws/EcoRouter.git
cd EcoRouter
```

---

## 🔑 Passo 2: Configurar Chave do Google Maps

### 2.1 Obter a Chave

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto (se não tiver um)
3. Ative as seguintes APIs:
   - ✅ **Maps JavaScript API**
   - ✅ **Directions API**
   - ✅ **Places API**
   - ✅ **Geocoding API**
4. Crie uma chave de API (tipo "Chave de navegador")
5. Copie a chave

### 2.2 Configurar no Arquivo `.env`

Na raiz do projeto, crie um arquivo chamado `.env`:

```bash
# Windows (PowerShell)
echo "GOOGLE_MAPS_API_KEY=sua_chave_aqui" > .env

# Linux/Mac
echo "GOOGLE_MAPS_API_KEY=sua_chave_aqui" > .env
```

Ou edite o arquivo `.env` manualmente e adicione:

```
GOOGLE_MAPS_API_KEY=sua_chave_api_aqui
```

⚠️ **IMPORTANTE:** Nunca compartilhe sua chave de API! Adicione `.env` ao `.gitignore`

---

## 📦 Passo 3: Instalar Dependências

### Usando o Script de Setup

```bash
# Windows
python setup.py

# Linux/Mac
python3 setup.py
```

O script irá:
1. ✅ Criar um ambiente virtual (`venv`)
2. ✅ Instalar todas as dependências do `requirements.txt`
3. ✅ Verificar/criar arquivo `.env`


## ▶️ Passo 4: Executar a Aplicação

Com o ambiente virtual ativado, execute:

```bash
python app.py
```

Você verá algo como:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

---

## 🌐 Passo 5: Acessar no Navegador

Abra seu navegador e acesse:

```
http://localhost:5000
```

ou

```
http://127.0.0.1:5000
```

---

## ✅ Checklist de Configuração

- [ ] Python 3.11+ instalado
- [ ] Git instalado
- [ ] Repositório clonado
- [ ] Chave Google Maps obtida
- [ ] Arquivo `.env` criado com a chave
- [ ] Dependências instaladas
- [ ] Aplicação em execução em `http://localhost:5000`

---

## 🆘 Troubleshooting

### ❌ "Python não encontrado"
```bash
# Verifique a versão
python --version

# Se não funcionar, tente python3
python3 --version
```

### ❌ "Módulo flask não encontrado"
```bash
# Verifique se o venv está ativado
which python  # Linux/Mac
where python  # Windows (PowerShell)

# Se estiver fora do venv, ative:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### ❌ "Erro de chave API do Google Maps"
- Verifique se a chave está no arquivo `.env`
- Confirme que as APIs estão habilitadas no Google Cloud Console
- Tente regenerar a chave

### ❌ "Porta 5000 já está em uso"
```bash
# Mude a porta editando app.py:
# Altere: app.run(debug=True, port=5000)
# Para:  app.run(debug=True, port=5001)
```

---

## 📚 Próximos Passos

Depois de instalar com sucesso:

1. Leia [ECOSCORE.md](ECOSCORE.md) para entender a metodologia
2. Explore o código em `app.py`
3. Personalize as configurações conforme necessário
4. Contribua com melhorias! 🌿

---

## 💡 Dicas de Desenvolvimento

### Ativar o Modo Debug
O Flask já está em modo debug por padrão. Mudanças no código recarregam automaticamente.

### Instalar Novos Pacotes
```bash
pip install nome_do_pacote
pip freeze > requirements.txt  # Atualizar requirements.txt
```

### Desativar o Ambiente Virtual
```bash
deactivate
```

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique [README.md](README.md)
2. Consulte [ECOSCORE.md](ECOSCORE.md)
3. Abra uma issue no [GitHub](https://github.com/brunobws/EcoRouter/issues)
4. Entre em contato: [brun0ws@outlook.com](mailto:brun0ws@outlook.com)

---

**Versão:** 1.0  
**Última atualização:** Novembro 2025  
**Status:** ✅ Pronto para uso
