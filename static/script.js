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