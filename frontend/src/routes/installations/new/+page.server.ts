import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

const apps = [
	{
		slug: 'chevereto',
		name: 'Chevereto',
		category: 'Media',
		tagline: "Plateforme d'hébergement d'images et de vidéos"
	},
	{
		slug: 'coolify',
		name: 'Coolify',
		category: 'Platform',
		tagline: 'PaaS auto-hébergeable'
	},
	{
		slug: 'firefox',
		name: 'Firefox',
		category: 'Browser',
		tagline: 'Navigateur web Mozilla'
	},
	{
		slug: 'filebrowser',
		name: 'File Browser',
		category: 'Files',
		tagline: 'Gestionnaire de fichiers web'
	},
	{
		slug: 'n8n',
		name: 'n8n',
		category: 'Automation',
		tagline: 'Automatisation open source'
	}
];

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const appSlug = url.searchParams.get('app') ?? '';

	const app = apps.find((item) => item.slug === appSlug);

	if (!app) {
		throw redirect(303, '/app-store');
	}

	const machinesResponse = await apiFetchWithAuth(locals.token, '/me/machines', {
		method: 'GET'
	});

	const machines = machinesResponse.ok ? await machinesResponse.json() : [];

	return {
		app,
		machines
	};
};

export const actions: Actions = {
	createInstallation: async ({ locals, request, url }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await request.formData();

		const machine_id = String(formData.get('machine_id') ?? '').trim();
		const subdomain = String(formData.get('subdomain') ?? '').trim();
		const auth_type = String(formData.get('auth_type') ?? '').trim();
		const app_slug = String(formData.get('app_slug') ?? '').trim();

		if (!machine_id || !subdomain || !auth_type || !app_slug) {
			return fail(400, {
				error: 'Tous les champs sont requis',
				machine_id,
				subdomain,
				auth_type,
				app_slug
			});
		}

		const response = await apiFetchWithAuth(locals.token, '/me/installations', {
			method: 'POST',
			body: JSON.stringify({
				machine_id,
				app_slug,
				subdomain,
				auth_type
			})
		});

		if (!response.ok) {
			let message = 'Impossible de lancer l’installation';

			try {
				const data = await response.json();
				if (typeof data?.detail === 'string') {
					message = data.detail;
				}
			} catch {
				// ignore
			}

			return fail(response.status, {
				error: message,
				machine_id,
				subdomain,
				auth_type,
				app_slug
			});
		}

		const data = await response.json();
		throw redirect(303, `/installations/${data.job_id}`);
	}
};
