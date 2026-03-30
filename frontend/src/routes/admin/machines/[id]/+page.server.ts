import { redirect, error, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	if (!locals.user.is_admin) {
		throw redirect(303, '/');
	}

	const [machineResponse, jobsResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, `/admin/machines/${params.id}`, { method: 'GET' }),
		apiFetchWithAuth(locals.token, `/admin/machines/${params.id}/jobs`, { method: 'GET' })
	]);

	if (!machineResponse.ok) {
		throw error(machineResponse.status, 'Machine introuvable');
	}

	const machine = await machineResponse.json();
	const jobs = jobsResponse.ok ? await jobsResponse.json() : [];

	return {
		user: locals.user,
		machine,
		jobs
	};
};

export const actions: Actions = {
	createJob: async ({ locals, params, request }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		if (!locals.user.is_admin) {
			return fail(403, { error: 'Accès admin requis' });
		}

		const formData = await request.formData();
		const app_slug = String(formData.get('app_slug') ?? '').trim();
		const subdomain = String(formData.get('subdomain') ?? '').trim();
		const auth_type = String(formData.get('auth_type') ?? '').trim();

		if (!app_slug || !subdomain || !auth_type) {
			return fail(400, {
				error: 'Tous les champs sont requis',
				app_slug,
				subdomain,
				auth_type
			});
		}

		const response = await apiFetchWithAuth(locals.token, `/admin/machines/${params.id}/jobs`, {
			method: 'POST',
			body: JSON.stringify({
				app_slug,
				subdomain,
				auth_type
			})
		});

		if (!response.ok) {
			return fail(response.status, {
				error: 'Impossible de créer le job',
				app_slug,
				subdomain,
				auth_type
			});
		}

		const data = await response.json();
		const jobId = data.job_id;

		if (!jobId) {
			return fail(500, { error: 'Réponse invalide du backend' });
		}

		throw redirect(303, `/admin/jobs/${jobId}`);
	}
};