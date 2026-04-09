import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { getServerBackendWsUrl } from '$lib/server/backend';

export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const machinesResponse = await apiFetchWithAuth(locals.token, '/me/machines', {
		method: 'GET'
	});

	if (!machinesResponse.ok) {
		throw error(machinesResponse.status, 'Impossible de charger le serveur');
	}

	const machines = await machinesResponse.json();
	const normalizedMachines = Array.isArray(machines) ? machines : [];
	const machine = normalizedMachines.find((item: any) => String(item?.id) === params.id);

	if (!machine) {
		throw error(404, 'Serveur introuvable');
	}

	const machineSocketUrl = `${getServerBackendWsUrl()}/ws/machines?token=${encodeURIComponent(locals.token)}`;

	return {
		machine,
		machineSocketUrl
	};
};
