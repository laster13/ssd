import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const response = await apiFetchWithAuth(locals.token, '/me/machines', {
		method: 'GET'
	});

	if (!response.ok) {
		throw error(response.status, 'Impossible de charger les serveurs');
	}

	const servers = await response.json();

	return {
		servers
	};
};