class ChatBot {
    constructor() {
        this.messagesContainer = document.getElementById('messages-container');
        this.messageInput = document.getElementById('message-input');
        this.chatForm = document.getElementById('chat-form');
        this.sendButton = document.getElementById('send-button');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.ingredientsDisplay = document.getElementById('ingredients-display');
        this.ingredientsList = document.getElementById('ingredients-list');
        this.recommendationsContainer = document.getElementById('recommendations-container');
        
        this.currentIngredients = [];
        this.isProcessing = false;
        
        this.init();
    }
    
    init() {
        // Afficher l'heure de bienvenue
        document.getElementById('welcome-time').textContent = this.formatTime(new Date());
        
        // Événements
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSubmit(e);
            }
        });
        
        // Focus sur l'input
        this.messageInput.focus();
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        if (this.isProcessing) return;
        
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Ajouter le message utilisateur
        this.addUserMessage(message);
        this.messageInput.value = '';
        this.setProcessing(true);
        
        try {
            // Envoyer à l'API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Afficher la réponse du bot
            setTimeout(() => {
                this.addBotMessage(
                    data.bot_response || "Voici vos recommandations :",
                    data.recommendations || []
                );
                this.setProcessing(false);
            }, 1000);
            
        } catch (error) {
            console.error('Erreur:', error);
            setTimeout(() => {
                this.addBotMessage('Désolé, une erreur est survenue. Veuillez réessayer.');
                this.setProcessing(false);
            }, 1000);
        }
    }
    
    addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message fade-in';
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${this.escapeHtml(message)}</p>
                <span class="message-time">${this.formatTime(new Date())}</span>
            </div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addBotMessage(message, recommendations = []) {
    const messageDiv = document.createElement('p');
    messageDiv.className = 'message bot-message fade-in';

        let recommandationsHtml = '';
        if (recommendations.length > 0) {
            recommandationsHtml = `
                <p class="suggestion-title">Suggestions :</p>
                    <ul class="recommendation-list">
                        ${recommendations.map(rec => `<li>🥣 ${this.escapeHtml(rec.product_name || rec)}</li>`).join('')}
                    </ul>
            `;
        }

        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${this.escapeHtml(message)}</p>
                ${recommandationsHtml}
                <span class="message-time">${this.formatTime(new Date())}</span>
            </div>
        `;

        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    setProcessing(processing) {
        this.isProcessing = processing;
        this.sendButton.disabled = processing;
        this.messageInput.disabled = processing;
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }, 100);
    }
    
    formatTime(date) {
        return date.toLocaleTimeString('fr-FR', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialiser le chatbot quand la page est chargée
document.addEventListener('DOMContentLoaded', () => {
    window.chatBot = new ChatBot();
});

// Gestion des erreurs globales
window.addEventListener('error', (e) => {
    console.error('Erreur JavaScript:', e.error);
});
