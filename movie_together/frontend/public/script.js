const users = new Map();

function addMessage(text) {
    const messages = document.querySelector('.messageList');
    const message = document.createElement('li');
    const messageText = document.createTextNode(text);
    message.appendChild(messageText);
    messages.appendChild(message);
}

function getMessage(event) {
    const data = JSON.parse(event.data)
    if (data.action === "CONNECT") {
        users.set(data.username, data.data);
        addMessage(
            `${data.data.first_name} ${data.data.last_name}: ${data.datetime} : connected`
        );
    }
    else if (data.action === "MESSAGE") {
        const user = users.get(data.username);
        addMessage(
            `${user.first_name} ${user.last_name}: ${data.datetime} : ${data.data}`
        );
    // } else if (data.action === "PLAY") {
    //     document.querySelector(".video").play()
    // } else if (data.action === "PAUSE") {
    //     document.querySelector(".video").pause()
    } else if (data.action === "DISCONNECT") {
        const user = users.get(data.username);
        addMessage(
            `${user.first_name} ${user.last_name}: ${data.datetime} : disconnected`
        );
    }
}

function sendMessage(ws, event) {
    event.preventDefault();
    const input = event.target.querySelector(".messageForm__text");
    const data = {
        action: 'MESSAGE',
        data: input.value,
    }
    ws.send(JSON.stringify(data))
    input.value = ''
    addMessage(`You: ${data.data}`);
}

// function controlVideo(clientId, action, event) {
//     const data = {
//         type: 'PLAYER',
//         message: action,
//         author: clientId,
//     }
//     ws.send(JSON.stringify(data))
// }


function connect(event) {
    event.preventDefault();
    const sessionInput = event.target.querySelector(".connectForm_session");
    const tokenInput = event.target.querySelector(".connectForm_token");

    const ws = new WebSocket(
        `ws://localhost:8000/api/v1/room/${sessionInput.value}?auth=${tokenInput.value}`
    );
    ws.onopen = event => {
        document.querySelector(".session").style.display = "block";
        ws.addEventListener("message", getMessage);
        document.querySelector(".messageForm")
            .addEventListener("submit", sendMessage.bind(null, ws))
    }
    ws.onclose = event => {
        document.querySelector(".messageForm")
            .removeEventListener("submit", sendMessage.bind(null, ws))
        ws.removeEventListener("message", getMessage);
        document.querySelector(".session").style.display = "none";
        document.querySelector(".messageList").innerHTML = "";
    }
}

document.querySelector(".connectForm")
    .addEventListener("submit", connect);



// const clientId = Date.now();
// document.querySelector("#ws-id").textContent = clientId;
// const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
//
// ws.addEventListener("message", getMessage)
// document.querySelector("#messageForm")
//     .addEventListener("submit", sendMessage.bind(null, clientId))
//
// document.querySelector("#video")
//     .addEventListener("pause", controlVideo.bind(null, clientId, "PAUSE"))
//
// document.querySelector("#video")
//     .addEventListener("play", controlVideo.bind(null, clientId, "PLAY"))
