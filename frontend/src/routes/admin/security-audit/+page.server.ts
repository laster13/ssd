import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	if (!locals.user.is_admin) {
		throw redirect(303, '/');
	}

	const response = await apiFetchWithAuth(locals.token, '/admin/security-audit', {
		method: 'GET'
	});

	const logs = response.ok ? await response.json() : [];

	return {
		user: locals.user,
		logs
	};
};
