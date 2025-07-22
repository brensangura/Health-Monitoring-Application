function initChatbot() {
    const chatbotMessages = document.getElementById('chatbotMessages');
    const userMessageInput = document.getElementById('userMessage');
    const sendMessageBtn = document.getElementById('sendMessage');
    const checkSymptomsBtn = document.getElementById('checkSymptoms');
    const symptomsInput = document.getElementById('symptomsInput');
    const symptomResults = document.getElementById('symptomResults');
    const healthTip = document.getElementById('healthTip');
    const newTipBtn = document.getElementById('newTip');
    
    // Handle sending messages to chatbot
    function sendMessage() {
        const message = userMessageInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessageToChat(message, 'user');
        userMessageInput.value = '';
        
        // Send to server and get response
        fetch('/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChat(data.response, 'bot');
        });
    }
    
    // Add a message to the chat UI
    function addMessageToChat(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
        messageDiv.textContent = message;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }
    
    // Check symptoms
    function checkSymptoms() {
        const symptoms = symptomsInput.value.trim();
        if (symptoms === '') return;
        
        fetch('/log_symptoms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ symptoms: symptoms })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                symptomResults.innerHTML = `
                    <p>Your symptoms have been logged. Here's some general advice:</p>
                    <ul>
                        <li>Rest and stay hydrated</li>
                        <li>Monitor your symptoms</li>
                        <li>Contact a doctor if symptoms worsen</li>
                    </ul>
                `;
            }
        });
    }
    
    // Get a new health tip
    function getNewTip() {
        fetch('/get_health_tip')
        .then(response => response.json())
        .then(data => {
            healthTip.textContent = data.tip;
        });
    }
    
    // Event listeners
    sendMessageBtn.addEventListener('click', sendMessage);
    userMessageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    checkSymptomsBtn.addEventListener('click', checkSymptoms);
    newTipBtn.addEventListener('click', getNewTip);
    
    // Initial tip
    getNewTip();
}
