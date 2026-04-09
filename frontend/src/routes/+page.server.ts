import type { PageServerLoad } from './$types';
import { apiFetch } from '$lib/server/api';

export const load: PageServerLoad = async ({ locals }) => {
	const catalogResponse = await apiFetch('/catalog/apps', { method: 'GET' });
	const apps = catalogResponse.ok ? await catalogResponse.json() : [];

	return {
		user: locals.user ?? null,
		apps
	};
};