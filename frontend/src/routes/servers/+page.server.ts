import { fail, redirect, error } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const response = await apiFetchWithAuth(locals.token, '/me/machines', {
		method: 'GET'
	});

	if (!response.ok) {
		throw error(response.status, 'Impossible de charger les serveurs');
	}

	const machines = await response.json();
	const normalizedMachines = Array.isArray(machines) ? machines : [];

	return {
		machines: normalizedMachines.filter(
			(machine: any) => String(machine?.status ?? '').trim().toLowerCase() !== 'revoked'
		)
	};
};

export const actions: Actions = {
	delete: async ({ request, cookies, locals, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const machineId = String(formData.get('machine_id') ?? '').trim();

		if (!machineId) {
			return fail(400, {
				error: 'Serveur introuvable'
			});
		}

		const response = await apiFetchWithAuth(locals.token, `/me/machines/${machineId}`, {
			method: 'DELETE'
		});

		if (!response.ok) {
			let message = "Impossible de supprimer l'appairage du serveur";

			try {
				const payload = await response.json();
				if (typeof payload?.detail === 'string' && payload.detail.trim()) {
					message = payload.detail;
				}
			} catch {
				// no-op
			}

			return fail(response.status, {
				error: message
			});
		}

		return {
			success: true
		};
	}
};