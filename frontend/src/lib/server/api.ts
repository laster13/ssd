import { getBackendUrl } from '$lib/public-config';

const BACKEND_URL = getBackendUrl();

export async function apiFetch(path: string, init: RequestInit = {}) {
	return fetch(`${BACKEND_URL}${path}`, init);
}

export async function apiFetchWithAuth(token: string, path: string, init: RequestInit = {}) {
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