import type { RequestHandler } from './$types';
import { apiFetch } from '$lib/server/api';

export const GET: RequestHandler = async ({ params }) => {
	const path = typeof params.path === 'string' ? params.path : '';

	const response = await apiFetch(`/uploads/${path}`);

	if (!response.ok) {
		return new Response('Not found', { status: response.status });
	}

	const body = await response.arrayBuffer();
	const contentType = response.headers.get('content-type') ?? 'application/octet-stream';
	const cacheControl = response.headers.get('cache-control') ?? 'public, max-age=31536000, immutable';

	return new Response(body, {
		status: 200,
		headers: {
			'content-type': contentType,
			'cache-control': cacheControl
		}
	});
};