class BotaoDeslizar extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.isDragging = false;
        this.acaoConcluida = false;
        this.startX = 0;
    }

    connectedCallback() {
        // Lê as propriedades que você passar na tag HTML (ou usa um padrão)
        const textoPadrao = this.getAttribute('texto') || 'DESLIZE PARA INICIAR';
        const textoSucesso = this.getAttribute('texto-sucesso') || 'CONCLUÍDO!';
        const cor = this.getAttribute('cor') || '#00a859';

        this.shadowRoot.innerHTML = `
            <style>
                .swipe-container {
                    position: relative;
                    width: 100%;
                    max-width: 350px;
                    height: 60px;
                    background-color: #e0e0e0;
                    border-radius: 30px;
                    overflow: hidden;
                    display: flex;
                    align-items: center;
                    box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
                    user-select: none;
                    margin: 10px 0;
                }
                .swipe-text {
                    position: absolute;
                    width: 100%;
                    text-align: center;
                    color: #757575;
                    font-weight: bold;
                    font-family: sans-serif;
                    font-size: 16px;
                    z-index: 1;
                    pointer-events: none;
                }
                .swipe-thumb {
                    position: absolute;
                    left: 5px;
                    width: 50px;
                    height: 50px;
                    background-color: ${cor};
                    border-radius: 50%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    cursor: grab;
                    z-index: 2;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                    transition: transform 0.3s ease, background-color 0.3s ease;
                }
                .swipe-thumb:active { cursor: grabbing; }
                .swipe-thumb svg { width: 24px; height: 24px; stroke: white; }
                
                .swipe-success { background-color: ${cor}; transition: background-color 0.3s ease; }
                .swipe-success .swipe-text { color: white; }
                .swipe-success .swipe-thumb { filter: brightness(0.8); }
            </style>
            
            <div class="swipe-container" id="container">
                <div class="swipe-text" id="texto">${textoPadrao}</div>
                <div class="swipe-thumb" id="thumb">
                    <svg viewBox="0 0 24 24" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                        <polyline points="9 18 15 12 9 6"></polyline>
                    </svg>
                </div>
            </div>
        `;

        this.container = this.shadowRoot.getElementById('container');
        this.thumb = this.shadowRoot.getElementById('thumb');
        this.textoEl = this.shadowRoot.getElementById('texto');
        
        this.textoSucessoStr = textoSucesso;
        this.initEvents();
    }

    initEvents() {
        const iniciarArrasto = (e) => {
            if (this.acaoConcluida) return;
            this.isDragging = true;
            this.startX = e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
            this.thumb.style.transition = 'none';
        };

        const arrastar = (e) => {
            if (!this.isDragging) return;
            
            const currentX = e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
            let movimento = currentX - this.startX;
            const limiteMaximo = this.container.offsetWidth - this.thumb.offsetWidth - 10;

            if (movimento < 0) movimento = 0;
            if (movimento > limiteMaximo) movimento = limiteMaximo;

            this.thumb.style.transform = `translateX(${movimento}px)`;

            if (movimento >= limiteMaximo * 0.95) {
                this.isDragging = false;
                this.acaoConcluida = true;
                this.thumb.style.transform = `translateX(${limiteMaximo}px)`;
                
                this.container.classList.add('swipe-success');
                this.textoEl.innerText = this.textoSucessoStr;

                // Dispara um evento personalizado para o HTML saber que terminou
                this.dispatchEvent(new CustomEvent('confirmado', { bubbles: true, composed: true }));
            }
        };

        const pararArrasto = () => {
            if (!this.isDragging) return;
            this.isDragging = false;
            this.thumb.style.transition = 'transform 0.3s ease';
            this.thumb.style.transform = `translateX(0px)`;
        };

        this.thumb.addEventListener('mousedown', iniciarArrasto);
        document.addEventListener('mousemove', arrastar);
        document.addEventListener('mouseup', pararArrasto);

        this.thumb.addEventListener('touchstart', iniciarArrasto, { passive: true });
        document.addEventListener('touchmove', arrastar, { passive: true });
        document.addEventListener('touchend', pararArrasto);
    }

    // Método que permite resetar o botão via JavaScript, se precisar
    resetar() {
        this.acaoConcluida = false;
        this.container.classList.remove('swipe-success');
        this.textoEl.innerText = this.getAttribute('texto') || 'DESLIZE PARA INICIAR';
        this.thumb.style.transition = 'transform 0.3s ease';
        this.thumb.style.transform = `translateX(0px)`;
    }
}

// Registra a nova tag HTML
customElements.define('botao-deslizar', BotaoDeslizar);
