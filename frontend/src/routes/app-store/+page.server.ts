import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

const apps = [
	{
		slug: 'chevereto',
		name: 'Chevereto',
		category: 'Media',
		tagline: "Plateforme d'hébergement d'images et de vidéos",
		description:
			'Crée ton propre service de partage média avec albums, comptes utilisateurs et stockage externe.',
		icon: 'https://chevereto.com/favicon.ico',
		accent: 'linear-gradient(135deg, rgba(244,63,94,0.9), rgba(251,146,60,0.9))',
		status: 'Disponible'
	},
	{
		slug: 'coolify',
		name: 'Coolify',
		category: 'Platform',
		tagline: 'PaaS auto-hébergeable',
		description:
			'Déploie apps, bases de données et services sur ton propre serveur avec une expérience type cloud.',
		icon: 'https://coolify.io/favicon.ico',
		accent: 'linear-gradient(135deg, rgba(34,197,94,0.9), rgba(16,185,129,0.9))',
		status: 'Disponible'
	},
	{
		slug: 'firefox',
		name: 'Firefox',
		category: 'Browser',
		tagline: 'Navigateur web Mozilla',
		description:
			'Expose un navigateur web distant dans ton environnement avec une UX familière et moderne.',
		icon: 'https://www.firefox.com/favicon.ico',
		accent: 'linear-gradient(135deg, rgba(249,115,22,0.95), rgba(168,85,247,0.9))',
		status: 'Disponible'
	},
	{
		slug: 'filebrowser',
		name: 'File Browser',
		category: 'Files',
		tagline: 'Gestionnaire de fichiers web',
		description:
			'Parcours, édite et administre tes fichiers via une interface web simple et efficace.',
		icon: 'https://filebrowser.org/favicon.ico',
		accent: 'linear-gradient(135deg, rgba(59,130,246,0.95), rgba(14,165,233,0.9))',
		status: 'Disponible'
	},
	{
		slug: 'n8n',
		name: 'n8n',
		category: 'Automation',
		tagline: 'Automatisation open source',
		description:
			'Crée des workflows et connecte tes outils avec une interface visuelle moderne.',
		icon: 'https://n8n.io/favicon.ico',
		accent: 'linear-gradient(135deg, rgba(239,68,68,0.95), rgba(217,70,239,0.9))',
		status: 'Disponible'
	}
];

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const machinesResponse = await apiFetchWithAuth(locals.token, '/me/machines', {
		method: 'GET'
	});

	const machines = machinesResponse.ok ? await machinesResponse.json() : [];

	return {
		apps,
		machines
	};
};

export const actions: Actions = {
	createInstallation: async ({ locals, request }) => {
		if (!locals.user || !locals.token) {
			throw redirect(303, '/login');
		}

		const formData = await request.formData();
		const machine_id = String(formData.get('machine_id') ?? '').trim();
		const app_slug = String(formData.get('app_slug') ?? '').trim();
		const subdomain = String(formData.get('subdomain') ?? '').trim();
		const auth_type = String(formData.get('auth_type') ?? '').trim();

		if (!machine_id || !app_slug || !subdomain || !auth_type) {
			return fail(400, {
				error: 'Tous les champs sont requis',
				machine_id,
				app_slug,
				subdomain,
				auth_type
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
				// ignore parse error
			}

			return fail(response.status, {
				error: message,
				machine_id,
				app_slug,
				subdomain,
				auth_type
			});
		}

		const data = await response.json();
		const jobId = data.job_id;

		if (!jobId) {
			return fail(500, {
				error: 'Réponse invalide du backend',
				machine_id,
				app_slug,
				subdomain,
				auth_type
			});
		}

		throw redirect(303, `/installations/${jobId}`);
	}
};