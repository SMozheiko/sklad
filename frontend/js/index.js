'use strict';

function render(response) {
    const frame = document.querySelector('.frame');
    if (frame.classList.contains('visible-frame')) {
        frame.classList.remove('visible-frame')
    };
    const body = document.querySelector(`#${response.tag}`);
    body.innerHTML = response.html;
}

function renderForm(response) {
    const frame = document.querySelector('.frame');
    frame.innerHTML = response.html;
    frame.classList.add('visible-frame');
}

eel.expose(renderResponse);
function renderResponse(response) {
    if (response.tag === 'frame') {
        renderForm(response)
    } else {
        render(response)
    }
}

async function formControlListner(event) {
    event.preventDefault();
    if (event.target.tagName === 'BUTTON') {
        if (event.target.dataset.action === 'cancel') {
            const frame = document.querySelector('.frame');
            frame.innerHTML = '';
            frame.classList.remove('visible-frame');
        } else if (event.target.dataset.action === 'exit') {
            window.close();
        } else {
            const params = {}
            for (let key in event.target.dataset) {
                if (key !== 'action') {
                    params[key] = event.target.dataset[key];
                }
            }
            const data = {};
            const form = event.target.parentElement.previousElementSibling;
            form.querySelectorAll('INPUT').forEach(child => {
                data[child.name] = child.value;
            });
            form.querySelectorAll('SELECT').forEach(child => {
                let value = child.options[child.selectedIndex];
                data[child.name] = value.value;
            });
            await eel.route(event.target.dataset.action, 'post', params, data)();
        }
    }
}

async function PageClickListener(event) {
    event.preventDefault();
    if (event.target.classList.contains('operational-button')) {
        const params = {}
        for (let key in event.target.dataset) {
            if (key !== 'action') {
                params[key] = event.target.dataset[key];
            }
        }
        await eel.route(event.target.dataset.action, 'get', params, {})
    }
}

window.addEventListener('load', async () => {
    const frame = document.querySelector('.frame');
    frame.addEventListener('click', async (event) => formControlListner(event));
    const body = document.querySelector('#body');
    body.addEventListener('click', async (event) => PageClickListener(event));
    await eel.route('managers_list', 'get', {}, {});
})