/// <reference types="svelte" />

/**
 * Generic JSONAPI types.
 */
type JsonApiResponse = {
    data?: JsonApiObject | JsonApiObject[],
    errors?: JsonApiError[],
};

type JsonApiObject = {
    type: string,
    id?: string,
    attributes?: JsonApiAttributeDict,
    relationships?: {[key: string]: JsonApiObjectRelationship}
};

type JsonApiAttributeDict = {
    [key: string]: any,
};

type JsonApiObjectRelationship = {
    data: JsonApiObjectReference | JsonApiObjectReference[];
}

type JsonApiObjectReference = {
    type: string;
    id: string;
}

type JsonApiError = {
    status: string,
    code?: string,
    title: string,
    detail?: string,
    source?: JsonApiErrorSource,
};

type JsonApiErrorSource = {
    pointer: string,
};

/**
 * Types for user documents.
 */
type UserDocumentReference = {
    type: 'users';
    id: string;
};

/**
 * Types for source documents.
 */
type SourceDocumentReference = {
    type: 'sources',
    id: string,
};

type SourceDocument = {
    type: 'sources';
    id?: string,
    attributes: SourceDocumentAttributes;
    relationships: SourceDocumentRelationships;
};

type SourceDocumentAttributes = {
    type: 'book' | 'newspaper';
    title: string;
    subtitle: string;
    date: string;
    location: string;
    publisher: string;
    page_numbers: string;
    data: string;
    created: number;
};

type SourceDocumentRelationships = {
    creator: {data: UserDocumentReference},
    jokes: {data: JokeDocumentReference[]},
};

/**
 * Types for joke documents.
 */
type JokeDocumentReference = {
    type: 'jokes',
    id: string,
};

type JokeDocument = {
    type: 'jokes',
    id?: string,
    attributes: JokeDocumentAttributes | JokeUpdateAttributes,
    relationships: JokeDocumentRelationships,
};

type JokeDocumentAttributes = {
    title: string,
    coordinates: number[],
    transcriptions: JokeDocumentTranscriptions,
    categories: string[],
    topics: string,
    language: string,
};

type JokeUpdateAttributes = {
    actions: JokeUpdateAction[],
};

type JokeUpdateAction = JokeUpdateCoordinates | JokeUpdateAnnotated | JokeUpdateCategories | JokeUpdateTopics | JokeUpdateLanguage | JokeUpdateStatus;

type JokeUpdateAnnotated = {
    annotated: TiptapNode;
};

type JokeUpdateStatus = {
    status: 'annotated';
};

type JokeUpdateCoordinates = {
    coordinates: number[],
};

type JokeUpdateCategories = {
    categories: string[];
};

type JokeUpdateTopics = {
    topics: string;
};

type JokeUpdateLanguage = {
    language: string;
};

type JokeDocumentTranscriptions = {
    auto?: TiptapNode,
    final?: TiptapNode,
    [x: string]: TiptapNode,
};

type TiptapNode = {
    type: 'doc' | 'paragraph' | 'text',
    content?: TiptapNode[],
    text?: '',
};

type JokeDocumentRelationships = {
    source: {data: SourceDocumentReference},
};
