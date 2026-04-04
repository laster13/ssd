import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const [jobsResponse, machinesResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, '/me/installations', { method: 'GET' }),
		apiFetchWithAuth(locals.token, '/me/machines', { method: 'GET' })
	]);

	const jobsPayload = jobsResponse.ok ? await jobsResponse.json() : [];
	const machinesPayload = machinesResponse.ok ? await machinesResponse.json() : [];

	const machines = Array.isArray(machinesPayload) ? machinesPayload : [];
	const jobs = (Array.isArray(jobsPayload) ? jobsPayload : [])
		.filter((job: any) => String(job?.type ?? '') === 'install_ssdv2')
		.sort((a: any, b: any) => {
			const aTime = new Date(String(a?.created_at ?? 0)).getTime();
			const bTime = new Date(String(b?.created_at ?? 0)).getTime();
			return bTime - aTime;
		})
		.map((job: any) => {
			const machine =
				machines.find((item: any) => String(item?.id) === String(job?.machine_id)) ?? null;

			return {
				...job,
				machine
			};
		});

	return {
		jobs
	};
};
