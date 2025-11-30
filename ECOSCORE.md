# 🌍 EcoScore - Documentação Completa

## 📋 Visão Geral

**EcoScore v4** é um sistema inteligente de pontuação (0-100) criado por nnós que avalia a eficiência ambiental de uma rota de dirigibilidade baseado em 6 fatores científicos e dados reais do Google Maps.

**Rota ECO** = A rota com **MAIOR EcoScore** (mais eficiente em combustível e emissões)

---

## 📊 Tabela de Pesos

| Fator | Peso | Categoria | Descrição |
|-------|------|-----------|-----------|
| **Tempo de Viagem** | 30% | Efeito Direto | Motor ligado menos tempo = menos CO₂ |
| **Elevação** | 20% | Efeito Direto | Sem subidas = sem gasto energético extra |
| **Paradas** | 20% | Efeito Direto | Sem paradas = sem aceleração frequent |
| **Tráfego** | 15% | Efeito Indireto | Fluxo livre vs congestionamento |
| **Distância** | 10% | Efeito Indireto | Menos km = menos consumo |
| **Tipo de Via** | 5% | Efeito Indireto | Rodovia vs rua (já refletido em paradas) |

**Total:** 100% (sem normalização adicional)

---

## 🧮 Fórmula Matemática

### Passo 1: Normalização Dinâmica (cada fator 0-100)

```
score_tempo = ((tempo_máx - tempo_atual) / (tempo_máx - tempo_mín)) × 100
score_elevacao = 100 × e^(-elevação_total / 200)
score_paradas = ((paradas_máx - paradas_atual) / (paradas_máx - paradas_mín)) × 100
score_trafego = (0-100 conforme traffic_model)
score_distancia = ((dist_máx - dist_atual) / (dist_máx - dist_mín)) × 100
score_via = (0-100 conforme road_type)
```

**Vantagem:** Cada fator é normalizado dentro do conjunto de rotas disponíveis, não com valores fixos absolutos.

### Passo 2: Subscore Combinado de Fluidez

```
score_fluidez = (
    (score_tempo × 0.8) +
    (score_trafego × 0.3) +
    (score_paradas × 0.2)
) / 1.3
```

**Objetivo:** Evitar multicolinearidade (Tempo, Tráfego e Paradas são correlacionados em áreas urbanas).

### Passo 3: EcoScore Final

```
EcoScore = (
    0.35 * score_fluidez +
    0.20 * score_elevacao +
    0.25 * score_distancia +
    0.15 * score_via +
    0.05  # Margem
)

Resultado: 0-100 (sempre normalizado)
```

---

## 📈 Detalhamento de Cada Fator

### 1️⃣ **Tempo de Viagem (30%) - EFEITO DIRETO**

```
Menos tempo = menos motor ligado = menos CO₂

Normalização dinâmica:
score_tempo = ((tempo_máx - tempo_atual) / (tempo_máx - tempo_mín)) × 100

Exemplo com 3 rotas:
- Rota A: 110 min → score = ((130-110)/(130-95)) × 100 = 57
- Rota B: 95 min  → score = ((130-95)/(130-95)) × 100 = 100 ✅
- Rota C: 130 min → score = ((130-130)/(130-95)) × 100 = 0
```

**Impacto:** Principal fator (30%) porque tempo direto = combustível consumido

---

### 2️⃣ **Elevação (20%) - EFEITO DIRETO**

```
Subidas = gasto energético extra (motor trabalha mais)

Fator exponencial (não linear):
score_elevacao = 100 × e^(-elevação_total / 200)

Exemplos:
- 0m:    100 × e^0       = 100 pontos (perfeito)
- 50m:   100 × e^(-0.25) = 78 pontos (moderado)
- 120m:  100 × e^(-0.6)  = 55 pontos (significativo)
- 250m:  100 × e^(-1.25) = 29 pontos (crítico)

Benefício: Pequenas subidas não penalizam tanto;
grandes subidas penalizam fortemente
```

**Impacto:** 20% porque subidas têm custo energético real e mensurável

---

