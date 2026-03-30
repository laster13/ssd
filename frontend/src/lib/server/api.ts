import { PUBLIC_API_BASE_URL } from '$env/static/public';

export async function apiFetch(path: string, options: RequestInit = {}) {
	return fetch(`${PUBLIC_API_BASE_URL}${path}`, {
		...options,
		headers: {
			'Content-Type': 'application/json',
			...(options.headers ?? {})
		}
	});
}

export async function apiFetchWithAuth(token: string, path: string, options: RequestInit = {}) {
	return fetch(`${PUBLIC_API_BASE_URL}${path}`, {
		...options,
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`,
			...(options.headers ?? {})
		}
	});
}