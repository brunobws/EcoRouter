# EcoRouter

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Google Maps](https://img.shields.io/badge/Google%20Maps-APIs-yellow?logo=googlemaps&logoColor=white)](https://developers.google.com/maps)
[![HTML5](https://img.shields.io/badge/HTML5-%3E%3D5-orange?logo=html5&logoColor=white)](https://developer.mozilla.org/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-%3E%3D3-blue?logo=css3&logoColor=white)](https://developer.mozilla.org/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript&logoColor=black)](https://developer.mozilla.org/docs/Web/JavaScript)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple?logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

Calculador de rotas ecológicas com EcoScore v4 — identifica a rota mais eficiente em emissões e combustível.

Visão curta: uma aplicação Flask que consulta o Google Maps, calcula um EcoScore para cada rota e retorna a rota "ECO" com estimativas de economia de CO₂, combustível e custo.

---

## Instalação rápida

- Clone o repositório:

```powershell
git clone https://github.com/brunobws/EcoRouter.git
cd "EcoRouter - Copia"
```

- Crie e ative um ambiente virtual (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

- Instale as dependências:

```powershell
pip install -r requirements.txt
```

---

## Configuração

- Crie um arquivo `.env` com sua chave do Google Maps API:

```
GOOGLE_MAPS_API_KEY=SEU_KEY_AQUI
```

- Verifique se ativou as APIs necessárias no Google Cloud Console: Directions, Geocoding, Places e (opcional) Elevation.

---

## Uso rápido

- Execute a aplicação:

```powershell
python app.py
```

- Abra `http://127.0.0.1:5000` e preencha Origem, Destino e Frequência semanal. Clique em "Calcular".

---

## Estrutura mínima do projeto

- `app.py` — backend Flask e lógica do EcoScore
- `ECOSCORE_V4_DOCUMENTATION.md` — documentação técnica do algoritmo
- `templates/index.html` — frontend
- `static/` — `script.js` e `style.css`
- `requirements.txt` — dependências

---

## Sugestões rápidas para melhorar o README e a documentação EcoScore

- Deixe o `README.md` objetivo: instalação, configuração da API, comando de execução e link para a documentação técnica `ECOSCORE_V4_DOCUMENTATION.md`.
- No `ECOSCORE_V4_DOCUMENTATION.md`, adicione um sumário (TOC), exemplos de entrada/saída (JSON), pseudocódigo/fluxograma e exemplos numéricos curtos.
- Documente endpoints (ex.: `POST /calculate`) com exemplos de payloads e respostas.
- Inclua um tópico "Como contribuir" e instruções para executar testes (se houver).
- Adicione um CHANGELOG simples e um arquivo LICENSE se ainda não existir.

---

## Contribuição

- Fork → branch → commit → PR. Abra uma issue para discutir mudanças maiores.

---

## Licença

MIT (ver arquivo `LICENSE` se existir).

---

## Autor

Bruno Silva — https://github.com/brunobws

---

Para detalhes técnicos completos do EcoScore, veja `ECOSCORE_V4_DOCUMENTATION.md`.
|--------|-----------|

---

## Saiba mais sobre o EcoScore

- Para entender a metodologia completa do EcoScore (fórmulas, pesos, exemplos), acesse o arquivo de documentação técnica:

	- `ECOSCORE_V4_DOCUMENTATION.md` (documentação completa do EcoScore v4)

---

## Tecnologias e funcionalidades

- Tecnologias (ícones representativos):
	- 🐍 `Python` — lógica do backend e cálculos
	- ⚗️ `Flask` — servidor web e endpoints
	- 🌐 `Google Maps APIs` — Directions, Geocoding, Places (Autocomplete) e opcional Elevation
	- 💻 `HTML/CSS/JavaScript` — interface do usuário
	- 🎨 `Bootstrap` — estilos e responsividade
	- 📦 `requests` / `python-dotenv` — chamadas HTTP e configuração por `.env`

- Funcionalidades principais:
	- 🌿 Cálculo do EcoScore v4 para múltiplas rotas
	- 🗺️ Visualização de rotas no mapa e polyline da rota ECO
	- 🔁 Comparação entre rota padrão e rota ECO (distância, tempo, emissões)
	- 📈 Estimativa anual de economia de CO₂, combustível e custo
	- 🔎 Autocomplete de endereços (Places API)
	- ⚙️ Instalação automatizada via `setup.py`

---

## Instalação (recomendada)

O projeto inclui um script de setup automático: `setup.py`. Ele cria um `venv`, instala as dependências do `requirements.txt` e cria um arquivo `.env` de exemplo.

- Para usar o instalador automático:

```powershell
# No PowerShell (Windows)
python setup.py
# ou, de forma explícita:
python setup.py
```

- O que o `setup.py` faz (verificado no arquivo `setup.py` do repositório):
	- Detecta a versão do Python.
	- Cria o diretório `venv` se não existir.
	- Instala as dependências usando o `pip` do `venv`.
	- Cria um `.env` com um placeholder para `GOOGLE_MAPS_API_KEY` se não existir.

- Se preferir instalar manualmente, os passos equivalentes são:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Configuração

- Crie/edite o arquivo `.env` com sua chave do Google Maps API:

```
GOOGLE_MAPS_API_KEY=SEU_KEY_AQUI
```

- As APIs recomendadas no Google Cloud Console: `Directions API`, `Geocoding API`, `Places API` (Autocomplete) e `Maps Embed API`. Para obter informações de elevação (opcional), habilite `Elevation API`.

---

## Uso rápido

- Execute a aplicação:

```powershell
python app.py
```

- Abra `http://127.0.0.1:5000`, preencha Origem, Destino e Frequência semanal e clique em "Calcular".

---

## Créditos

- Desenvolvido por: **Bruno William da Silva**
- Finalidade: Projeto pessoal e trabalho acadêmico para a faculdade **FACENS - Sorocaba**

---

## Contato

Se tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato:

- **Nome:** Bruno William da Silva
- **Email:** brun0ws@outlook.com
- **LinkedIn:** Bruno William da Silva

---

## Contribuição

- Fork → branch → commit → PR. Abra uma issue para discutir mudanças maiores.

---

## Licença

MIT (ver arquivo `LICENSE` se existir).

---

Para detalhes técnicos completos do EcoScore, veja `ECOSCORE_V4_DOCUMENTATION.md`.

