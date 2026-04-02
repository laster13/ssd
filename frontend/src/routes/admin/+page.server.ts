import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';

export const load: PageServerLoad = async ({ locals }) => {
	const [jobsResponse, machinesResponse, usersResponse] = await Promise.all([
		apiFetchWithAuth(locals.token!, '/admin/jobs', { method: 'GET' }),
		apiFetchWithAuth(locals.token!, '/admin/machines', { method: 'GET' }),
		apiFetchWithAuth(locals.token!, '/admin/users', { method: 'GET' })
	]);

	const jobs = jobsResponse.ok ? await jobsResponse.json() : [];
	const machines = machinesResponse.ok ? await machinesResponse.json() : [];
	const users = usersResponse.ok ? await usersResponse.json() : [];

	return { user: locals.user, jobs, machines, users };
};

export const actions: Actions = {
	grantAdmin: async ({ request, cookies, locals, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const userId = String(formData.get('user_id') ?? '').trim();
		if (!userId) {
			return fail(400, { error: 'Utilisateur manquant' });
		}

		const response = await apiFetchWithAuth(locals.token, `/admin/users/${userId}/grant-admin`, {
			method: 'POST'
		});

		if (!response.ok) {
			let message = "Impossible d'ajouter cet admin";
			try {
				const payload = await response.json();
				if (typeof payload?.detail === 'string') {
					message = payload.detail;
				}
			} catch {
				// no-op
			}

			return fail(response.status, { error: message });
		}

		return { success: true };
	}
};