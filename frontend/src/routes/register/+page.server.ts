import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { setSessionCookie, validateCsrf } from '$lib/server/security';
import { getBackendUrl } from '$lib/public-config';

const BACKEND_URL = getBackendUrl();

export const load: PageServerLoad = async ({ locals }) => {
	if (locals.user) {
		throw redirect(303, '/app-store');
	}

	return {};
};

export const actions: Actions = {
	default: async ({ request, cookies, fetch, url }) => {
		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: null
		});

		const email = String(formData.get('email') ?? '').trim();
		const password = String(formData.get('password') ?? '').trim();

		if (!email || !password) {
			return fail(400, { error: 'Email et mot de passe requis', email });
		}

		const registerResponse = await fetch(`${BACKEND_URL}/auth/register`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ email, password })
		});

		if (!registerResponse.ok) {
			return fail(registerResponse.status, { error: 'Impossible de créer le compte', email });
		}

		const loginResponse = await fetch(`${BACKEND_URL}/auth/login`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ email, password })
		});

		if (!loginResponse.ok) {
			return fail(loginResponse.status, {
				error: 'Compte créé, mais connexion automatique impossible',
				email
			});
		}

		const loginData = await loginResponse.json();
		setSessionCookie(cookies, loginData.access_token);

		throw redirect(303, '/app-store');
	}
};