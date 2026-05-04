import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const GET: RequestHandler = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		return json({ links: [] }, { status: 200 });
	}

	const response = await apiFetchWithAuth(locals.token, '/notifications/unread-topic-links');

	if (!response.ok) {
		return json({ links: [] }, { status: 200 });
	}

	const payload = await response.json();
	return json({
		links: Array.isArray(payload?.links) ? payload.links : []
	});
};