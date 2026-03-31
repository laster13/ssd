import { fail, redirect, error } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { getBackendUrl } from '$lib/public-config';

const BACKEND_URL = getBackendUrl();

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const response = await apiFetchWithAuth(locals.token, '/pairing/register', {
		method: 'POST'
	});

	if (!response.ok) {
		throw error(response.status, 'Impossible de générer un code de connexion');
	}

	const pairing = await response.json();

	return {
		pairing,
		backendUrl: BACKEND_URL
	};
};

export const actions: Actions = {
	regenerate: async ({ locals }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const response = await apiFetchWithAuth(locals.token, '/pairing/register', {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, {
				error: 'Impossible de générer un nouveau code de connexion'
			});
		}

		const pairing = await response.json();

		return {
			pairing,
			backendUrl: BACKEND_URL,
			success: true
		};
	}
};