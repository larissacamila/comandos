/**
 * Configuração do checkout com Mercado Pago
 * Para app de mobilidade estilo Uber
 */

// ⚠️ SUBSTITUA PELA SUA PUBLIC KEY DO MERCADO PAGO ⚠️
// Você encontra em: Mercado Pago Developers > Sua Aplicação > Credenciais
const PUBLIC_KEY = 'TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx';

// URL do seu backend (ajuste conforme sua configuração)
const BACKEND_URL = 'http://localhost:8000';

// Inicializa o SDK do Mercado Pago
const mp = new MercadoPago(PUBLIC_KEY, {
    locale: 'pt-BR'
});

/**
 * Busca os dados da corrida do backend
 * Normalmente você receberia isso via parâmetro na URL (ex: ?ride_id=123)
 */
async function getRideData() {
    // Exemplo: buscar da URL ou de sessionStorage
    const urlParams = new URLSearchParams(window.location.search);
    const rideId = urlParams.get('ride_id');
    
    if (rideId) {
        try {
            const response = await fetch(`${BACKEND_URL}/api/ride/${rideId}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Erro ao buscar corrida:', error);
        }
    }
    
    // Dados de exemplo (substitua pelos dados reais da sua corrida)
    return {
        ride_id: 'RIDE-001',
        origin: 'Av. Paulista, 1000',
        destination: 'Av. Brigadeiro Faria Lima, 2000',
        passenger_name: 'João Silva',
        passenger_email: 'joao@email.com',
        amount: 45.90,
        date: new Date().toLocaleString('pt-BR')
    };
}

/**
 * Cria uma preferência de pagamento no backend
 * Essa preferência é necessária para o checkout
 */
async function createPreference(rideData) {
    try {
        const response = await fetch(`${BACKEND_URL}/api/create-preference`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ride_id: rideData.ride_id,
                amount: rideData.amount,
                passenger_name: rideData.passenger_name,
                passenger_email: rideData.passenger_email,
                description: `Corrida de ${rideData.origin} para ${rideData.destination}`
            })
        });
        
        if (!response.ok) {
            throw new Error('Erro ao criar preferência');
        }
        
        const data = await response.json();
        return data.preference_id;
    } catch (error) {
        console.error('Erro ao criar preferência:', error);
        throw error;
    }
}

/**
 * Renderiza o botão de pagamento do Mercado Pago
 */
async function renderPaymentButton(preferenceId) {
    const bricksBuilder = mp.bricks();
    
    try {
        await bricksBuilder.create('wallet', 'walletBrick_container', {
            initialization: {
                preferenceId: preferenceId
            },
            customization: {
                texts: {
                    action: 'pay',
                    valueProp: 'security_safety'
                }
            },
            callbacks: {
                onReady: () => {
                    console.log('Checkout pronto para uso');
                },
                onSubmit: () => {
                    console.log('Usuário iniciou o pagamento');
                },
                onError: (error) => {
                    console.error('Erro no checkout:', error);
                    alert('Ocorreu um erro ao carregar o pagamento. Tente novamente.');
                }
            }
        });
    } catch (error) {
        console.error('Erro ao renderizar botão:', error);
        alert('Não foi possível carregar o checkout. Tente novamente mais tarde.');
    }
}

/**
 * Atualiza a interface com os dados da corrida
 */
function updateUI(rideData) {
    document.getElementById('origin').textContent = rideData.origin;
    document.getElementById('destination').textContent = rideData.destination;
    document.getElementById('passenger').textContent = rideData.passenger_name;
    document.getElementById('date').textContent = rideData.date;
    document.getElementById('amount').textContent = `R$ ${rideData.amount.toFixed(2)}`;
}

/**
 * Função principal
 */
async function init() {
    try {
        // 1. Buscar dados da corrida
        const rideData = await getRideData();
        updateUI(rideData);
        
        // 2. Criar preferência no backend
        const preferenceId = await createPreference(rideData);
        console.log('Preferência criada:', preferenceId);
        
        // 3. Renderizar botão de pagamento
        await renderPaymentButton(preferenceId);
        
    } catch (error) {
        console.error('Erro na inicialização:', error);
        document.getElementById('walletBrick_container').innerHTML = `
            <div class="loading">
                ⚠️ Erro ao carregar pagamento.<br>
                <button onclick="location.reload()">Tentar novamente</button>
            </div>
        `;
    }
}

// Inicia o checkout quando a página carregar
init();
