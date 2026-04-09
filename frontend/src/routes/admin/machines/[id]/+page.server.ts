import { redirect, error, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { ensureCsrfCookie, validateCsrf } from '$lib/server/security';

function getPublicWebSocketOrigin(origin: string): string {
	const url = new URL(origin);
	url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
	return url.origin;
}

export const load: PageServerLoad = async ({ locals, params, cookies, url }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	if (!locals.user.is_admin) {
		throw redirect(303, '/');
	}

	const csrfToken = ensureCsrfCookie(cookies, locals.token);

	const [machineResponse, jobsResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, `/admin/machines/${params.id}`, { method: 'GET' }),
		apiFetchWithAuth(locals.token, `/admin/machines/${params.id}/jobs`, { method: 'GET' })
	]);

	if (!machineResponse.ok) {
		throw error(machineResponse.status, 'Machine introuvable');
	}

	const machine = await machineResponse.json();
	const jobs = jobsResponse.ok ? await jobsResponse.json() : [];
	const machineSocketUrl = `${getPublicWebSocketOrigin(url.origin)}/ws/machines?token=${encodeURIComponent(locals.token)}`;

	return { user: locals.user, machine, jobs, csrfToken, machineSocketUrl };
};

export const actions: Actions = {
	createJob: async ({ locals, params, request, cookies, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		if (!locals.user.is_admin) {
			return fail(403, { error: 'Accès admin requis' });
		}

		const formData = await validateCsrf({ request, cookies, url, sessionToken: locals.token });
		const app_slug = String(formData.get('app_slug') ?? '').trim();
		const subdomain = String(formData.get('subdomain') ?? '').trim();
		const auth_type = String(formData.get('auth_type') ?? '').trim();

		if (!app_slug || !subdomain || !auth_type) {
			return fail(400, { error: 'Tous les champs sont requis', app_slug, subdomain, auth_type });
		}

		const response = await apiFetchWithAuth(locals.token, `/admin/machines/${params.id}/jobs`, {
			method: 'POST',
			body: JSON.stringify({ app_slug, subdomain, auth_type })
		});

		if (!response.ok) {
			let message = 'Impossible de créer le job';
			try {
				const data = await response.json();
				if (typeof data?.detail === 'string') {
					message = data.detail;
				}
			} catch {
				// ignore
			}
			return fail(response.status, { error: message, app_slug, subdomain, auth_type });
		}

		const data = await response.json();
		const jobId = data.job_id;

		if (!jobId) {
			return fail(500, { error: 'Réponse invalide du backend' });
		}

		throw redirect(303, `/admin/jobs/${jobId}`);
	},

	rotateToken: async ({ locals, params, request, cookies, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		if (!locals.user.is_admin) {
			return fail(403, { error: 'Accès admin requis' });
		}

		await validateCsrf({ request, cookies, url, sessionToken: locals.token });

		const response = await apiFetchWithAuth(locals.token, `/admin/machines/${params.id}/rotate-token`, {
			method: 'POST'
		});

		if (!response.ok) {
			let message = 'Impossible de rotater le token machine';
			try {
				const data = await response.json();
				if (typeof data?.detail === 'string') {
					message = data.detail;
				}
			} catch {
				// ignore
			}
			return fail(response.status, { error: message });
		}

		const data = await response.json();
		return { rotated: true, rotatedToken: data.machine_token };
	},

	revokeMachine: async ({ locals, params, request, cookies, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		if (!locals.user.is_admin) {
			return fail(403, { error: 'Accès admin requis' });
		}

		await validateCsrf({ request, cookies, url, sessionToken: locals.token });

		const response = await apiFetchWithAuth(locals.token, `/admin/machines/${params.id}/revoke-token`, {
			method: 'POST'
		});

		if (!response.ok) {
			let message = 'Impossible de révoquer la machine';
			try {
				const data = await response.json();
				if (typeof data?.detail === 'string') {
					message = data.detail;
				}
			} catch {
				// ignore
			}
			return fail(response.status, { error: message });
		}

		return { revoked: true };
	}
};
