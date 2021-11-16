import { get } from 'svelte/store';

import { authToken, authUser } from './auth';
import { localLoadValue, sessionLoadValue, NestedStorage } from '../local-persistence';

export class JsonApiException extends Error {
    public errors = [] as JsonApiError[];

    constructor(errors: JsonApiError[]) {
        super('JSONAPI Error');
        this.errors = errors;
    }
}

function getCookie(name: string): string | undefined {
    const cookies = Object.fromEntries(document.cookie.split(';').map((cookie) => {
        return cookie.split('=');
    }));
    return cookies[name];
}

export async function sendJsonApiRequest(method: string, url: string, obj: JsonApiObject) {
    const settings = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-XSRFToken': getCookie('_xsrf'),
            'X-Toja-Auth': get(authToken)
        }
    }
    if (obj) {
        settings['body'] = JSON.stringify({'data': obj});
    }
    return await window.fetch(url, settings);
}

export async function saveJsonApiObject(obj: JsonApiObject) {
    if (obj.id) {
        const response = await sendJsonApiRequest('PUT', '/api/' + obj.type + '/' + obj.id, obj);
        if (response.status === 200) {
            const data = await response.json() as JsonApiResponse;
            return data.data;
        } else {
            let data = null;
            try {
                data = await response.json();
            } catch (err) {
                throw new JsonApiException([{status: response.status.toString(), title: 'Network error'}]);
            }
            throw new JsonApiException(data.errors);
        }
    } else {
        const response = await sendJsonApiRequest('POST', '/api/' + obj.type, obj);
        if (response.status === 201) {
            const data = await response.json() as JsonApiResponse;
            return data.data;
        } else {
            let data = null;
            try {
                data = await response.json();
            } catch (err) {
                throw new JsonApiException([{status: response.status.toString(), title: 'Network error'}]);
            }
            throw new JsonApiException(data.errors);
        }
    }
}

export async function getJsonApiObject(type: string, id: string): Promise<JsonApiObject> {
    const response = await sendJsonApiRequest('GET', '/api/' + type + '/' + id, null);
    if (response.status === 200) {
        const data = await response.json() as JsonApiResponse;
        return data.data as JsonApiObject;
    } else {
        let data = null;
        try {
            data = await response.json();
        } catch (err) {
            throw new JsonApiException([{status: response.status.toString(), title: 'Network error'}]);
        }
        throw new JsonApiException(data.errors);
    }
}

export async function getJsonApiObjects(type: string): Promise<JsonApiObject[]> {
    const response = await sendJsonApiRequest('GET', '/api/' + type, null);
    if (response.status === 200) {
        const data = await response.json() as JsonApiResponse;
        return data.data as JsonApiObject[];
    } else {
        let data = null;
        try {
            data = await response.json();
        } catch (err) {
            throw new JsonApiException([{status: response.status.toString(), title: 'Network error'}]);
        }
        throw new JsonApiException(data.errors);
    }
}

export async function attemptAuthentication() {
    let auth = sessionLoadValue('auth', null) as NestedStorage;
    if (!auth) {
        auth = localLoadValue('auth', null) as NestedStorage;
    }
    if (auth) {
        authToken.set(auth.id + '$$' + auth.token);
        try {
            const user = await getJsonApiObject('users', auth.id as string);
            authUser.set(user);
        } catch {
            authToken.set('');
            authUser.set(null);
        }
    }
}

attemptAuthentication();
