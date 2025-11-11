"""
EcoRouter - Sistema de Rotas Ecológicas
Backend em Flask para cálculo de economia de CO₂
Integração com Google Maps APIs para rotas reais

EcoScore v4:
- Normalização dinâmica (adaptada ao conjunto de rotas)
- Fator exponencial para elevação
- Subscore combinado para evitar multicolinearidade
"""

from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import urllib3
import math

# Desabilitar aviso SSL (seguro para testes)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração da API OpenRouteService
ORS_API_KEY = os.getenv('ORS_API_KEY', '')
ORS_BASE_URL = "https://api.openrouteservice.org"
VERIFY_SSL = False  # Desabilitar SSL para testes

# Configuração da API Google Maps
GOOGLE_MAPS_API_KEY = 'AIzaSyDOfhpMIiqWQvCrNeNpLXVLcU8TqoAR37c'

def geocode_address(address):
    """
    Geocodifica endereço usando Google Maps Geocoding API
    
    Args:
        address (str): Endereço para geocodificar
        
    Returns:
        dict: Coordenadas lat/lng ou None se falhar
    """
    if not GOOGLE_MAPS_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY não configurada")
    
    try:
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            'address': address,
            'key': GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10, verify=VERIFY_SSL)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'OK' or not data.get('results'):
            raise ValueError(f"Endereço não encontrado: {address}")
        
        location = data['results'][0]['geometry']['location']
        formatted_address = data['results'][0]['formatted_address']
        
        return {
            'lat': location['lat'],
            'lng': location['lng'],
            'address': formatted_address
        }
    
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao geocodificar {address}: {str(e)}")

def calculate_ecoscore(route, all_routes_data):
    """
    Calcula EcoScore v4 para uma rota (0-100)
    
    EcoScore v4 = 0.35 * fluidez + 0.20 * elevacao + 0.25 * distancia + 0.15 * via + 0.05
    
    Args:
        route: Dados da rota do Google Maps
        all_routes_data: Lista com dados de todas as rotas (para normalização dinâmica)
        
    Returns:
        dict: EcoScore e scores individuais
    """
    
    # Extrair dados da rota
    summary = route['legs'][0]
    distance_km = summary['distance']['value'] / 1000
    duration_min = summary['duration']['value'] / 60
    duration_in_traffic_min = summary.get('duration_in_traffic', {}).get('value', summary['duration']['value']) / 60
    
    # Estimar elevação (aproximadamente por latitude/longitude) - usar 0 por agora
    # Em produção, usar Google Elevation API
    elevation_gain = 0  # TODO: Integrar com Google Elevation API
    
    # Estimar paradas por tipo de via (placeholder)
    estimated_stops = estimate_stops(route)
    
    # Obter tipo de tráfego
    traffic_model = classify_traffic(duration_min, duration_in_traffic_min)
    
    # Obter tipo de via (aproximação)
    road_type = get_dominant_road_type(route)
    
    # PASSO 1: Normalizar cada fator dinamicamente (0-100)
    score_tempo = normalize_factor(
        duration_min,
        [r['duration_min'] for r in all_routes_data],
        descending=True  # Menos tempo = melhor (invertido)
    )
    
    score_elevacao = 100 * math.exp(-elevation_gain / 200)
    
    score_paradas = normalize_factor(
        estimated_stops,
        [r['estimated_stops'] for r in all_routes_data],
        descending=True
    )
    
    score_trafego = get_traffic_score(traffic_model)
    
    score_distancia = normalize_factor(
        distance_km,
        [r['distance_km'] for r in all_routes_data],
        descending=True
    )
    
    score_via = get_road_type_score(road_type)
    
    # PASSO 2: Calcular subscore de Fluidez
    # Fluidez = (Tempo × 0.8 + Tráfego × 0.3 + Paradas × 0.2) / 1.3
    score_fluidez = (
        (score_tempo * 0.8) +
        (score_trafego * 0.3) +
        (score_paradas * 0.2)
    ) / 1.3
    
    # PASSO 3: Calcular EcoScore Final
    ecoscore = (
        (0.35 * score_fluidez) +
        (0.20 * score_elevacao) +
        (0.25 * score_distancia) +
        (0.15 * score_via) +
        0.05  # Margem/reserva
    )
    
    return {
        'ecoscore': round(min(ecoscore, 100), 1),  # Limitar a 100
        'score_tempo': round(score_tempo, 1),
        'score_elevacao': round(score_elevacao, 1),
        'score_paradas': round(score_paradas, 1),
        'score_trafego': round(score_trafego, 1),
        'score_distancia': round(score_distancia, 1),
        'score_via': round(score_via, 1),
        'score_fluidez': round(score_fluidez, 1),
        'distance_km': round(distance_km, 2),
        'duration_min': round(duration_min, 1),
        'elevation_gain': elevation_gain,
        'estimated_stops': estimated_stops,
        'traffic_model': traffic_model,
        'road_type': road_type
    }

