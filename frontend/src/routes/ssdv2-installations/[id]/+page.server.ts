import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const [jobResponse, logsResponse, machinesResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, `/me/installations/${params.id}`, { method: 'GET' }),
		apiFetchWithAuth(locals.token, `/me/installations/${params.id}/logs`, { method: 'GET' }),
		apiFetchWithAuth(locals.token, '/me/machines', { method: 'GET' })
	]);

	if (!jobResponse.ok) {
		throw error(jobResponse.status, 'Installation SSDv2 introuvable');
	}

	const job = await jobResponse.json();

	if (String(job?.type ?? '') !== 'install_ssdv2') {
		throw error(404, 'Installation SSDv2 introuvable');
	}

	const logs = logsResponse.ok ? await logsResponse.json() : [];
	const machines = machinesResponse.ok ? await machinesResponse.json() : [];

	const machine = Array.isArray(machines)
		? machines.find((item: any) => String(item?.id) === String(job?.machine_id)) ?? null
		: null;

	return {
		job,
		logs,
		machine
	};
};
