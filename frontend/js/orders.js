'use strict';

const dataLists = {
    customers: [],
    products: []
};

function focusIn(el) {
    getDataList(el);
    el.nextElementSibling.style.display = 'flex';
}

function focusOut(el) {
    el.nextElementSibling.innerHTML = '';
    el.nextElementSibling.style.display = 'none';
}

function customerClickChoice(el) {
    const title = el.innerText;
    const inputEl = document.querySelector('#customer');
    inputEl.dataset.id = el.dataset.id;
    inputEl.value = title;
    inputEl.textContent = title;
    focusOut(inputEl);
}

function productClickChoice(el) {
    const formSet = el.parentElement.parentElement;
    const product = dataLists['products'][el.dataset.product_idx];
    formSet.querySelectorAll('INPUT').forEach(
        inputEl => inputEl.value = product[inputEl.name]
    )
    focusOut(formSet.querySelector('INPUT'));
}

function customerOnInput(el) {
    el.nextElementSibling.querySelectorAll('SPAN').forEach(sp => sp.remove());
    dataLists['customers'].forEach(customer => {
        if (el.value !== '' && customer['title'].search(el.value) !== -1) {
            let spanEl = document.createElement('span');
            spanEl.addEventListener('click', event => customerClickChoice(event.target));
            spanEl.innerText = customer.title;
            spanEl.dataset.id = customer.id;
            el.nextElementSibling.append(spanEl);
        }
    })
}

function collectData(button) {
    const data = {};
    const form = button.parentElement.previousElementSibling;
    const customer = form.querySelector('#customer');
    data['customer'] = Number.parseInt(customer.dataset.id);
    data['positions'] = [];
    const items = form.querySelectorAll('.order-item');
    items.forEach(item => {
        let id = item.querySelector('INPUT[name=id]').value;
        if (id !== '') {
            const obj = {};
            item.querySelectorAll('INPUT').forEach(input => {
                obj[input.name] = input.value;
            });
            data['positions'].push(obj);
        }
    });
    return data;
}

function productsOnInput(el) {
    el.nextElementSibling.querySelectorAll('SPAN').forEach(sp => sp.remove());
    let i = 0;
    dataLists['products'].forEach(product => {
        if (el.value !== '' && product['title'].search(el.value) !== -1) {
            let spanEl = document.createElement('span');
            spanEl.dataset.product_idx = i;
            spanEl.addEventListener('click', event => productClickChoice(event.target));
            spanEl.innerText = product.title;
            el.nextElementSibling.append(spanEl);
        }
        i++;
    });
}

function addOrderItem(button) {
    const items = document.querySelectorAll('.order-item');
    let i = 0;
    for (let item of items) {
        if (i + 1 === items.length) {
            const newField = item.cloneNode(true);
            newField.querySelectorAll('INPUT').forEach(inp => {
                let id = Number.parseInt(inp.id.split('-')[1]) + 1;
                inp.id = inp.name + `-${id}`;
            });
            item.style.display = 'block';
            item.after(newField);
        };
        i++;
    }
}

function getDataList(el) {
    let getter = async () => {
        const data = {
            action: el.dataset.action
        };
        await getData(data);
    };
    getter();
}

async function getData(data){
    const response = await eel.json_data(data)();
    dataLists[data.action] = [];
    dataLists[data.action].push(...response.result);
}