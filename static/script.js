// ============ Google Maps Setup ============
let map;
let originMarker;
let destinationMarker;
let originPlace;
let destinationPlace;
let originAutocomplete;
let destinationAutocomplete;

function initGoogleMaps() {
    // Coordenadas iniciais (Sorocaba, SP)
    const sorocaba = { lat: -23.5036, lng: -47.4578 };

    // Criar mapa invisível (necessário para Autocomplete funcionar)
    const mapContainer = document.createElement('div');
    mapContainer.style.display = 'none';
    document.body.appendChild(mapContainer);

    map = new google.maps.Map(mapContainer, {
        zoom: 13,
        center: sorocaba,
    });

    // Autocomplete para Origem
    originAutocomplete = new google.maps.places.Autocomplete(
        document.getElementById('originSearch'),
        { 
            componentRestrictions: { country: 'br' }, 
            fields: ['place_id', 'formatted_address', 'geometry'],
            types: ['establishment', 'geocode']
        }
    );
    originAutocomplete.bindTo('bounds', map);
    originAutocomplete.addListener('place_changed', onOriginPlaceChanged);

    // Autocomplete para Destino
    destinationAutocomplete = new google.maps.places.Autocomplete(
        document.getElementById('destinationSearch'),
        { 
            componentRestrictions: { country: 'br' }, 
            fields: ['place_id', 'formatted_address', 'geometry'],
            types: ['establishment', 'geocode']
        }
    );
    destinationAutocomplete.bindTo('bounds', map);
    destinationAutocomplete.addListener('place_changed', onDestinationPlaceChanged);
}

function onOriginPlaceChanged() {
    const place = originAutocomplete.getPlace();
    if (!place.geometry) {
        alert('Endereço não encontrado. Tente outro.');
        return;
    }
    setOriginPlace(place);
}

function onDestinationPlaceChanged() {
    const place = destinationAutocomplete.getPlace();
    if (!place.geometry) {
        alert('Endereço não encontrado. Tente outro.');
        return;
    }
    setDestinationPlace(place);
}

function setOriginPlace(place) {
    originPlace = place;
    document.getElementById('originStatus').textContent = '✓ Origem selecionada';
    updateSelectionStatus();
}

function setDestinationPlace(place) {
    destinationPlace = place;
    document.getElementById('destinationStatus').textContent = '✓ Destino selecionado';
    updateSelectionStatus();
}

function clearOrigin() {
    originPlace = null;
    document.getElementById('originSearch').value = '';
    document.getElementById('originStatus').textContent = '';
    updateSelectionStatus();
}

function clearDestination() {
    destinationPlace = null;
    document.getElementById('destinationSearch').value = '';
    document.getElementById('destinationStatus').textContent = '';
    updateSelectionStatus();
}

function updateSelectionStatus() {
    const statusDiv = document.getElementById('selectionStatus');
    const statusText = document.getElementById('statusText');
    
    if (originPlace && destinationPlace) {
        statusDiv.style.display = 'block';
        statusDiv.className = 'alert alert-success mb-3';
        statusText.innerHTML = '<i class="fas fa-check-circle"></i> ✓ Ambos os pontos selecionados! Defina a frequência e calcule.';
    } else if (originPlace) {
        statusDiv.style.display = 'block';
        statusDiv.className = 'alert alert-info mb-3';
        statusText.innerHTML = '<i class="fas fa-info-circle"></i> Agora selecione o destino';
    } else {
        statusDiv.style.display = 'block';
        statusDiv.className = 'alert alert-warning mb-3';
        statusText.innerHTML = '<i class="fas fa-map-marker-alt"></i> Selecione a origem';
    }
}

// ============ Variáveis Globais para Mapa ============
let currentRouteData = null;

