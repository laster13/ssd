import { error, fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';

function normalizeBoolean(value: FormDataEntryValue | null): boolean {
	if (value === null) return false;

	const normalized = String(value).trim().toLowerCase();
	return normalized === 'true' || normalized === '1' || normalized === 'on' || normalized === 'yes';
}

function asString(value: FormDataEntryValue | null): string {
	return String(value ?? '').trim();
}

export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const [machinesResponse, settingsResponse, jobsResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, '/me/machines', { method: 'GET' }),
		apiFetchWithAuth(locals.token, `/me/machines/${params.id}/settings`, { method: 'GET' }),
		apiFetchWithAuth(locals.token, '/me/installations', { method: 'GET' })
	]);

	if (!machinesResponse.ok) {
		throw error(machinesResponse.status, 'Impossible de charger le serveur');
	}

	if (!settingsResponse.ok) {
		throw error(settingsResponse.status, 'Impossible de charger la configuration du serveur');
	}

	const machines = await machinesResponse.json();
	const settings = await settingsResponse.json();
	const jobs = jobsResponse.ok ? await jobsResponse.json() : [];

	const normalizedMachines = Array.isArray(machines) ? machines : [];
	const machine = normalizedMachines.find((item: any) => String(item?.id) === params.id);

	if (!machine) {
		throw error(404, 'Serveur introuvable');
	}

	const latestSsdv2Job = (Array.isArray(jobs) ? jobs : [])
		.filter(
			(item: any) =>
				String(item?.machine_id ?? '') === params.id && String(item?.type ?? '') === 'install_ssdv2'
		)
		.sort((a: any, b: any) => {
			const aTime = new Date(String(a?.created_at ?? 0)).getTime();
			const bTime = new Date(String(b?.created_at ?? 0)).getTime();
			return bTime - aTime;
		})[0] ?? null;

	return {
		machine,
		settings,
		latestSsdv2Job,
		saveSuccess: false
	};
};

export const actions: Actions = {
	save: async ({ request, cookies, locals, url, params }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const payload = {
			username: asString(formData.get('username')),
			email: asString(formData.get('email')),
			domain: asString(formData.get('domain')),
			password: asString(formData.get('password')),
			cloudflare_login: asString(formData.get('cloudflare_login')),
			cloudflare_api_key: asString(formData.get('cloudflare_api_key')),
			oauth_enabled: normalizeBoolean(formData.get('oauth_enabled')),
			oauth_client: asString(formData.get('oauth_client')),
			oauth_secret: asString(formData.get('oauth_secret')),
			oauth_mail: asString(formData.get('oauth_mail'))
		};

		const response = await apiFetchWithAuth(locals.token, `/me/machines/${params.id}/settings`, {
			method: 'PATCH',
			body: JSON.stringify(payload)
		});

		if (!response.ok) {
			let message = 'Impossible de sauvegarder la configuration du serveur';

			try {
				const apiError = await response.json();
				if (typeof apiError?.detail === 'string' && apiError.detail.trim()) {
					message = apiError.detail;
				}
			} catch {
				// no-op
			}

			return fail(response.status, {
				error: message,
				values: payload
			});
		}

		const settings = await response.json();

		return {
			success: true,
			settings
		};
	},

	install: async ({ request, cookies, locals, url, params }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const response = await apiFetchWithAuth(
			locals.token,
			`/me/machines/${params.id}/install-ssdv2`,
			{
				method: 'POST'
			}
		);

		if (!response.ok) {
			let message = "Impossible de lancer l'installation SSDv2";

			try {
				const apiError = await response.json();
				if (typeof apiError?.detail === 'string' && apiError.detail.trim()) {
					message = apiError.detail;
				}
			} catch {
				// no-op
			}

			return fail(response.status, {
				installError: message
			});
		}

		const job = await response.json();
		throw redirect(303, `/ssdv2-installations/${job.job_id}`);
	}
};