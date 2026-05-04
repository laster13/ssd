import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const POST: RequestHandler = async ({ request, locals }) => {
	if (!locals.user || !locals.token) {
		return json({ error: 'Non authentifié.' }, { status: 401 });
	}

	const body = await request.json().catch(() => null);
	const link = typeof body?.link === 'string' ? body.link.trim() : '';

	if (!link) {
		return json({ error: 'Lien manquant.' }, { status: 400 });
	}

	const response = await apiFetchWithAuth(locals.token, '/notifications/mark-link-read', {
		method: 'POST',
		body: JSON.stringify({ link })
	});

	if (!response.ok) {
		let error = 'Impossible de marquer ces notifications comme lues.';
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

	return json({ ok: true });
};