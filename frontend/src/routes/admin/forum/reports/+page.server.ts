import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login?next=/admin/forum/reports');
	}

	const status = url.searchParams.get('status')?.trim() || '';
	const params = new URLSearchParams();
	if (status) params.set('status', status);

	const response = await apiFetchWithAuth(
		locals.token,
		params.toString() ? `/forum/reports?${params.toString()}` : '/forum/reports'
	);

	if (!response.ok) {
		if (response.status === 403) {
			throw redirect(303, '/forum');
		}

		return {
			reports: [],
			status,
			loadError: "Impossible de charger les signalements."
		};
	}

	const reports = await response.json();

	return {
		reports,
		status,
		loadError: null
	};
};

export const actions: Actions = {
	resolveReport: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, { error: 'Connexion requise.' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const reportId = String(formData.get('report_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/reports/${reportId}/resolve`, {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, { error: 'Impossible de résoudre ce signalement.' });
		}

		return { ok: true };
	},

	dismissReport: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, { error: 'Connexion requise.' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const reportId = String(formData.get('report_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/reports/${reportId}/dismiss`, {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, { error: 'Impossible d’ignorer ce signalement.' });
		}

		return { ok: true };
	},

	deletePost: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, { error: 'Connexion requise.' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const postId = String(formData.get('post_id') ?? '').trim();
		const reportId = String(formData.get('report_id') ?? '').trim();

		const deleteResponse = await apiFetchWithAuth(locals.token, `/forum/posts/${postId}`, {
			method: 'DELETE'
		});

		if (!deleteResponse.ok) {
			return fail(deleteResponse.status, { error: 'Impossible de supprimer le message.' });
		}

		if (reportId) {
			await apiFetchWithAuth(locals.token, `/forum/reports/${reportId}/resolve`, {
				method: 'POST'
			});
		}

		return { ok: true };
	}
};