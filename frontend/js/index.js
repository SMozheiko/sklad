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

eel.expose(renderErrors);
function renderErrors(errors) {
    const form = document.querySelector('.frame').querySelector('FORM');
    const errorsContainer = document.createElement('div');
    errorsContainer.className = 'form-errors';
    for (let error of errors) {
        const el = document.createElement('p');
        el.className = 'form-error';
        el.innerText = error;
    }
    form.prepend(errorsContainer);
}

async function formControlListner(event) {
    event.preventDefault();
    if (event.target.tagName === 'BUTTON') {
        if (event.target.dataset.action === 'cancel') {
            const frame = document.querySelector('.frame');
            frame.innerHTML = '';
            frame.classList.remove('visible-frame');
        } else {
            const data = {};
            const form = event.target.parentElement.previousElementSibling;
            for (let child of form.children) {
                if (child.tagName === 'INPUT') {
                    data[child.name] = child.value;
                }
            }
            const html = await eel.route(event.target.dataset.action, 'post', data)();
            console.log(html);
            if (html) {
                form.parentElement.parentElement.classList.remove('visible-frame');
                render(html);
            }
        }
    }
}

window.addEventListener('load', async () => {
    const frame = document.querySelector('.frame');
    frame.addEventListener('click', async (event) => formControlListner(event));
    const html = await get('managers_list');
    renderForm(html);
})