"""
EcoRouter - Sistema de Rotas Ecológicas
Backend em Flask para cálculo de economia de CO₂
"""

from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

def geocode_address(address):
    """
    Simula geocodificação de endereço
    Em produção, usar Google Maps Geocoding API ou OpenRouteService
    
    Args:
        address (str): Endereço para geocodificar
        
    Returns:
        dict: Coordenadas lat/lng
    """
    # Hash simples para simular coordenadas baseadas no endereço
    hash_value = sum(ord(c) for c in address)
    lat = -23.5 + (hash_value % 100) / 1000
    lng = -46.6 + (hash_value % 200) / 1000
    
    return {'lat': lat, 'lng': lng}

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calcula distância entre dois pontos usando a fórmula de Haversine
    
    Args:
        lat1, lon1: Coordenadas do ponto 1
        lat2, lon2: Coordenadas do ponto 2
        
    Returns:
        float: Distância em quilômetros
    """
    R = 6371  # Raio da Terra em km
    
    # Converter para radianos
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Fórmula de Haversine
    a = (math.sin(delta_lat / 2) ** 2 + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * 
         math.sin(delta_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance

def calculate_emissions(distance_standard, distance_eco, frequency):
    """
    Calcula emissões e economia de CO₂
    
    Args:
        distance_standard: Distância da rota padrão em km
        distance_eco: Distância da rota ecológica em km
        frequency: Frequência semanal de deslocamento
        
    Returns:
        dict: Dados de emissões e economia
    """
    # Fatores de emissão (kg CO₂ por km)
    EMISSION_STANDARD = 0.120  # Rota padrão com trânsito
    EMISSION_ECO = 0.095       # Rota eco com velocidade constante
    
    # Cálculo anual (52 semanas)
    total_standard = distance_standard * EMISSION_STANDARD * frequency * 52
    total_eco = distance_eco * EMISSION_ECO * frequency * 52
    savings = total_standard - total_eco
    
    # Comparações educativas
    trees_equivalent = round(savings / 21)  # ~21kg CO₂/árvore/ano
    km_car_equivalent = round(savings / 0.120)  # km não dirigidos
    
    return {
        'total_standard': round(total_standard, 2),
        'total_eco': round(total_eco, 2),
        'savings': round(savings, 2),
        'trees_equivalent': trees_equivalent,
        'km_car_equivalent': km_car_equivalent
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
    Endpoint para calcular rota ecológica e economia de CO₂
    
    Returns:
        JSON com dados da rota e economia
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
        
        # Calcular distância da rota padrão
        distance_standard = calculate_distance(
            origin_coords['lat'], origin_coords['lng'],
            dest_coords['lat'], dest_coords['lng']
        )
        
        # Simular rota ecológica (8% maior, mas com menor emissão)
        distance_eco = distance_standard * 1.08
        
        # Calcular emissões
        emissions = calculate_emissions(distance_standard, distance_eco, frequency)
        
        # Mensagem de impacto
        impact_message = get_impact_message(emissions['savings'])
        
        # Preparar resposta
        result = {
            'origin': origin,
            'destination': destination,
            'origin_coords': origin_coords,
            'dest_coords': dest_coords,
            'distance_standard': round(distance_standard, 2),
            'distance_eco': round(distance_eco, 2),
            'frequency': frequency,
            'emissions': emissions,
            'impact_message': impact_message
        }
        
        return jsonify(result)
    
    except ValueError:
        return jsonify({'error': 'Frequência deve ser um número válido'}), 400
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