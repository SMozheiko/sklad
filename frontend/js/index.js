'use strict';

function render(html) {
    const body = document.querySelector('#body');
    body.innerHTML = html;
}

function renderForm(html) {
    const frame = document.querySelector('.frame');
    frame.innerHTML = html;
    frame.classList.add('visible-frame');
}


async function get(action) {
    const result = await eel.route(action, 'get')();
    return result;
}

window.addEventListener('load', async () => {
    const html = await get('managers_list');
    renderForm(html);
})