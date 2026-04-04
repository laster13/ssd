import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals, url }) => {
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

	const initialTab = url.searchParams.get('tab') === 'history' ? 'history' : 'applications';

	const rawFilter = url.searchParams.get('filter');
	const initialFilter =
		rawFilter === 'running' ||
		rawFilter === 'completed' ||
		rawFilter === 'failed' ||
		rawFilter === 'all'
			? rawFilter
			: 'all';

	return {
		jobs,
		machines,
		initialTab,
		initialFilter
	};
};

export const actions: Actions = {
	deleteInstallation: async ({ request, locals }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await request.formData();
		const jobId = String(formData.get('job_id') ?? '').trim();

		if (!jobId) {
			return fail(400, {
				deleteError: 'Identifiant du job manquant.'
			});
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

		return {
			deleteSuccess: 'Job supprimé de l’historique.'
		};
	}
};