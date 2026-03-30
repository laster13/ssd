import { fail, redirect, error } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

function getSafeNext(url: URL): string | null {
	const next = url.searchParams.get('next')?.trim();
	if (!next) return null;
	if (!next.startsWith('/')) return null;
	if (next.startsWith('//')) return null;
	return next;
}

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const statusResponse = await apiFetchWithAuth(locals.token, '/auth/2fa/status', {
		method: 'GET'
	});

	if (!statusResponse.ok) {
		throw error(statusResponse.status, 'Impossible de charger le statut 2FA');
	}

	const status = await statusResponse.json();

	return {
		status,
		required: url.searchParams.get('required') ?? null,
		next: getSafeNext(url)
	};
};

export const actions: Actions = {
	setup: async ({ locals }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const response = await apiFetchWithAuth(locals.token, '/auth/2fa/setup', {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, { error: 'Impossible de préparer le 2FA' });
		}

		const setup = await response.json();
		return { setup };
	},

	confirm: async ({ locals, request, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await request.formData();
		const otp_code = String(formData.get('otp_code') ?? '').trim();

		if (!otp_code) {
			return fail(400, { error: 'Code 2FA requis', otp_code });
		}

		const response = await apiFetchWithAuth(locals.token, '/auth/2fa/confirm', {
			method: 'POST',
			body: JSON.stringify({ otp_code })
		});

		if (!response.ok) {
			let message = 'Impossible d’activer le 2FA';

			try {
				const data = await response.json();
				if (typeof data?.detail === 'string') {
					message = data.detail;
				}
			} catch {
				// no-op
			}

			return fail(response.status, { error: message, otp_code });
		}

		const next = getSafeNext(url);
		if (next) {
			throw redirect(303, next);
		}

		return { confirmed: true };
	},

	disable: async ({ locals, request }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await request.formData();
		const password = String(formData.get('password') ?? '').trim();
		const otp_code = String(formData.get('otp_code') ?? '').trim();

		if (!password || !otp_code) {
			return fail(400, {
				error: 'Mot de passe et code 2FA requis pour désactiver',
				disable_password: password,
				disable_otp_code: otp_code
			});
		}

		const response = await apiFetchWithAuth(locals.token, '/auth/2fa/disable', {
			method: 'POST',
			body: JSON.stringify({ password, otp_code })
		});

		if (!response.ok) {
			let message = 'Impossible de désactiver le 2FA';

			try {
				const data = await response.json();
				if (typeof data?.detail === 'string') {
					message = data.detail;
				}
			} catch {
				// no-op
			}

			return fail(response.status, {
				error: message,
				disable_password: password,
				disable_otp_code: otp_code
			});
		}

		return { disabled: true };
	}
};