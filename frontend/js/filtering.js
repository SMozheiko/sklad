function searchProducts(el) {
    const params = {};
    params[el.name] = el.value;
    const func = async (params, el) => {
        await eel.route(el.dataset.action, 'get', params, {})();
    };
    func(params, el);
}

function filterProducts(button) {
    const el = button.parentElement.parentElement;
    const filters = el.querySelector('.filter');
    const sorting = el.querySelector('.sorting');
    const params = {
        'filter': {
            'manufacturer': [],
            'category': []
        },
        'sorting': {
            'sort': null,
            'order': null
        }
    }

    const selectFilter = filters.querySelectorAll('SELECT');
    selectFilter.forEach(select => {
        for (let option of select.selectedOptions) {
            if (option.value !== 'all') {
                params.filter[select.name].push(...[option.value])
            }
        }    
    });
    const sortingFilter = sorting.querySelectorAll('SELECT');
    sortingFilter.forEach(select => {
        params.sorting[select.name] = select.options[select.selectedIndex].value;
    });
    const func = async (params, button) => {
        await eel.route(button.dataset.action, 'get', params, {})();
    };
    func(params, button);
}

