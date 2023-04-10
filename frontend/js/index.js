'use strict';

function render(html) {
    const body = document.querySelector('#body');
    body.innerHTML = html;
}

function renderForm(action, html) {
    const frame = document.querySelector('#frame');
    frame.innerHTML = html;
    frame.addEventListener('click', async (event) => {
        if (event.target.tagName !== 'BUTTON') {} else {
            if (event.target.classList.contains('ok-button')) {
                const form = frame.querySelector('form');
                const data = serializeForm(form);
                await post_html(action, data);
            };
            frame.classList.toggle('visible-frame');
        }
    });
    frame.classList.toggle('visible-frame');
}

function serializeForm(form) {
    const data = new FormData(form);
    return data;
}

async function get_html(action, data) {
    const result = await eel.route(action, 'get', data)();
    return result;
}

async function post_html(action, data) {
    const result = await eel.route(action, 'post', data)();
    render(result);
}

window.addEventListener('load', async () => {
    const result = await get_html('managers_list', {});
    renderForm('login', result);
})