def normalize_factor(value, all_values, descending=False):
    """
    Normaliza um fator para escala 0-100 (dinâmica)
    
    score = ((max - value) / (max - min)) × 100  (se descending)
    score = ((value - min) / (max - min)) × 100  (se ascending)
    
    Args:
        value: Valor atual
        all_values: Lista de todos os valores (para encontrar min/max)
        descending: True se valor menor = melhor (ex: tempo)
        
    Returns:
        float: Score 0-100
    """
    if not all_values or len(all_values) < 2:
        return 50  # Default se só tem 1 rota
    
    min_val = min(all_values)
    max_val = max(all_values)
    
    # Evitar divisão por zero
    if min_val == max_val:
        return 50
    
    if descending:
        # Valor menor = score maior
        score = ((max_val - value) / (max_val - min_val)) * 100
    else:
        # Valor maior = score maior
        score = ((value - min_val) / (max_val - min_val)) * 100
    
    return max(0, min(100, score))  # Limitar entre 0-100

def estimate_stops(route):
    """
    Estima número de paradas baseado na rota
    
    Args:
        route: Dados da rota
        
    Returns:
        int: Número estimado de paradas
    """
    # Aproximação: usar número de steps da rota
    # Em produção, usar dados de semáforos do Google
    total_steps = sum(len(leg.get('steps', [])) for leg in route.get('legs', []))
    
    # Estimar: ~1 parada por 2-3 steps em cidade
    estimated = total_steps // 2 if total_steps > 0 else 0
    
    return max(0, estimated)

def classify_traffic(duration_normal, duration_traffic):
    """
    Classifica tráfego comparando duração normal vs com tráfego
    
    Args:
        duration_normal: Duração em condições normais
        duration_traffic: Duração com tráfego atual
        
    Returns:
        str: 'free_flow', 'slow', ou 'traffic_jam'
    """
    if duration_traffic is None:
        duration_traffic = duration_normal
    
    ratio = duration_traffic / duration_normal if duration_normal > 0 else 1
    
    if ratio < 1.1:
        return 'free_flow'
    elif ratio < 1.4:
        return 'slow'
    else:
        return 'traffic_jam'

def get_dominant_road_type(route):
    """
    Obtém o tipo de via dominante da rota
    
    Args:
        route: Dados da rota
        
    Returns:
        str: Tipo de via ('trunk', 'primary', 'secondary', etc)
    """
    # Buscar nas properties da rota (se disponível)
    # Por enquanto, retornar padrão
    # Em produção, analisar os segments da rota
    return 'secondary'

def get_traffic_score(traffic_model):
    """
    Retorna score baseado em modelo de tráfego
    
    Args:
        traffic_model: 'free_flow', 'slow', ou 'traffic_jam'
        
    Returns:
        float: Score 0-100
    """
    scores = {
        'free_flow': 100,
        'slow': 60,
        'traffic_jam': 30
    }
    return scores.get(traffic_model, 50)

def get_road_type_score(road_type):
    """
    Retorna score baseado em tipo de via
    
    Args:
        road_type: Tipo de via do Google Maps
        
    Returns:
        float: Score 0-100
    """
    scores = {
        'trunk': 100,        # Rodovia federal/estadual
        'primary': 70,       # Avenida principal
        'secondary': 40,     # Rua principal
        'residential': 20    # Residencial
    }
    return scores.get(road_type, 50)

def analyze_routes(data):
    """
    Analisa múltiplas rotas usando EcoScore v4
    
    Retorna a rota com MAIOR EcoScore como eco
    
    Args:
        data: Response do Google Maps Directions API
        
    Returns:
        tuple: (rota_padrão, rota_eco, análise_dict)
    """
    routes = data.get('routes', [])
    if not routes:
        raise ValueError("Nenhuma rota encontrada")
    
    # Se tiver apenas uma rota, usar a mesma para ambas
    if len(routes) == 1:
        route = routes[0]
        analysis = {
            'strategy': 'single_route',
            'message': 'Apenas uma rota disponível',
            'ecoscore_eco': 50,
            'ecoscore_std': 50
        }
        return route, route, analysis
    
    # Preparar dados para normalização
    routes_data = []
    for route in routes:
        summary = route['legs'][0]
        routes_data.append({
            'distance_km': summary['distance']['value'] / 1000,
            'duration_min': summary['duration']['value'] / 60,
            'estimated_stops': estimate_stops(route),
            'route': route
        })
    
    # Calcular EcoScore para cada rota
    ecoscore_results = []
    for route_data in routes_data:
        score = calculate_ecoscore(route_data['route'], routes_data)
        ecoscore_results.append({
            'route': route_data['route'],
            'ecoscore': score['ecoscore'],
            'details': score
        })
    
    # Ordenar por EcoScore (maior = melhor)
    ecoscore_results.sort(key=lambda x: x['ecoscore'], reverse=True)
    
    eco_result = ecoscore_results[0]      # Maior EcoScore
    std_result = ecoscore_results[-1]     # Menor EcoScore
    
    analysis = {
        'strategy': 'ecoscore_v4',
        'ecoscore_eco': eco_result['ecoscore'],
        'ecoscore_std': std_result['ecoscore'],
        'ecoscore_difference': round(eco_result['ecoscore'] - std_result['ecoscore'], 1),
        'message': f"EcoScore Eco: {eco_result['ecoscore']} | EcoScore Padrão: {std_result['ecoscore']} ({eco_result['ecoscore'] - std_result['ecoscore']:.0f}% melhor)",
        'eco_details': eco_result['details'],
        'std_details': std_result['details']
    }
    
    return std_result['route'], eco_result['route'], analysis

