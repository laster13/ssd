import { redirect, error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

export const load: LayoutServerLoad = async ({ locals, url }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	if (!locals.user.is_admin) {
		throw redirect(303, '/');
	}

	const statusResponse = await apiFetchWithAuth(locals.token, '/auth/2fa/status', {
		method: 'GET'
	});

	if (!statusResponse.ok) {
		throw error(statusResponse.status, 'Impossible de vérifier le statut 2FA');
	}

	const status = await statusResponse.json();

	if (!status.enabled) {
		const next = encodeURIComponent(url.pathname + url.search);
		throw redirect(303, `/settings/security?required=admin-2fa&next=${next}`);
	}

	return {
		user: locals.user
	};
};
