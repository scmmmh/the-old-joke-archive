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

export async function saveJsonApiObject(obj: JsonApiObject) {
    if (obj['_id']) {
        const response = await window.fetch('/api/' + obj.type + '/' + obj['_id'], {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-XSRFToken': getCookie('_xsrf'),
            },
            body: JSON.stringify({'data': obj})
        });
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
    } else {
        const response = await window.fetch('/api/' + obj.type, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-XSRFToken': getCookie('_xsrf'),
            },
            body: JSON.stringify({'data': obj})
        });
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
