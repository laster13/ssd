import { fail, redirect, error } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

const APPS = {
	chevereto: {
		slug: 'chevereto',
		name: 'Chevereto',
		description: "Plateforme d'hébergement d'images et de vidéos",
		icon: 'https://chevereto.com/favicon.ico'
	},
	coolify: {
		slug: 'coolify',
		name: 'Coolify',
		description: 'PaaS auto-hébergeable',
		icon: 'https://coolify.io/favicon.ico'
	},
	firefox: {
		slug: 'firefox',
		name: 'Firefox',
		description: 'Navigateur web Mozilla',
		icon: 'https://www.firefox.com/favicon.ico'
	},
	filebrowser: {
		slug: 'filebrowser',
		name: 'File Browser',
		description: 'Gestionnaire de fichiers web',
		icon: 'https://filebrowser.org/favicon.ico'
	}
} as const;

export const load: PageServerLoad = async ({ locals, params }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const app = APPS[params.slug as keyof typeof APPS];
	if (!app) {
		throw error(404, 'Application introuvable');
	}

	const machinesResponse = await apiFetchWithAuth(locals.token, '/me/machines', {
		method: 'GET'
	});

	if (!machinesResponse.ok) {
		throw error(machinesResponse.status, 'Impossible de charger les serveurs');
	}

	const machines = await machinesResponse.json();

	return {
		user: locals.user,
		app,
		machines
	};
};

export const actions: Actions = {
	install: async ({ locals, request, params }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const app = APPS[params.slug as keyof typeof APPS];
		if (!app) {
			return fail(404, { error: 'Application introuvable' });
		}

		const formData = await request.formData();
		const machine_id = String(formData.get('machine_id') ?? '').trim();
		const subdomain = String(formData.get('subdomain') ?? '').trim();
		const auth_type = String(formData.get('auth_type') ?? '').trim();

		if (!machine_id || !subdomain || !auth_type) {
			return fail(400, {
				error: 'Tous les champs sont requis',
				machine_id,
				subdomain,
				auth_type
			});
		}

		const response = await apiFetchWithAuth(locals.token, `/admin/machines/${machine_id}/jobs`, {
			method: 'POST',
			body: JSON.stringify({
				app_slug: app.slug,
				subdomain,
				auth_type
			})
		});

		if (!response.ok) {
			return fail(response.status, {
				error: "Impossible de créer l'installation",
				machine_id,
				subdomain,
				auth_type
			});
		}

		const data = await response.json();
		throw redirect(303, `/installations/${data.job_id}`);
	}
};