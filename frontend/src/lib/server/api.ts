import { getServerBackendUrl } from '$lib/server/backend';

export async function apiFetch(path: string, init: RequestInit = {}) {
	const BACKEND_URL = getServerBackendUrl();
	return fetch(`${BACKEND_URL}${path}`, init);
}

export async function apiFetchWithAuth(token: string, path: string, init: RequestInit = {}) {
	const BACKEND_URL = getServerBackendUrl();
	const headers = new Headers(init.headers);

	headers.set('Authorization', `Bearer ${token}`);

	if (!headers.has('Content-Type') && init.body && !(init.body instanceof FormData)) {
		headers.set('Content-Type', 'application/json');
	}

	return fetch(`${BACKEND_URL}${path}`, {
		...init,
		headers
	});
}