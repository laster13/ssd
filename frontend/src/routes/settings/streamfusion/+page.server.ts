import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';

async function readApiError(response: Response, fallback: string): Promise<string> {
	try {
		const data = await response.json();
		if (typeof data?.detail === 'string' && data.detail.trim()) {
			return data.detail;
		}
	} catch {
		// no-op
	}

	return fallback;
}

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	return {};
};

export const actions: Actions = {
	create: async ({ locals, request, cookies, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const label = String(formData.get('label') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, '/me/streamfusion/tokens', {
			method: 'POST',
			body: JSON.stringify({
				label: label || null
			})
		});

		if (!response.ok) {
			return fail(response.status, {
				error: await readApiError(response, 'Impossible de créer le lien StreamFusion'),
				label
			});
		}

		const created = await response.json();

		return {
			created
		};
	}
};