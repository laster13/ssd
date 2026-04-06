import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const [applicationsResponse, jobsResponse, machinesResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, '/me/applications', { method: 'GET' }),
		apiFetchWithAuth(locals.token, '/me/installations', { method: 'GET' }),
		apiFetchWithAuth(locals.token, '/me/machines', { method: 'GET' })
	]);

	const applications = applicationsResponse.ok ? await applicationsResponse.json() : [];
	const jobs = jobsResponse.ok ? await jobsResponse.json() : [];
	const machines = machinesResponse.ok ? await machinesResponse.json() : [];

	const initialTab = url.searchParams.get('tab') === 'history' ? 'history' : 'applications';
	const rawFilter = url.searchParams.get('filter');
	const initialFilter =
		rawFilter === 'running' ||
		rawFilter === 'completed' ||
		rawFilter === 'failed' ||
		rawFilter === 'all'
			? rawFilter
			: 'all';

	return { applications, jobs, machines, initialTab, initialFilter };
};

export const actions: Actions = {
	deleteInstallation: async ({ request, locals }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await request.formData();
		const jobId = String(formData.get('job_id') ?? '').trim();

		if (!jobId) {
			return fail(400, { deleteError: 'Identifiant du job manquant.' });
		}

		const response = await apiFetchWithAuth(locals.token, `/me/installations/${jobId}`, {
			method: 'DELETE'
		});

		if (!response.ok) {
			let deleteError = 'Impossible de supprimer ce job.';
			try {
				const payload = await response.json();
				if (typeof payload?.detail === 'string' && payload.detail.trim()) {
					deleteError = payload.detail.trim();
				}
			} catch {
				// noop
			}
			return fail(response.status, { deleteError });
		}

		return { deleteSuccess: 'Job supprimé de l’historique.' };
	},

	uninstallApplication: async ({ request, locals }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await request.formData();
		const machineId = String(formData.get('machine_id') ?? '').trim();
		const appSlug = String(formData.get('app_slug') ?? '').trim();

		if (!machineId || !appSlug) {
			return fail(400, { uninstallError: 'Informations de désinstallation manquantes.' });
		}

		const response = await apiFetchWithAuth(locals.token, '/me/uninstallations', {
			method: 'POST',
			body: JSON.stringify({ machine_id: machineId, app_slug: appSlug })
		});

		if (!response.ok) {
			let uninstallError = 'Impossible de lancer la désinstallation.';
			try {
				const payload = await response.json();
				if (typeof payload?.detail === 'string' && payload.detail.trim()) {
					uninstallError = payload.detail.trim();
				}
			} catch {
				// noop
			}
			return fail(response.status, { uninstallError });
		}

		const payload = await response.json();
		const jobId = String(payload?.job_id ?? '').trim();

		if (!jobId) {
			return fail(500, {
				uninstallError: 'La désinstallation a été créée, mais aucun job_id n’a été retourné.'
			});
		}

		throw redirect(303, `/uninstallations/${jobId}`);
	}
};