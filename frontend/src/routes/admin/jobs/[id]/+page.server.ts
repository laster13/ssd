import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	if (!locals.user.is_admin) {
		throw redirect(303, '/');
	}

	const [jobResponse, logsResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, `/admin/jobs/${params.id}`, { method: 'GET' }),
		apiFetchWithAuth(locals.token, `/admin/jobs/${params.id}/logs`, { method: 'GET' })
	]);

	if (!jobResponse.ok) {
		throw error(jobResponse.status, 'Job introuvable');
	}

	const job = await jobResponse.json();
	const logs = logsResponse.ok ? await logsResponse.json() : [];

	return {
		user: locals.user,
		job,
		logs
	};
};