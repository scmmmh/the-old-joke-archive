export class JsonApiException extends Error {
    public errors = [] as JsonApiError[];

    constructor(errors: JsonApiError[]) {
        super('JSONAPI Error');
        this.errors = errors;
    }
}

export async function saveJsonApiObject(obj: JsonApiObject) {
    if (obj['_id']) {
        const response = await window.fetch('/' + obj.type + '/' + obj['_id'], {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'data': obj})
        });
        if (response.status === 201) {
            const data = await response.json() as JsonApiResponse;
            return data.data;
        } else {
            try {
                const data = await response.json();
                throw new JsonApiException(data.errors);
            } catch {
                throw new JsonApiException([{status: response.status.toString(), title: 'Network error'}]);
            }
        }
    } else {
        const response = await window.fetch('/' + obj.type, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({'data': obj})
        });
        if (response.status === 201) {
            const data = await response.json() as JsonApiResponse;
            return data.data;
        } else {
            try {
                const data = await response.json();
                throw new JsonApiException(data.errors);
            } catch {
                throw new JsonApiException([{status: response.status.toString(), title: 'Network error'}]);
            }
        }
    }
}
