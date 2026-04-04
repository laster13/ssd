import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

import { getServerBackendUrl } from '$lib/server/backend';
import { setSessionCookie, validateCsrf } from '$lib/server/security';

function normalizeNext(rawNext: string | null): string {
	if (!rawNext) return '/app-store';
	if (!rawNext.startsWith('/')) return '/app-store';
	if (rawNext.startsWith('//')) return '/app-store';
	return rawNext;
}

export const load: PageServerLoad = async ({ locals, url }) => {
	if (locals.user) {
		throw redirect(303, normalizeNext(url.searchParams.get('next')));
	}

	return {};
};

export const actions: Actions = {
	default: async ({ request, cookies, fetch, url }) => {
		const BACKEND_URL = getServerBackendUrl();

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: null
		});

		const email = String(formData.get('email') ?? '').trim();
		const password = String(formData.get('password') ?? '').trim();
		const otp_code = String(formData.get('otp_code') ?? '').trim();

		if (!email || !password) {
			return fail(400, {
				error: 'Email et mot de passe requis',
				email,
				otp_code
			});
		}

		const payload: Record<string, string> = { email, password };

		if (otp_code) {
			payload.otp_code = otp_code;
		}

		const response = await fetch(`${BACKEND_URL}/auth/login`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(payload)
		});

		if (!response.ok) {
			let message = 'Identifiants invalides';

			try {
				const errorData = await response.json();

				if (errorData?.detail === 'OTP code required') {
					message = 'Code 2FA requis';
				} else if (errorData?.detail === 'Invalid OTP code') {
					message = 'Code 2FA invalide';
				} else if (typeof errorData?.detail === 'string') {
					message = errorData.detail;
				}
			} catch {
				// réponse non JSON ou vide
			}

			return fail(response.status, {
				error: message,
				email,
				otp_code
			});
		}

		const data = await response.json();

		if (typeof data?.access_token !== 'string' || !data.access_token) {
			return fail(502, {
				error: 'Réponse backend invalide',
				email,
				otp_code
			});
		}

		setSessionCookie(cookies, data.access_token);

		throw redirect(303, normalizeNext(url.searchParams.get('next')));
	}
};