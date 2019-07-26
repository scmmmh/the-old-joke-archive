export interface State {
    baseURL: string;
    sourceId: number | null;
    userId: number | null;
    source: object;
    jokes: Joke[];
    selected: Joke | null;
}

export interface Config {
    baseURL: string;
    sourceId: number | null;
    userId: number | null;
}

export interface Joke {
    type: string;
    id: number;
    attributes: JokeAttributes;
}

export interface JokeAttributes {
    parent_id: number;
    owner_id: number;
    bbox: BBox;
}

export interface BBox {
    top: number;
    left: number;
    width: number;
    height: number;
}
