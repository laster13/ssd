import type { LayoutServerLoad } from './$types';
import { ensureCsrfCookie } from '$lib/server/security';

export const load: LayoutServerLoad = async ({ locals, cookies }) => {
	const csrfToken = ensureCsrfCookie(cookies, locals.token);

	return {
		user: locals.user,
		csrfToken
	};
};