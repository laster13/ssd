import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

import { apiFetchWithAuth } from '$lib/server/api';

export const POST: RequestHandler = async ({ request, locals, url }) => {
	if (!locals.user || !locals.token) {
		return json({ error: 'Non authentifié.' }, { status: 401 });
	}

	const origin = request.headers.get('origin');
	if (origin && origin !== url.origin) {
		return json({ error: 'Origine non autorisée.' }, { status: 403 });
	}

	const incoming = await request.formData();
	const file = incoming.get('file');

	if (!(file instanceof File)) {
		return json({ error: 'Aucun fichier reçu.' }, { status: 400 });
	}

	const formData = new FormData();
	formData.set('file', file);

	const response = await apiFetchWithAuth(locals.token, '/forum/uploads/file', {
		method: 'POST',
		body: formData
	});

	if (!response.ok) {
		let error = "Impossible d'envoyer le fichier.";

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
	const publicPath = `/forum-assets/${payload.storage_path}`;
	const markdown = `[${payload.original_name ?? payload.file_name}](${publicPath})`;

	return json({
		ok: true,
		file_name: payload.file_name,
		original_name: payload.original_name ?? payload.file_name,
		storage_path: payload.storage_path,
		public_url: publicPath,
		markdown
	});
};