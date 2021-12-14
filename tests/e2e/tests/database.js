import axios from 'axios';

const databaseBaseUrl = 'http://main:aiZiojoh7Eux@localhost:5984';

export async function createRecord(databaseName, record) {
    const response = await axios.post(databaseBaseUrl + '/' + databaseName, record);
    return await getRecord(databaseName, response.data.id);
}

export async function getAllRecords(databaseName) {
    const response = await axios.get(databaseBaseUrl + '/' + databaseName + '/_all_docs');
    response.data.obj_rows = response.data.rows.filter((row) => {
        return !row.id.startsWith('_design');
    });
    return response.data;
}

export async function getRecord(databaseName, recordId) {
    const response = await axios.get(databaseBaseUrl + '/' + databaseName + '/' + recordId);
    return response.data;
}

export async function createTestRecords(names) {
    const response = await axios.put('http://localhost:6543/test?' + names.map((name) => { return 'obj=' + name; }).join('&'));
    const data = response.data;
    for (let db_key of Object.keys(data)) {
        for (let [item_key, item_id] of Object.entries(data[db_key])) {
            data[db_key][item_key] = await getRecord(db_key, item_id);
        }
    }
    return data
}

export function mergeTestRecords(a, b) {
    const result = {};
    for (let [obj_key, obj_values] of Object.entries(a)) {
        result[obj_key] = {...obj_values}
    }
    for (let [obj_key, obj_values] of Object.entries(b)) {
        if (result[obj_key]) {
            result[obj_key] = {...result[obj_key], ...obj_values}
        } else {
            result[obj_key] = {...obj_values}
        }
    }
    return result;
}

export async function setupEmptyDatabase() {
    await axios.delete('http://localhost:6543/test');
    await axios.post('http://localhost:6543/test');
}

export async function setupMinimalDatabase() {
    await setupEmptyDatabase();
    const objs = createTestRecords(['admin']);
    return objs;
}

export async function setupStandardDatabase() {
    let objs = await setupMinimalDatabase();
    objs = mergeTestRecords(objs, await createTestRecords(['user1', 'userNew', 'userInactive', 'userBlocked', 'source1', 'source2']))
    return objs;
}
