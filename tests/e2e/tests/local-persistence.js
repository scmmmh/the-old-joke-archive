import { ClientFunction } from "testcafe";

function storeValue(obj, path, value) {
    const pathElements = path.split('.');
    let current = obj;
    for (let idx = 0; idx < pathElements.length; idx++) {
        const element = pathElements[idx];
        if (idx === pathElements.length - 1) {
            current[element] = value;
        } else {
            if (!current[element]) {
                current[element] = {};
            }
            current = current[element];
        }
    }
    return obj;
}

function loadValue(obj, path, defaultValue) {
    const pathElements = path.split('.');
    let current = obj;
    for (let idx = 0; idx < pathElements.length; idx++) {
        const element = pathElements[idx];
        if (idx === pathElements.length - 1) {
            if (current[element] !== undefined) {
                return current[element];
            } else {
                return defaultValue;
            }
        } else {
            if (current[element]) {
                current = current[element];
            } else {
                return defaultValue;
            }
        }
    }
    return defaultValue;
}

function deleteValue(storage, path) {
    let obj = {};
    const data = storage.getItem('toja:storage');
    if (data) {
        obj = JSON.parse(data);
    }
    const pathElements = path.split('.');
    let current = obj;
    for (let idx = 0; idx < pathElements.length; idx++) {
        const element = pathElements[idx];
        if (idx === pathElements.length - 1) {
            delete current[element];
        } else {
            if (!current[element]) {
                break;
            }
            current = current[element];
        }
    }
    storage.setItem('toja:storage', JSON.stringify(obj));
}

const getStorage = ClientFunction((type) => {
    const data = (type === 'session' ? sessionStorage : localStorage).getItem('toja:storage');
    if (data) {
        return JSON.parse(data);
    } else {
        return {};
    }
});

const setStorage = ClientFunction((type, obj) => {
    (type === 'session' ? sessionStorage : localStorage).setItem('toja:storage', JSON.stringify(obj));
});

export async function sessionStoreValue(path, value) {
    await setStorage('session', storeValue(await getStorage('session'), path, value));
}

export async function sessionLoadValue(path, defaultValue) {
    return loadValue(await getStorage('session'), path, defaultValue);
}

export async function sessionDeleteValue(path) {
    await setStorage('session', deleteValue(await getStorage('session'), path));
}

export async function localStoreValue(path, value) {
    await setStorage('local', storeValue(await getStorage('local'), path, value));
}

export async function localLoadValue(path, defaultValue) {
    return loadValue(await getStorage('local'), path, defaultValue);
}

export async function localDeleteValue(path) {
    await setStorage('local', deleteValue(await getStorage('local'), path));
}
