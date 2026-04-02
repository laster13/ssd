import { error, fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	if (!locals.user.is_admin) {
		throw redirect(303, '/');
	}

	const usersResponse = await apiFetchWithAuth(locals.token, '/admin/users', {
		method: 'GET'
	});

	if (!usersResponse.ok) {
		throw error(usersResponse.status, 'Impossible de charger les utilisateurs');
	}

	const users = await usersResponse.json();

	return {
		user: locals.user,
		users
	};
};

async function readApiError(response: Response, fallback: string) {
	try {
		const payload = await response.json();
		if (typeof payload?.detail === 'string' && payload.detail.trim()) {
			return payload.detail;
		}
		return fallback;
	} catch {
		return fallback;
	}
}

export const actions: Actions = {
	grantAdmin: async ({ request, cookies, locals, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		if (!locals.user.is_admin) {
			return fail(403, { error: 'Accès admin requis' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const userId = String(formData.get('user_id') ?? '').trim();

		if (!userId) {
			return fail(400, { error: 'Utilisateur manquant' });
		}

		const response = await apiFetchWithAuth(locals.token, `/admin/users/${userId}/grant-admin`, {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, {
				error: await readApiError(response, "Impossible d'ajouter cet admin")
			});
		}

		return {
			success: true,
			action: 'grantAdmin',
			targetUserId: userId
		};
	},

	revokeAdmin: async ({ request, cookies, locals, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		if (!locals.user.is_admin) {
			return fail(403, { error: 'Accès admin requis' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const userId = String(formData.get('user_id') ?? '').trim();

		if (!userId) {
			return fail(400, { error: 'Utilisateur manquant' });
		}

		const response = await apiFetchWithAuth(locals.token, `/admin/users/${userId}/revoke-admin`, {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, {
				error: await readApiError(response, "Impossible de rétrograder cet admin")
			});
		}

		return {
			success: true,
			action: 'revokeAdmin',
			targetUserId: userId
		};
	},

	deleteUser: async ({ request, cookies, locals, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		if (!locals.user.is_admin) {
			return fail(403, { error: 'Accès admin requis' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const userId = String(formData.get('user_id') ?? '').trim();

		if (!userId) {
			return fail(400, { error: 'Utilisateur manquant' });
		}

		const response = await apiFetchWithAuth(locals.token, `/admin/users/${userId}/delete`, {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, {
				error: await readApiError(response, 'Impossible de supprimer ce compte')
			});
		}

		return {
			success: true,
			action: 'deleteUser',
			targetUserId: userId
		};
	}
};