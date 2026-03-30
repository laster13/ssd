import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const [jobsResponse, machinesResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, '/me/installations', {
			method: 'GET'
		}),
		apiFetchWithAuth(locals.token, '/me/machines', {
			method: 'GET'
		})
	]);

	const jobs = jobsResponse.ok ? await jobsResponse.json() : [];
	const machines = machinesResponse.ok ? await machinesResponse.json() : [];

	return {
		jobs,
		machines
	};
};
