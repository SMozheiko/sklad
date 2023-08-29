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

function productManufacturerCreateListener(elem, header) {
    if (elem.options[elem.selectedIndex].value === 'add new') {
        const newManufacturerForm = document.createElement('DIV');
        const ok = document.createElement('BUTTON');
        ok.innerText = 'OK';
        ok.addEventListener('click', event => {
          const newOpt = document.createElement('OPTION');
          newOpt.value = event.target.parentElement.previousElementSibling.querySelector('INPUT').value;
          newOpt.innerText = event.target.parentElement.previousElementSibling.querySelector('INPUT').value;
          newOpt.setAttribute('selected', 'selected')
          elem.append(newOpt);
          newManufacturerForm.remove();
        });
        const cancel = document.createElement('BUTTON');
        cancel.innerText = 'Отмена';
        cancel.classList.add('cancel-button');
        cancel.addEventListener('click', event => {
          newManufacturerForm.remove();
        });
        const windowHeader = document.createElement('h4');
        windowHeader.innerText = header;
        const newManContainer = document.createElement('DIV');
        const newMan = document.createElement('INPUT');
        newMan.name = elem.name;
        newManContainer.appendChild(newMan);
        const buttonsContainer = document.createElement('DIV');
        buttonsContainer.append(...[ok, cancel])
        newManufacturerForm.append(...[windowHeader, newManContainer, buttonsContainer]);
        newManufacturerForm.classList.add('dialog');
        elem.before(newManufacturerForm);
    }
}

function renderHeader(response) {
    const header = document.querySelector('#header');
    header.innerHTML = response.header;
}


eel.expose(renderResponse);
function renderResponse(response) {
    if (response.tag === 'frame') {
        renderForm(response)
    } else {
        render(response)
    };
    if (response.header !== null) {
        renderHeader(response)
    }
}

async function formControlListner(event) {
    event.preventDefault();
    if (event.target.classList.contains('control-button')) {
        if (event.target.dataset.action === 'cancel') {
            const frame = document.querySelector('.frame');
            for (let child of frame.children) {
                child.remove();
            }
            frame.classList.remove('visible-frame');
        } else if (event.target.dataset.action === 'exit') {
            window.close();
        } else if (event.target.dataset.action === 'create_order') {
            let orderData = collectData(event.target);
            await eel.route(event.target.dataset.action, 'post', {}, orderData)();
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
                if (child.value !== 'add new') {
                    data[child.name] = child.value;
                }
            });
            form.querySelectorAll('SELECT').forEach(select => {
                if (select.multiple === true) {
                    data[select.name] = [];
                    for (let option of select.selectedOptions) {
                        if (option.value !== 'add new') {
                            data[select.name].push(...[option.value]);
                        }
                    }
                } else {
                    let value = select.options[select.selectedIndex];
                    data[select.name] = value.value;
                }
            });
            await eel.route(event.target.dataset.action, 'post', params, data)();
        }
    }
}

async function PageClickListener(event) {
    event.preventDefault();
    if (event.target.id === 'logout') {
        document.querySelector('#header').innerHTML = null;
        document.querySelector('#body').innerHTML = null;
        await eel.route(event.target.dataset.action, 'get', {}, {})
    }
    else if (event.target.classList.contains('operational-button')) {
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
    const body = document.querySelector('body');
    body.addEventListener('click', async (event) => PageClickListener(event));
    await eel.route('managers_list', 'get', {}, {});
})