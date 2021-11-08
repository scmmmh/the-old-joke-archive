import axios from 'axios';

const databaseBaseUrl = 'http://main:aiZiojoh7Eux@localhost:5984';

export async function dropDatabase(databaseName) {
    try {
        await axios.delete(databaseBaseUrl + '/' + databaseName);
    } catch {}
}

export async function createDatabase(databaseName) {
    try {
        await axios.put(databaseBaseUrl + '/' + databaseName);
    } catch {}
}

export async function createRecord(databaseName, record) {
    return await axios.post(databaseBaseUrl + '/' + databaseName, record);
}

export async function getAllRecords(databaseName) {
    const response = await axios.get(databaseBaseUrl + '/' + databaseName + '/_all_docs');
    return response.data;
}

export async function getRecord(databaseName, recordId) {
    const response = await axios.get(databaseBaseUrl + '/' + databaseName + '/' + recordId);
    return response.data;
}

export async function setupEmptyDatabase() {
    await createDatabase('_users');
    await createDatabase('_replicator');

    await dropDatabase('users');
    await createDatabase('users');
}

export async function setupMinimalDatabase() {
    await setupEmptyDatabase();

    const objs = {};
    let response = await createRecord('users', {'email': 'admin@example.com', 'name': 'Admin User', 'token': 'adminToken', 'groups': ['admin']});
    objs.admin = response.data;

    return objs;
}
