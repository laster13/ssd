import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { setSessionCookie, validateCsrf } from '$lib/server/security';
import { getServerBackendUrl } from '$lib/server/backend';

export const load: PageServerLoad = async ({ locals }) => {
	if (locals.user) {
		throw redirect(303, '/app-store');
	}

	return {};
};

export const actions: Actions = {
	default: async ({ request, cookies, fetch, url }) => {
		const BACKEND_URL = getServerBackendUrl();
		const formData = await validateCsrf({ request, cookies, url, sessionToken: null });

		const email = String(formData.get('email') ?? '').trim();
		const password = String(formData.get('password') ?? '').trim();

		if (!email || !password) {
			return fail(400, {
				error: 'Email et mot de passe requis',
				email
			});
		}

		const registerResponse = await fetch(`${BACKEND_URL}/auth/register`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email, password })
		});

		if (!registerResponse.ok) {
			let message = 'Impossible de créer le compte';

			try {
				const errorData = await registerResponse.json();
				if (typeof errorData?.detail === 'string') {
					message = errorData.detail;
				}
			} catch {
				// no-op
			}

			return fail(registerResponse.status, {
				error: message,
				email
			});
		}

		const loginResponse = await fetch(`${BACKEND_URL}/auth/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email, password })
		});

		if (!loginResponse.ok) {
			let message = 'Compte créé, mais connexion automatique impossible';

			try {
				const errorData = await loginResponse.json();
				if (typeof errorData?.detail === 'string') {
					message = errorData.detail;
				}
			} catch {
				// no-op
			}

			return fail(loginResponse.status, {
				error: message,
				email
			});
		}

		const loginData = await loginResponse.json();

		setSessionCookie(cookies, loginData.access_token);
		throw redirect(303, '/app-store');
	}
};