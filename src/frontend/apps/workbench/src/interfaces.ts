export interface State {
    baseURL: string;
    sourceId: string;
    source: object;
    jokes: Joke[];
}

export interface Config {
    baseURL: string;
    sourceId: string;
}

export interface Joke {
    type: string;
    id: number;
    attributes: JokeAttributes;
}

export interface JokeAttributes {
    parent_id: number;
    bbox: BBox;
}

export interface BBox {
    top: number;
    left: number;
    width: number;
    height: number;
}