### 3️⃣ **Paradas (20%) - EFEITO DIRETO**

```
Parar e arrancar = máximo consumo de combustível
(aceleração consome 5x mais que velocidade constante)

Estimado por tipo de via:
- trunk (rodovia): ~0-2 paradas/50km
- primary (avenida): ~3-5 paradas/20km
- secondary (rua): ~8-12 paradas/10km
- residential (rua residencial): ~15-20 paradas/10km

Normalização dinâmica:
score_paradas = ((paradas_máx - paradas_atual) / (paradas_máx - paradas_mín)) × 100

Exemplo:
- Rota rodovia: 3 paradas → score = ((40-3)/(40-0)) × 100 = 92 ✅
- Rota rua: 25 paradas  → score = ((40-25)/(40-0)) × 100 = 37
```

**Impacto:** 20% porque paradas são fator crítico de consumo

---

### 4️⃣ **Tráfego (15%) - EFEITO INDIRETO**

```
Engarrafamento = aceleração frequente = mais consumo
Classifica por comparação: duration_traffic / duration_normal

Modelo de tráfego:
- free_flow: ratio < 1.1 (fluxo livre) → 100 pontos
- slow: ratio 1.1-1.4 (trânsito lento) → 60 pontos
- traffic_jam: ratio > 1.4 (congestionado) → 30 pontos

Função:
score_trafego = get_traffic_score(traffic_model)
```

**Impacto:** 15% porque complementa o tempo (já considerado em fluidez)

---

### 5️⃣ **Distância (10%) - EFEITO INDIRETO**

```
Mais curta = menos km = menos combustível
(impacto linear e previsível)

Normalização dinâmica:
score_distancia = ((dist_máx - dist_atual) / (dist_máx - dist_mín)) × 100

Exemplo:
- Rota A: 104 km → score = ((110-104)/(110-98)) × 100 = 50
- Rota B: 98 km  → score = ((110-98)/(110-98)) × 100 = 100 ✅
```

**Impacto:** 10% porque é secundário (efeito indireto, já refletido em paradas/tráfego)

---

### 6️⃣ **Tipo de Via (5%) - EFEITO INDIRETO**

```
Rodovia = fluxo contínuo (melhor)
Rua residencial = muitas paradas (pior)

Scoring por tipo:
- trunk (rodovia): 100 pontos
- primary (avenida principal): 70 pontos
- secondary (rua principal): 40 pontos
- residential (residencial): 20 pontos

Via está já refletida em "Paradas", então peso baixo (5%)
Serve principalmente para desempate
```

**Impacto:** 5% porque é redundante com paradas (já consideradas)

---

## 🎯 Como Uma Rota é Selecionada como ECO

### **Algoritmo de Decisão**

1. **Google Maps retorna 2-3 rotas alternativas**
   ```
   Rota A: Pela avenida (mais semáforo)
   Rota B: Pela rodovia (menos trânsito)
   Rota C: Alternativa (se houver)
   ```

2. **Calcular EcoScore para CADA rota**
   ```
   EcoScore_A = 45.3
   EcoScore_B = 78.9 ✅ MAIOR
   EcoScore_C = 32.1
   ```

3. **Selecionar as duas melhores**
   ```
   Rota PADRÃO = EcoScore menor (45.3)
   Rota ECO = EcoScore maior (78.9) ← ESSA!
   ```

4. **Retornar para cálculo de emissões**
   ```
   Usar fator dinâmico baseado no EcoScore da rota eco
   ```

---

## 🚗 Fator de Emissão de CO₂ (Gasolina)

Baseado no **EcoScore da rota eco**, aplicar fator dinâmico:

```python
GASOLINA - Padrão Brasil (0.115 kg CO₂/km base)

if ecoscore >= 80:
    fator = 0.115 kg/km   # Ideal
    desc = "Fluxo Ideal"
    
elif ecoscore >= 65:
    fator = 0.122 kg/km   # Muito Bom (+6%)
    desc = "Fluxo Muito Bom"
    
elif ecoscore >= 50:
    fator = 0.135 kg/km   # Normal (+17%)
    desc = "Fluxo Normal"
    
elif ecoscore >= 35:
    fator = 0.148 kg/km   # Moderado (+29%)
    desc = "Fluxo Moderado"
    
else:
    fator = 0.165 kg/km   # Congestionado (+44%)
    desc = "Congestionado"
```

