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

	const [machinesResponse, settingsResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, '/me/machines', { method: 'GET' }),
		apiFetchWithAuth(locals.token, `/me/machines/${params.id}/settings`, { method: 'GET' })
	]);

	if (!machinesResponse.ok) {
		throw error(machinesResponse.status, 'Impossible de charger le serveur');
	}

	if (!settingsResponse.ok) {
		throw error(settingsResponse.status, 'Impossible de charger la configuration du serveur');
	}

	const machines = await machinesResponse.json();
	const settings = await settingsResponse.json();

	const normalizedMachines = Array.isArray(machines) ? machines : [];
	const machine = normalizedMachines.find((item: any) => String(item?.id) === params.id);

	if (!machine) {
		throw error(404, 'Serveur introuvable');
	}

	return {
		machine,
		settings,
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
	}
};