window.onload = (event) => {
    if (window.location.pathname.startsWith('/surprise')) {
      handle_used_codes()
    }
  }

function clear_used_codes() {
    localStorage.removeItem('used_codes');

    const el = document.getElementById("used-codes-container");
    if (el) {
        el.remove();
    }
}

function handle_used_codes() {
    const surprise_code = document.getElementById('surprise-code');
    if (surprise_code) {
        handle_new_code(surprise_code.textContent);
    }

    const container = document.getElementById('used-codes-list');
    if (container) {
        handle_used_codes_list(container);
    }
}

function handle_new_code(code) {
    var used_codes = localStorage.getItem('used_codes');
    used_codes = used_codes ? JSON.parse(used_codes) : [];

    if (!used_codes.includes(code)) {
        console.log('Caching code: ' + code);
        used_codes.push(code);
    }

    localStorage.setItem('used_codes', JSON.stringify(used_codes));
}

function handle_used_codes_list(container) {
    var used_codes = localStorage.getItem('used_codes');
    if (!used_codes) {
        const el = document.getElementById("used-codes-container");
        if (el) {
            el.remove();
        }
        return;
    }

    used_codes = JSON.parse(used_codes);
    //used_codes.sort();
    for (code of used_codes) {
        const span = document.createElement('span');
        span.classList.add('surprise-code');
        span.textContent = code;

        const a = document.createElement('a');
        a.classList.add('ml-4', 'h5');
        a.href = '/surprise/' + code;
        a.appendChild(span);

        const li = document.createElement('li');
        li.classList.add('mt-2');
        li.appendChild(a);

        container.appendChild(li);
    }

    const el = document.getElementById("used-codes-container");
    if (el) {
        el.classList.remove('invisible');
    }
}
