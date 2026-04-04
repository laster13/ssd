import { env } from '$env/dynamic/private';

function normalize(url: string): string {
	return url.replace(/\/+$/, '');
}

export function getServerBackendUrl(): string {
	return normalize(env.BACKEND_URL || 'http://127.0.0.1:8000');
}