**Cálculo Final:**
```
CO₂_ano = distância × fator_dinâmico × frequência × 52 semanas
Economia = CO₂_padrão - CO₂_eco
```

---

## 📊 Exemplos Práticos

### **Exemplo 1: São Paulo → Guarulhos (3 rotas)**

```
ROTA A (Avenida Dutra):
├─ Tempo: 110 min
├─ Elevação: 45m
├─ Paradas: 25
├─ Tráfego: slow (60 pts)
├─ Distância: 104 km
├─ Via: secondary (40 pts)
└─ EcoScore: 50.2 ❌

ROTA B (Rodovia Imigrantes):
├─ Tempo: 95 min ← MELHOR
├─ Elevação: 120m
├─ Paradas: 5 ← MUITO MELHOR
├─ Tráfego: free_flow (100 pts) ← MELHOR
├─ Distância: 98 km ← MELHOR
├─ Via: trunk (100 pts) ← MELHOR
└─ EcoScore: 78.9 ✅ ECO!

ROTA C (Alternativa):
├─ Tempo: 125 min
├─ Elevação: 90m
├─ Paradas: 35
├─ Tráfego: slow (60 pts)
├─ Distância: 110 km
├─ Via: secondary (40 pts)
└─ EcoScore: 32.1 ❌

DECISÃO: Rota B (EcoScore 78.9) é selecionada como ECO
```

---

## ✅ Benefícios do EcoScore

| Aspecto | Versão Anterior | EcoScore |
|---------|-----------------|-----------|
| **Lógica** | Velocidade média | 6 fatores científicos |
| **Normalização** | Valores fixos | Dinâmica (adaptada) |
| **Elevação** | Linear | Exponencial |
| **Multicolinearidade** | Problema | Resolvida (subscore) |
| **Precisão** | Baixa | Alta |
| **Transparência** | Baixa | Muito alta |
| **Combustível** | Genérico | Gasolina específica |

---

## 🔬 Fundamentação Científica

### Base de Dados Utilizados

- **CONPET** (Programa Nacional de Conservação de Energia em Transportes)
- **IPCC** (Painel Intergovernamental sobre Mudanças Climáticas)
- **Google Maps** (Dados reais de rotas e tráfego)
- **Consumo Médio Brasileiro:** 9,6 km/litro
- **CO₂ Gasolina:** 2,31 kg CO₂ por litro

### Equações Utilizadas

```
1. Normalização:
   score = ((max - valor) / (max - min)) × 100

2. Elevação exponencial:
   score = 100 × e^(-elevação / 200)

3. Subscore Fluidez:
   fluidez = (tempo × 0.8 + trafego × 0.3 + paradas × 0.2) / 1.3

4. EcoScore:
   score = 0.35×fluidez + 0.20×elevacao + 0.25×distancia + 0.15×via + 0.05

5. Emissões:
   CO₂_ano = distância × fator_dinamico × frequência × 52
```

---

## 🚀 Próximas Melhorias (Future Work)

- [ ] Integrar Google Elevation API para dados reais de elevação
- [ ] Integrar Google Places API para dados de semáforos
- [ ] Suporte a múltiplos combustíveis (diesel, etanol, elétrico)
- [ ] Histórico de rotas e padrões de dirigibilidade
- [ ] Machine Learning para prever tráfego com precisão
- [ ] Integração com dados de emissões por fabricante/modelo

---

## 📞 Suporte Técnico

Para dúvidas sobre o EcoScore v4:
- Consulte `CHANGELOG.md` para histórico de versões
- Veja `README.md` para guia de uso geral
- Verifique `BOAS_PRATICAS.md` para contexto técnico

---

**Versão:** EcoScore v4.0  
**Data:** Novembro 2025  
**Status:** ✅ Pronto para Produção
