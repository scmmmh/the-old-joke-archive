import { request as nodeRequest } from 'http';

export async function request(url: string) {
    return new Promise((resolve, reject) => {
        const req = nodeRequest(url, (res) => {
            if (res.statusCode === 200) {
                resolve();
            } else {
                reject();
            }
        });
        req.end();
    });
}
