# 🌱 EcoRouter v2.0

**Calculadora inteligente de rotas ecológicas com análise de velocidade e economia de CO₂**

Um aplicativo web que compara múltiplas rotas, seleciona automaticamente a opção mais sustentável baseada em padrões de velocidade, e calcula economia de CO₂, combustível e dinheiro. Inclui visualização em mapa interativo e navegação integrada com Google Maps.

---

## ✨ Funcionalidades

### 🧠 Seleção Inteligente de Rotas
- **Análise de Velocidade Média**: Compara múltiplas alternativas disponíveis
- **Rota Eco Automática**: Escolhe a com velocidade constante (menos paradas)
- **15% Menos Emissões**: Velocidade constante = consumo menor

### 💚 Cálculo de Economia (Anual)
- 📉 **CO₂ Economizado**: Em kg/ano
- 🌳 **Equivalência**: Quantas árvores plantadas
- 🚗 **Km Poupados**: Quilômetros economizados
- 💰 **Dinheiro Salvo**: Em reais de combustível

### 🗺️ Experiência do Usuário
- 🗺️ **Mapa Interativo**: Embed do Google Maps em tempo real
- 🧭 **Botão "Seguir Rota"**: Abre navegação no Google Maps
- 🔍 **Autocomplete**: Sugestões enquanto digita
- 📱 **Responsivo**: Desktop e mobile

---

## 🚀 Instalação

### 1. Clonar Repositório
```bash
git clone https://github.com/brunobws/EcoRouter.git
cd EcoRouter
```

### 2. Criar e Ativar Ambiente Virtual
```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar Google Maps API

1. Vá para [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto novo
3. Ative estas APIs:
   - Google Maps Geocoding API
   - Google Maps Directions API
   - Google Places API
   - Google Maps Embed API
4. Crie uma chave API (restrição a HTTP referrer)
5. Copie sua chave

### 5. Configurar .env
```
GOOGLE_MAPS_API_KEY=sua_chave_aqui
```

### 6. Executar
```bash
python app.py
```
Abra: **http://127.0.0.1:5000**

---

## 📖 Como Usar

1. **Digite Origem**: Endereço de partida
2. **Digite Destino**: Endereço de chegada
3. **Frequência**: Vezes por semana que faz o trajeto (1-7)
4. **Clique "Calcular"**: Aguarde análise
5. **Veja Resultados**:
   - Comparação de distâncias e tempos
   - Economia de CO₂ calculada
   - Equivalência em árvores
   - Mapa com a rota eco
6. **Clique "Seguir Rota"**: Abre Google Maps para navegação

---

## 🔧 Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Flask 2.3.3 (Python) |
| Frontend | HTML5, CSS3, JavaScript (ES6+) |
| Estilo | Bootstrap 5, Font Awesome 6 |
| APIs | Google Maps (4 serviços) |

---

## 📊 Fórmulas de Cálculo

### Seleção de Rota
```
velocidade_media = distancia_total / tempo_total (em horas)
rota_eco = rota com menor velocidade média
```
**Por quê?** Menor velocidade = menos paradas = consumo constante

### Emissões de CO₂
```
CO₂_padrao = distancia_padrao × 0.115 kg/km × frequencia × 52 semanas
CO₂_eco    = distancia_eco × 0.098 kg/km × frequencia × 52 semanas
economia   = CO₂_padrao - CO₂_eco
```
**15% de redução** vem da velocidade constante (menos aceleração)

### Equivalências
```
arvores      = economia_co2 / 21 kg (1 árvore absorve 21 kg CO₂/ano)
km_poupados  = diferenca_distancia × frequencia × 52
dinheiro     = km_poupados × (combustível/km) × preço_litro
```

---

## 📁 Estrutura do Projeto

```
EcoRouter/
├── app.py                    # Backend Flask
├── requirements.txt          # Dependências Python
├── setup.py                  # Setup do projeto
├── .env                      # Variáveis de ambiente
├── .gitignore                # Git config
├── README.md                 # Este arquivo
├── templates/
│   └── index.html            # Frontend
├── static/
│   ├── script.js             # JavaScript
│   └── style.css             # CSS
└── venv/                     # Ambiente virtual (ignorado no Git)
```

---

## 🔐 Segurança

- ✅ Chave API no `.env` (nunca commitada no Git)
- ✅ `.gitignore` protege `venv/` e `.env`
- ✅ Requisições para Google Maps pelo backend
- ✅ Nenhum dado sensível no frontend

---

## 🐛 Resolução de Problemas

### "ModuleNotFoundError: No module named 'flask'"
**Solução**: Ativar venv e instalar dependências
```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Erro 403 - Geocoding API not enabled"
**Solução**: Ativar Google Maps Geocoding API no Cloud Console

