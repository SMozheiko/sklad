'use strict';

function render(html) {
    const body = document.querySelector('#body');
    body.innerHTML = html;
}

async function get_html(action, data) {
    const result = await eel.route(action, 'get', data)();
    render(result);
}

window.addEventListener('load', async () => await get_html('managers_list', {}))