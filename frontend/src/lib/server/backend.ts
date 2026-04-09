import { env } from '$env/dynamic/private';

function normalize(url: string): string {
	return url.replace(/\/+$/, '');
}

export function getServerBackendUrl(): string {
	return normalize(env.BACKEND_URL || 'http://127.0.0.1:8000');
}

export function getServerBackendWsUrl(): string {
	const url = getServerBackendUrl();
	if (url.startsWith('https://')) {
		return `wss://${url.slice('https://'.length)}`;
	}
	if (url.startsWith('http://')) {
		return `ws://${url.slice('http://'.length)}`;
	}
	return url;
}
