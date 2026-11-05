const chatBox = document.getElementById("chat-box");

const chatList = document.getElementById("chat-list");

const userInput = document.getElementById("user-input");

const sendButton = document.getElementById("send-btn");

const newChatButton = document.getElementById("new-chat-btn");

const currentChatTitle = document.getElementById("current-chat-title");

let currentChatId = null;


// API helper
async function apiRequest(url, options = {}) {

    const response = await fetch(url, options);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
    }

    return data;
}


// Display messages
function addMessage(message, sender) {

    const messageElement = document.createElement("div");

    messageElement.classList.add(sender + "-message");

    messageElement.textContent = message;

    chatBox.appendChild(messageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// Show welcome message
function showWelcome() {

    chatBox.innerHTML = `
        <div class="welcome-message">
            <h1>Welcome to AURA</h1>
            <p>How can I help you today?</p>
        </div>
    `;
}


// Load all chat sessions
async function loadChats() {

    try {

        const data = await apiRequest("/api/chats");

        chatList.innerHTML = "";

        data.chats.forEach(chat => {

            const chatItem = document.createElement("div");

            chatItem.classList.add("chat-item");

            if (chat.id === currentChatId) {
                chatItem.classList.add("active");
            }

            const title = document.createElement("span");

            title.classList.add("chat-title");

            title.textContent = chat.title;

            title.addEventListener("click", () => {
                openChat(chat.id);
            });

            const deleteButton = document.createElement("button");

            deleteButton.classList.add("delete-btn");

            deleteButton.textContent = "×";

            deleteButton.title = "Delete chat";

            deleteButton.addEventListener("click", (event) => {

                event.stopPropagation();

                deleteChat(chat.id);

            });

            chatItem.appendChild(title);

            chatItem.appendChild(deleteButton);

            chatItem.addEventListener("click", () => {
                openChat(chat.id);
            });

            chatList.appendChild(chatItem);

        });

    }

    catch (error) {

        console.error(error);

        alert(error.message);

    }

}


// Open selected chat
async function openChat(chatId) {

    try {

        const data = await apiRequest("/api/chats/" + chatId);

        currentChatId = chatId;

        currentChatTitle.textContent = data.title;

        chatBox.innerHTML = "";

        if (data.messages.length === 0) {

            showWelcome();

        } else {

            data.messages.forEach(message => {

                if (message.role === "user") {
                    addMessage(message.content, "user");
                }

                else if (message.role === "assistant") {
                    addMessage(message.content, "bot");
                }

            });

        }

        await loadChats();

    }

    catch (error) {

        alert(error.message);

    }

}


// Create new chat
async function createNewChat() {

    try {

        const data = await apiRequest("/api/chats", {
            method: "POST"
        });

        await openChat(data.id);

        userInput.focus();

    }

    catch (error) {

        alert(error.message);

    }

}


// Delete chat
async function deleteChat(chatId) {

    const confirmed = confirm("Are you sure you want to delete this conversation?");

    if (!confirmed) {
        return;
    }

    try {

        await apiRequest("/api/chats/" + chatId, {
            method: "DELETE"
        });

        if (currentChatId === chatId) {
            currentChatId = null;
        }

        await loadChats();

        const data = await apiRequest("/api/chats");

        if (data.chats.length > 0) {

            await openChat(data.chats[0].id);

        }

    }

    catch (error) {

        alert(error.message);

    }

}


// Send message to AURA
async function sendMessage() {

    const message = userInput.value.trim();

    if (message === "" || !currentChatId) {
        return;
    }

    addMessage(message, "user");

    userInput.value = "";

    sendButton.disabled = true;

    const loading = document.createElement("div");

    loading.classList.add("bot-message");

    loading.textContent = "AURA is thinking...";

    chatBox.appendChild(loading);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const data = await apiRequest("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message,
                chat_id: currentChatId
            })

        });

        loading.remove();

        addMessage(data.reply, "bot");

        currentChatTitle.textContent = data.title;

        await loadChats();

    }

    catch (error) {

        loading.remove();

        addMessage("Error: " + error.message, "bot");

    }

    finally {

        sendButton.disabled = false;

        userInput.focus();

    }

}


// Button events
sendButton.addEventListener("click", sendMessage);

newChatButton.addEventListener("click", createNewChat);


// Enter key
userInput.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});


// Start application
async function initializeApp() {

    try {

        const data = await apiRequest("/api/chats");

        if (data.chats.length > 0) {

            await openChat(data.chats[0].id);

        }

    }

    catch (error) {

        console.error("Unable to start AURA:", error);

    }

}


initializeApp();