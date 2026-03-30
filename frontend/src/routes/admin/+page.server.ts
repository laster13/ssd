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

	const [jobsResponse, machinesResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, '/admin/jobs', { method: 'GET' }),
		apiFetchWithAuth(locals.token, '/admin/machines', { method: 'GET' })
	]);

	const jobs = jobsResponse.ok ? await jobsResponse.json() : [];
	const machines = machinesResponse.ok ? await machinesResponse.json() : [];

	return {
		user: locals.user,
		jobs,
		machines
	};
};