import { ClientFunction } from "testcafe";

function storeValue(storage, path, value) {
    let obj = {};
    const data = storage['toja:storage'];
    if (data) {
        obj = JSON.parse(data);
    }
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
    storage['toja:storage'] = JSON.stringify(obj);
}

function loadValue(storage, path, defaultValue) {
    const data = storage['toja:storage'];
    if (data) {
        const obj = JSON.parse(data);
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
    }
    return defaultValue;
}

function deleteValue(storage, path) {
    let obj = {};
    const data = storage['toja:storage'];
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
    storage['toja:storage'] = JSON.stringify(obj);
}

const sessionStorage = ClientFunction(() => { return window.sessionStorage; });

export async function sessionStoreValue(path, value) {
    storeValue(await sessionStorage(), path, value);
}

export async function sessionLoadValue(path, defaultValue) {
    return loadValue(await sessionStorage(), path, defaultValue);
}

export async function sessionDeleteValue(path) {
    return deleteValue(await sessionStorage(), path);
}

const localStorage = ClientFunction(() => { return window.localStorage; });

export async function localStoreValue(path, value) {
    storeValue(await localStorage(), path, value);
}

export async function localLoadValue(path, defaultValue) {
    return loadValue(await localStorage(), path, defaultValue);
}

export async function localDeleteValue(path) {
    return deleteValue(await localStorage(), path);
}
