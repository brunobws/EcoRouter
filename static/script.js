async function calculateRoute() {
            const origin = document.getElementById('origin').value.trim();
            const destination = document.getElementById('destination').value.trim();
            const frequency = document.getElementById('frequency').value;
            const errorDiv = document.getElementById('error-message');
            const resultsDiv = document.getElementById('results');
            const calculateBtn = document.getElementById('calculateBtn');

            // Limpar mensagens anteriores
            errorDiv.style.display = 'none';
            resultsDiv.style.display = 'none';

            // Validação básica
            if (!origin || !destination || !frequency) {
                errorDiv.textContent = 'Por favor, preencha todos os campos.';
                errorDiv.style.display = 'block';
                return;
            }

            // Mostrar loading
            calculateBtn.disabled = true;
            calculateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculando...';

            try {
                // Fazer requisição para o backend
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        origin: origin,
                        destination: destination,
                        frequency: parseInt(frequency)
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Erro ao calcular rota');
                }

                // Preencher resultados
                document.getElementById('distanceEco').textContent = data.distance_eco;
                document.getElementById('distanceStandard').textContent = data.distance_standard;
                document.getElementById('savingsAmount').textContent = data.emissions.savings + ' kg de CO₂';
                document.getElementById('treesEquivalent').textContent = data.emissions.trees_equivalent;
                document.getElementById('kmCarEquivalent').textContent = data.emissions.km_car_equivalent;
                document.getElementById('impactMessage').textContent = data.impact_message;

                // Mostrar resultados
                resultsDiv.style.display = 'block';
                
                // Scroll suave para os resultados
                resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });

            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            } finally {
                // Restaurar botão
                calculateBtn.disabled = false;
                calculateBtn.innerHTML = '🌿 Calcular Rota Ecológica';
            }
        }

        // Permitir Enter para calcular
        document.addEventListener('DOMContentLoaded', function() {
            const inputs = document.querySelectorAll('.form-control');
            inputs.forEach(input => {
                input.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        calculateRoute();
                    }
                });
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

        