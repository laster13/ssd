import { fail, redirect } from '@sveltejs/kit';

import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	return {};
};

export const actions: Actions = {
	generate: async ({ locals, request, cookies, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		try {
			const response = await apiFetchWithAuth(locals.token, '/pairing/register', {
				method: 'POST'
			});

			if (!response.ok) {
				return fail(response.status, {
					error:
						response.status === 429
							? 'Trop de codes générés récemment. Réessaie plus tard.'
							: 'Impossible de générer un code de connexion'
				});
			}

			const pairing = await response.json();

			return {
				pairing,
				success: true
			};
		} catch (err) {
			console.error('generate pairing failed', err);

			return fail(500, {
				error: 'Erreur interne pendant la génération du code'
			});
		}
	}
};