### "Mapa não aparece"
**Solução**: Verificar se chave API tem Google Maps Embed API ativada

### "Autocomplete não funciona"
**Solução**: Ativar Google Places API no Cloud Console

---

## 🚀 Deployment

### Heroku
```bash
git push heroku main
```

### Vercel + Backend Separado
Separar frontend (Vercel) e backend (Railway/Render)

### Docker
```bash
docker build -t ecorouter .
docker run -p 5000:5000 ecorouter
```

---

## 📝 Histórico de Mudanças

### v2.0 (Atual)
- ✅ Integração completa com Google Maps APIs
- ✅ Seleção inteligente baseada em velocidade média
- ✅ Cálculo de emissões com 15% eco factor
- ✅ Mapa embed interativo
- ✅ Botão "Seguir Rota" com Google Maps
- ✅ Geocodificação Google Maps
- ✅ Autocomplete de endereços

### v1.0
- OpenRouteService (descontinuado)
- Comparação básica de rotas
- Sem mapa interativo

---

## 🤝 Contribuir

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/MinhaFeature`)
3. Commit mudanças (`git commit -m 'Add MinhaFeature'`)
4. Push (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

MIT License - Veja LICENSE para detalhes

---

## 👤 Autor

**Bruno Silva** - [GitHub](https://github.com/brunobws)

---

## ❓ FAQ

### Por que precisa de um ambiente virtual do Python?

**Ambiente virtual = pasta isolada com Python e pacotes específicos do projeto**

#### 🎯 Por quês:

1. **Isolamento de Dependências**
   - Seu PC pode ter Python 3.8, 3.9, 3.10, etc
   - Cada projeto pode precisar de versões diferentes
   - Venv cria um Python isolado para EcoRouter
   - Não afeta outros projetos

2. **Evitar Conflitos**
   - Projeto A precisa: Flask 2.0
   - Projeto B precisa: Flask 3.0
   - Sem venv: conflito!
   - Com venv: cada um em sua bolha

3. **Reproduzibilidade**
   - requirements.txt lista versões exatas
   - Outro dev faz `pip install -r requirements.txt`
   - Instala EXATAMENTE as mesmas versões
   - Projeto funciona igual em todos os PCs

4. **Limpeza**
   - Instalar globalmente: `pip install flask` (contamina seu PC)
   - Instalar em venv: `pip install flask` (só nesta pasta)
   - Deletar projeto: `rm -rf venv/` (limpa tudo)

5. **Deployement**
   - Heroku/Railway/Docker usam requirements.txt
   - Criam um venv no servidor
   - Instalam dependências
   - Seu projeto roda exatamente como local

#### 📊 Exemplo Visual:
```
Sem venv (❌ BAD):
  Seu PC
  ├── Python 3.10 (global)
  ├── Flask 2.3.3
  ├── Requests 2.31.0
  ├── ... 50 pacotes instalados globalmente
  └── Tudo misturado!

Com venv (✅ GOOD):
  Seu PC
  └── Python 3.10 (global)
  
  EcoRouter/
  └── venv/
      ├── Python 3.10 (cópia isolada)
      ├── Flask 2.3.3
      ├── Requests 2.31.0
      └── Tudo limpo e isolado!
```

#### 🔧 Comandos:
```powershell
# Criar
python -m venv venv

# Ativar
.\venv\Scripts\Activate.ps1

# Desativar
deactivate
```

#### ✨ Boa Prática:
- ✅ SEMPRE usar venv para projetos Python
- ✅ Adicionar `venv/` no `.gitignore`
- ✅ Usar `requirements.txt` para documentar dependências
- ✅ Ativar venv antes de trabalhar no projeto

---

## 📞 Suporte

Dúvidas? Abra uma [Issue](https://github.com/brunobws/EcoRouter/issues)