def get_route(origin_coords, dest_coords):
    """
    Obtém múltiplas rotas usando Google Maps Directions API
    Calcula EcoScore v4 para cada uma e retorna ambas
    
    Args:
        origin_coords: Dict com lat/lng da origem
        dest_coords: Dict com lat/lng do destino
        
    Returns:
        dict: Dados das rotas (padrão e eco)
    """
    if not GOOGLE_MAPS_API_KEY:
        raise ValueError("GOOGLE_MAPS_API_KEY não configurada")
    
    try:
        url = "https://maps.googleapis.com/maps/api/directions/json"
        
        origin = f"{origin_coords['lat']},{origin_coords['lng']}"
        destination = f"{dest_coords['lat']},{dest_coords['lng']}"
        
        params = {
            'origin': origin,
            'destination': destination,
            'mode': 'driving',
            'key': GOOGLE_MAPS_API_KEY,
            'alternatives': 'true'  # Retornar rotas alternativas
        }
        
        response = requests.get(url, params=params, timeout=10, verify=VERIFY_SSL)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'OK':
            raise ValueError(f"Google Maps API error: {data.get('status')}")
        
        # Usar EcoScore v4 para selecionar rotas
        std_route, eco_route, analysis = analyze_routes(data)
        
        std_summary = std_route['legs'][0]
        eco_summary = eco_route['legs'][0]
        
        return {
            'distance_standard': std_summary['distance']['value'] / 1000,
            'distance_eco': eco_summary['distance']['value'] / 1000,
            'duration_standard': std_summary['duration']['value'] / 60,
            'duration_eco': eco_summary['duration']['value'] / 60,
            'analysis': analysis,
            'polyline': eco_route.get('overview_polyline', {}).get('points', '')
        }
    
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Erro ao calcular rota: {str(e)}")

def calculate_emissions(distance_standard, distance_eco, ecoscore_eco, frequency):
    """
    Calcula emissões de CO₂ usando gasolina como combustível padrão
    
    Fator de emissão dinâmico baseado em EcoScore:
    - EcoScore ≥ 80: 0.115 kg/km (Fluxo Ideal)
    - EcoScore 65-79: 0.122 kg/km (Fluxo Muito Bom)
    - EcoScore 50-64: 0.135 kg/km (Fluxo Normal)
    - EcoScore 35-49: 0.148 kg/km (Fluxo Moderado)
    - EcoScore < 35: 0.165 kg/km (Congestionado)
    
    Args:
        distance_standard: Distância da rota padrão em km
        distance_eco: Distância da rota eco em km
        ecoscore_eco: EcoScore da rota eco
        frequency: Frequência semanal de deslocamento
        
    Returns:
        dict: Dados de emissões e economia
    """
    
    # COMBUSTÍVEL: GASOLINA (0.115 kg CO₂/km base)
    EMISSION_FACTOR_BASE = 0.115  # kg CO₂/km (fluxo ideal)
    FUEL_CONSUMPTION_PER_KM = 1 / 9.6  # Litros por km (9,6 km/litro)
    FUEL_PRICE = 6.50  # R$/litro
    
    # Determinar fator de emissão baseado em EcoScore
    if ecoscore_eco >= 80:
        emission_factor_eco = 0.115  # Ideal
    elif ecoscore_eco >= 65:
        emission_factor_eco = 0.122  # Muito Bom
    elif ecoscore_eco >= 50:
        emission_factor_eco = 0.135  # Normal
    elif ecoscore_eco >= 35:
        emission_factor_eco = 0.148  # Moderado
    else:
        emission_factor_eco = 0.165  # Congestionado
    
    # Fator padrão é sempre o máximo (pior caso)
    emission_factor_standard = 0.165  # kg CO₂/km (congestionado)
    
    # Cálculo anual (52 semanas)
    total_standard = distance_standard * emission_factor_standard * frequency * 52
    total_eco = distance_eco * emission_factor_eco * frequency * 52
    savings = total_standard - total_eco
    
    # Dados adicionais
    distance_diff = distance_standard - distance_eco
    fuel_saved = distance_diff * FUEL_CONSUMPTION_PER_KM * frequency * 52
    money_saved = fuel_saved * FUEL_PRICE
    
    # Comparações educativas
    trees_equivalent = round(savings / 21) if savings > 0 else 0  # ~21kg CO₂/árvore/ano
    km_car_equivalent = round(savings / emission_factor_standard) if savings > 0 else 0
    
    return {
        'total_standard': round(total_standard, 2),
        'total_eco': round(total_eco, 2),
        'savings': round(max(savings, 0), 2),
        'trees_equivalent': max(trees_equivalent, 0),
        'km_car_equivalent': max(km_car_equivalent, 0),
        'fuel_saved': round(max(fuel_saved, 0), 2),
        'money_saved': round(max(money_saved, 0), 2),
        'emission_factor_standard': emission_factor_standard,
        'emission_factor_eco': emission_factor_eco,
        'fuel_consumption_rate': round(FUEL_CONSUMPTION_PER_KM, 4)
    }

