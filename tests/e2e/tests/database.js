import axios from 'axios';
import bcrypt from 'bcrypt';

const databaseBaseUrl = 'http://main:aiZiojoh7Eux@localhost:5984';
const passwordCache = {};

async function hashPassword(password) {
    if (!passwordCache[password]) {
        passwordCache[password] = await bcrypt.hash(password, 12);
    }
    return passwordCache[password];
}

function hexString(length) {
    const characters = []
    for (let idx = 0; idx < length; idx++) {
        characters.push(Math.floor(Math.random() * 16).toString(16))
    }
    return characters.join('');
}

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
    const response = await axios.post(databaseBaseUrl + '/' + databaseName, record);
    return await getRecord(databaseName, response.data.id);
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
    objs.admin = await createRecord('users', {
        'email': 'admin@example.com',
        'name': 'Admin User',
        'tokens': [
            {
                'token': hexString(128),
                'timestamp': Date.UTC(),
            }
        ],
        'password': await hashPassword('admin1pwd'),
        'groups': ['admin'],
        'status': 'active',
    });

    return objs;
}

export async function setupStandardDatabase() {
    const objs = await setupMinimalDatabase();

    objs.user1 = await createRecord('users', {
        'email': 'test1@example.com',
        'name': 'User One',
        'tokens': [
            {
                'token': hexString(128),
                'timestamp': Date.UTC(),
            }
        ],
        'password': await hashPassword('user1pwd'),
        'groups': [],
        'status': 'active'
    });
    objs.userNew = await createRecord('users', {
        'email': 'test_new@example.com',
        'name': 'User New',
        'tokens': [
            {
                'token': hexString(128),
                'timestamp': Date.UTC(),
            }
        ],
        'password': await hashPassword('userNewpwd'),
        'groups': [],
        'status': 'new'
    });
    objs.userLocked = await createRecord('users', {
        'email': 'test_locked@example.com',
        'name': 'User Locked',
        'tokens': [
            {
                'token': hexString(128),
                'timestamp': Date.UTC(),
            }
        ],
        'password': await hashPassword('userLockedpwd'),
        'groups': [],
        'status': 'locked'
    });
    objs.userBlocked = await createRecord('users', {
        'email': 'test_locked@example.com',
        'name': 'User Blocked',
        'tokens': [
            {
                'token': hexString(128),
                'timestamp': Date.UTC(),
            }
        ],
        'password': await hashPassword('userBlockedpwd'),
        'groups': [],
        'status': 'blocked'
    });

    return objs;
}
