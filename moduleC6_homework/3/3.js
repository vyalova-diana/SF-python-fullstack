const wsUri = "wss://echo-ws-service.herokuapp.com";

const input = document.querySelector('.input_msg');
const output = document.querySelector('.chat_content');
const btnSendMsg = document.querySelector('.j-btn-send');
const btnSendGeo = document.querySelector('.j-btn-geo');

let websocket;

function writeToScreen(message, type, href) {
    let msg = document.createElement("div");
    msg.className = `${type}_chat_msg`;
    if (href === undefined) {
        msg.textContent = message;
        output.appendChild(msg);
    }
    else {
        let link = document.createElement("a");
        link.href = href;
        link.target = "_blank";
        link.textContent = message;
        msg.appendChild(link);
        output.appendChild(msg);
    }
}

window.addEventListener('load', () => {
    websocket = new WebSocket(wsUri);
    websocket.onopen = function() {
        console.log("CONNECTED");
    };
    websocket.onclose = function() {
        console.log("DISCONNECTED");
    };
    websocket.onmessage = function(evt) {
        // if (typeof(evt.data) e)
        //     writeToScreen(`${evt.data}`,"server");
        const dataResponse = JSON.parse(evt.data);
        if (dataResponse.type === "input")
            writeToScreen(`${dataResponse.data}`,"server");
    };
    websocket.onerror = function(evt) {
        writeToScreen(`Error: ${evt.data}`,"server");
    };
});

btnSendMsg.addEventListener('click', () => {
    const message = input.value;
    if (message) {
        writeToScreen(message, "user");
        const objectToSend = JSON.stringify({
            type: "input",
            data: message
        });
        websocket.send(objectToSend);
    }
});

// Функция, выводящая текст об ошибке в получении геолокации
const error = () => {
    writeToScreen('Невозможно получить ваше местоположение', "server");
};

// Функция, срабатывающая при успешном получении геолокации
const success = (position) => {
    const latitude  = position.coords.latitude;
    const longitude = position.coords.longitude;
    writeToScreen('Гео-локация',
        "user",
        `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`);
    const objectToSend = JSON.stringify({
        type: "geo",
        data: {latitude, longitude}
    });
    websocket.send(objectToSend);
};

btnSendGeo.addEventListener('click', () => {
    if (!navigator.geolocation) {
        writeToScreen('Geolocation не поддерживается вашим браузером',"server");
    } else {
        console.log('Определение местоположения…');
        navigator.geolocation.getCurrentPosition(success, error);

    }

});

