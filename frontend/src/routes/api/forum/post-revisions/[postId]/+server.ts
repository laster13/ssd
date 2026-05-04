import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const GET: RequestHandler = async ({ locals, params }) => {
	if (!locals.user || !locals.token) {
		return json({ error: 'Non authentifié.' }, { status: 401 });
	}

	const response = await apiFetchWithAuth(
		locals.token,
		`/forum/posts/${params.postId}/revisions`
	);

	if (!response.ok) {
		let error = "Impossible de charger l'historique du message.";
		try {
			const payload = await response.json();
			if (typeof payload?.detail === 'string' && payload.detail.trim()) {
				error = payload.detail.trim();
			}
		} catch {
			// noop
		}
		return json({ error }, { status: response.status });
	}

	const payload = await response.json();
	return json(payload);
};