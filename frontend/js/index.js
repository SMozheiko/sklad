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
        } else if (event.target.dataset.action === 'cancel') {
            window.close();
        } else {
            const data = {};
            const form = event.target.parentElement.previousElementSibling;
            for (let child of form.children) {
                if (child.tagName === 'INPUT') {
                    data[child.name] = child.value;
                }
            }
            await eel.route(event.target.dataset.action, 'post', {}, data)();
        }
    }
}

window.addEventListener('load', async () => {
    const frame = document.querySelector('.frame');
    frame.addEventListener('click', async (event) => formControlListner(event));
    await eel.route('managers_list', 'get', {}, {});
})