/// <reference types="svelte" />

interface JsonApiResponse {
    data?: JsonApiObject | JsonApiObject[];
    errors?: JsonApiError[];
}

interface JsonApiObject {
    type: string;
    id?: string;
    attributes?: {[key: string]: string};
}

interface JsonApiError {
    status: string;
    code?: string;
    title: string;
    detail?: string;
    source?: JsonApiErrorSource;
}

interface JsonApiErrorSource {
    pointer: string;
}
