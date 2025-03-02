// Add smooth scrolling and animations
document.getElementById("userInputButton").addEventListener("click", getUserInput, false);

document.getElementById("userInput").addEventListener("keyup", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        getUserInput();
    }
});

// Add typing animation
function addTypingIndicator() {
    const messages = document.getElementById("messages");
    const typingDiv = document.createElement("div");
    typingDiv.className = "message to typing";
    typingDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    messages.appendChild(typingDiv);
    messages.scrollTop = messages.scrollHeight;
    return typingDiv;
}

function removeTypingIndicator(typingDiv) {
    if (typingDiv && typingDiv.parentNode) {
        typingDiv.parentNode.removeChild(typingDiv);
    }
}

eel.expose(addUserMsg);
eel.expose(addAppMsg);

function addUserMsg(msg) {
    const element = document.getElementById("messages");
    const messageDiv = document.createElement("div");
    messageDiv.className = "message from";
    messageDiv.textContent = msg;
    messageDiv.style.opacity = "0";
    
    element.appendChild(messageDiv);
    
    // Trigger reflow for animation
    messageDiv.offsetHeight;
    
    messageDiv.style.opacity = "1";
    element.scrollTop = element.scrollHeight;
}

function addAppMsg(msg) {
    const typingIndicator = addTypingIndicator();
    
    // Simulate typing delay
    setTimeout(() => {
        removeTypingIndicator(typingIndicator);
        
        const element = document.getElementById("messages");
        const messageDiv = document.createElement("div");
        messageDiv.className = "message to";
        messageDiv.textContent = msg;
        messageDiv.style.opacity = "0";
        
        element.appendChild(messageDiv);
        
        // Trigger reflow for animation
        messageDiv.offsetHeight;
        
        messageDiv.style.opacity = "1";
        element.scrollTop = element.scrollHeight;
    }, 1000); // Adjust timing as needed
}

function getUserInput() {
    const element = document.getElementById("userInput");
    const msg = element.value.trim();
    
    if (msg.length > 0) {
        element.value = "";
        eel.getUserInput(msg);
        
        // Add focus back to input
        element.focus();
    }
}

// Add some interactive effects
document.getElementById("userInput").addEventListener("focus", function() {
    this.parentElement.style.boxShadow = "0 0 15px rgba(56, 255, 132, 0.3)";
});

document.getElementById("userInput").addEventListener("blur", function() {
    this.parentElement.style.boxShadow = "none";
});