// ============ Cálculo de Rota ============
async function calculateRoute() {
    const frequency = document.getElementById('frequency').value;
    const errorDiv = document.getElementById('error-message');
    const resultsDiv = document.getElementById('results');
    const calculateBtn = document.getElementById('calculateBtn');

    errorDiv.style.display = 'none';
    resultsDiv.style.display = 'none';

    // Validação
    if (!originPlace || !destinationPlace) {
        errorDiv.textContent = 'Por favor, selecione origem e destino no mapa.';
        errorDiv.style.display = 'block';
        return;
    }

    if (!frequency || frequency < 1 || frequency > 7) {
        errorDiv.textContent = 'Frequência deve ser entre 1 e 7 vezes por semana.';
        errorDiv.style.display = 'block';
        return;
    }

    calculateBtn.disabled = true;
    calculateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculando...';

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                origin: originPlace.formatted_address,
                destination: destinationPlace.formatted_address,
                frequency: parseInt(frequency)
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Erro ao calcular rota');
        }

        // Armazenar dados para uso posterior
        currentRouteData = data;

        // Preencher resultados
        document.getElementById('distanceEco').textContent = data.distance_eco;
        document.getElementById('distanceStandard').textContent = data.distance_standard;
        document.getElementById('durationEco').textContent = data.duration_eco;
        document.getElementById('durationStandard').textContent = data.duration_standard;
        document.getElementById('savingsAmount').textContent = data.emissions.savings + ' kg de CO₂';
        document.getElementById('treesEquivalent').textContent = data.emissions.trees_equivalent;
        document.getElementById('kmCarEquivalent').textContent = data.emissions.km_car_equivalent;
        document.getElementById('impactMessage').textContent = data.impact_message;
        document.getElementById('analysisMessage').textContent = data.analysis_message || '';

        // Preencher EcoScore resumido
        if (data.ecoscore) {
            document.getElementById('ecoscore-eco-value').textContent = data.ecoscore.eco;
            document.getElementById('ecoscore-std-value').textContent = data.ecoscore.standard;
            document.getElementById('ecoscore-diff-value').textContent = data.ecoscore.difference;
            document.getElementById('ecoscore-summary').style.display = 'block';
        }

        if (data.emissions.fuel_saved !== undefined) {
            const fuelDiv = document.getElementById('fuelSaved');
            if (fuelDiv) {
                fuelDiv.textContent = data.emissions.fuel_saved.toFixed(2);
            }
        }
        
        if (data.emissions.money_saved !== undefined) {
            const moneyDiv = document.getElementById('moneySaved');
            if (moneyDiv) {
                moneyDiv.textContent = 'R$ ' + data.emissions.money_saved.toFixed(2);
            }
        }

        // Gerar mapa embed
        generateMapEmbed(data);

        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.display = 'block';
    } finally {
        calculateBtn.disabled = false;
        calculateBtn.innerHTML = '🌿 Calcular Rota Ecológica';
    }
}

// ============ Geração do Mapa Embed ============
function generateMapEmbed(data) {
    // Cria um iframe do Google Maps mostrando a rota ecológica
    const origin = `${data.origin_coords.lat},${data.origin_coords.lng}`;
    const destination = `${data.dest_coords.lat},${data.dest_coords.lng}`;
    
    // URL do Google Maps Embed com a rota
    const mapsUrl = `https://www.google.com/maps/embed/v1/directions?key=AIzaSyDOfhpMIiqWQvCrNeNpLXVLcU8TqoAR37c&origin=${origin}&destination=${destination}&mode=driving`;
    
    const mapIframe = document.getElementById('mapIframe');
    mapIframe.src = mapsUrl;
}

// ============ Botão Seguir Rota ============
function followEcoRoute() {
    // Abre a rota ecológica no Google Maps para navegação
    if (!currentRouteData) {
        alert('Por favor, calcule uma rota primeiro!');
        return;
    }
    
    const origin = `${currentRouteData.origin_coords.lat},${currentRouteData.origin_coords.lng}`;
    const destination = `${currentRouteData.dest_coords.lat},${currentRouteData.dest_coords.lng}`;
    
    // URL para abrir no Google Maps (app ou web)
    const mapsUrl = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}&travelmode=driving`;
    
    window.open(mapsUrl, '_blank');
}

// Inicializar ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    initGoogleMaps();
    updateSelectionStatus();

    // Permitir Enter
    document.getElementById('frequency').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            calculateRoute();
        }
    });
});

// Função para abrir o modal de boas-vindas
function openWelcomeModal() {
    const modal = document.getElementById('welcomeModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// Função para fechar o modal
function closeWelcomeModal() {
    const modal = document.getElementById('welcomeModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
        // Removido o sessionStorage para aparecer sempre
    }
}

// Inicialização do modal
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('welcomeModal');
    
    if (!modal) {
        return;
    }
    
    // Mostrar modal sempre ao carregar a página
    setTimeout(() => {
        openWelcomeModal();
    }, 500);
    
    // Fechar ao clicar no overlay
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeWelcomeModal();
        }
    });
    
    // Fechar com tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeWelcomeModal();
        }
    });
});

// Função para abrir modal de cálculos
function openCalculationsModal() {
    const modal = document.getElementById('calculationsModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// Função para fechar modal de cálculos
function closeCalculationsModal() {
    const modal = document.getElementById('calculationsModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
    }
}

// Adicionar listeners para o modal de cálculos
document.addEventListener('DOMContentLoaded', function() {
    const calculationsModal = document.getElementById('calculationsModal');
    
    if (calculationsModal) {
        // Fechar ao clicar no overlay
        calculationsModal.addEventListener('click', function(e) {
            if (e.target === calculationsModal) {
                closeCalculationsModal();
            }
        });
        
        // Fechar com ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && calculationsModal.classList.contains('active')) {
                closeCalculationsModal();
            }
        });
    }
});

        