def get_impact_message(savings):
    """
    Retorna mensagem motivacional baseada na economia
    
    Args:
        savings: Economia de CO₂ em kg
        
    Returns:
        str: Mensagem motivacional
    """
    if savings > 500:
        return "Impacto extraordinário! Você é um verdadeiro herói ambiental! 🌟"
    elif savings > 200:
        return "Excelente contribuição para o planeta! 🌍"
    elif savings > 50:
        return "Ótima escolha! Cada quilograma conta! 🌱"
    else:
        return "Pequenas ações fazem grande diferença! 💚"

@app.route('/')
def index():
    """Página inicial do EcoRouter"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Endpoint para calcular rota ecológica usando EcoScore v4
    Usa APIs reais do Google Maps
    
    Returns:
        JSON com dados da rota, EcoScore e economia
    """
    try:
        # Receber dados do formulário
        data = request.get_json()
        origin = data.get('origin', '').strip()
        destination = data.get('destination', '').strip()
        frequency = int(data.get('frequency', 0))
        
        # Validações
        if not origin or not destination:
            return jsonify({'error': 'Por favor, preencha origem e destino'}), 400
        
        if frequency < 1 or frequency > 7:
            return jsonify({'error': 'Frequência deve ser entre 1 e 7 vezes por semana'}), 400
        
        # Geocodificar endereços
        origin_coords = geocode_address(origin)
        dest_coords = geocode_address(destination)
        
        # Obter rotas do Google Maps
        route_data = get_route(origin_coords, dest_coords)
        
        distance_standard = route_data['distance_standard']
        distance_eco = route_data['distance_eco']
        
        # Extrair análise com EcoScore
        analysis = route_data['analysis']
        ecoscore_eco = analysis['ecoscore_eco']
        
        # Calcular emissões com EcoScore dinâmico
        emissions = calculate_emissions(
            distance_standard,
            distance_eco,
            ecoscore_eco,
            frequency
        )
        
        # Mensagem de impacto
        impact_message = get_impact_message(emissions['savings'])
        
        # Preparar resposta
        result = {
            'origin': origin_coords.get('address', origin),
            'destination': dest_coords.get('address', destination),
            'origin_coords': {'lat': origin_coords['lat'], 'lng': origin_coords['lng']},
            'dest_coords': {'lat': dest_coords['lat'], 'lng': dest_coords['lng']},
            'distance_standard': round(distance_standard, 2),
            'distance_eco': round(distance_eco, 2),
            'duration_standard': round(route_data['duration_standard'], 0),
            'duration_eco': round(route_data['duration_eco'], 0),
            'frequency': frequency,
            'emissions': emissions,
            'impact_message': impact_message,
            'eco_polyline': route_data.get('polyline', ''),
            'analysis_message': analysis.get('message', ''),
            'ecoscore': {
                'eco': analysis['ecoscore_eco'],
                'standard': analysis['ecoscore_std'],
                'difference': analysis['ecoscore_difference'],
                'eco_details': analysis['eco_details']
            }
        }
        
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro ao calcular rota: {str(e)}'}), 500

if __name__ == '__main__':
    # Rodar servidor Flask em modo debug
    print("\n" + "="*60)
    print("🌍 EcoRouter - Sistema de Rotas Ecológicas")
    print("="*60)
    print("🚀 Servidor rodando em: http://127.0.0.1:5000")
    print("💚 Pressione Ctrl+C para parar o servidor")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)