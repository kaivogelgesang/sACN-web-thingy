'use strict';

let sliders = {};
document.querySelectorAll('.ch-slider').forEach((o) => {
    const m = o.id.match(/ch-(\d+)/);
    if (m && m[1]) {
        const i = m[1];
        sliders[i] = o;
    }
});

const ws = new WebSocket("ws://" + window.location.host + "/ws");

for (const [channel, slider] of Object.entries(sliders)) {
    slider.addEventListener('input', () => {
        ws.send(`{"${channel}":${slider.value}}`);
    })
}

ws.onmessage = (msg) => {
    console.log(msg);
    const data = JSON.parse(msg.data);
    for (const [channel, value] of Object.entries(data)) {
        sliders[channel].value = value;
    }
};

ws.onerror = console.log;