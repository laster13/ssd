import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';

function hashString(value: string): number {
	let hash = 0;
	for (let i = 0; i < value.length; i += 1) {
		hash = (hash * 31 + value.charCodeAt(i)) | 0;
	}
	return Math.abs(hash);
}

function accentFor(slug: string): string {
	const gradients = [
		'linear-gradient(135deg, rgba(59,130,246,0.95), rgba(14,165,233,0.9))',
		'linear-gradient(135deg, rgba(34,197,94,0.95), rgba(16,185,129,0.9))',
		'linear-gradient(135deg, rgba(239,68,68,0.95), rgba(217,70,239,0.9))',
		'linear-gradient(135deg, rgba(249,115,22,0.95), rgba(168,85,247,0.9))',
		'linear-gradient(135deg, rgba(244,63,94,0.95), rgba(251,146,60,0.9))'
	];

	return gradients[hashString(slug) % gradients.length];
}

function iconFor(name: string): string {
	const initial = (name?.trim()?.[0] ?? '?').toUpperCase();

	const svg = `
		<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64">
			<rect width="64" height="64" rx="16" fill="#0f172a"/>
			<text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
				font-family="Arial, sans-serif" font-size="28" fill="#e2e8f0">${initial}</text>
		</svg>
	`;

	return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	const response = await apiFetchWithAuth(locals.token, '/catalog/apps', {
		method: 'GET'
	});

	const rawApps = response.ok ? await response.json() : [];

	const apps = rawApps.map((app: any) => ({
		...app,
		icon: iconFor(app.name),
		accent: accentFor(app.slug)
	}));

	return {
		apps
	};
};