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
	const image = incoming.get('image');

	if (!(image instanceof File)) {
		return json({ error: 'Aucun fichier reçu.' }, { status: 400 });
	}

	const formData = new FormData();
	formData.set('image', image);

	const response = await apiFetchWithAuth(locals.token, '/forum/uploads/image', {
		method: 'POST',
		body: formData
	});

	if (!response.ok) {
		let error = "Impossible d'envoyer l'image.";
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
	const markdown = `![image](${publicPath})`;

	return json({
		ok: true,
		storage_path: payload.storage_path,
		public_url: publicPath,
		markdown
	});
};