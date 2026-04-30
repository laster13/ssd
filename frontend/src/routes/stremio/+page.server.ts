import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { stremioLinks } from '$lib/data/stremio-links';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login');
	}

	return {
		user: locals.user,
		links: stremioLinks
	};
};