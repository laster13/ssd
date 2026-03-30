import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		apps: [
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
			}
		]
	};
};
