function getMessage(event) {
    const messages = document.querySelector('#messages');
    const message = document.createElement('li');

    const data = JSON.parse(event.data)
    if (data.type === "MESSAGE") {
        const messageText = document.createTextNode(
            `${data.author}: ${data.message}`
        );
        message.appendChild(messageText)
        messages.appendChild(message)
    } else if (data.type === "PLAYER") {
        if (data.message === "PLAY") {
            document.querySelector("#video").play()
        } else if (data.message === "PAUSE") {
            document.querySelector("#video").pause()
        }
    }
}

function sendMessage(clientId, event) {
    const input = document.querySelector("#messageText");

    const data = {
        type: 'MESSAGE',
        message: input.value,
        author: clientId,
    }
    ws.send(JSON.stringify(data))
    input.value = ''

    const messages = document.querySelector('#messages');
    const message = document.createElement('li');
    const messageText = document.createTextNode(
        `You: ${data.message}`
    );
    message.appendChild(messageText)
    messages.appendChild(message)

    event.preventDefault()
}


function controlVideo(clientId, action, event) {
    const data = {
        type: 'PLAYER',
        message: action,
        author: clientId,
    }
    ws.send(JSON.stringify(data))
}


const clientId = Date.now();
document.querySelector("#ws-id").textContent = clientId;
const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);

ws.addEventListener("message", getMessage)
document.querySelector("#messageForm")
    .addEventListener("submit", sendMessage.bind(null, clientId))

document.querySelector("#video")
    .addEventListener("pause", controlVideo.bind(null, clientId, "PAUSE"))

document.querySelector("#video")
    .addEventListener("play", controlVideo.bind(null, clientId, "PLAY"))
