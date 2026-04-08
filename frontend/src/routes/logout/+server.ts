import { redirect } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { clearSessionCookies, validateCsrf } from '$lib/server/security';

export const POST: RequestHandler = async ({ request, cookies, locals, url }) => {
	await validateCsrf({
		request,
		cookies,
		url,
		sessionToken: locals.token
	});

	clearSessionCookies(cookies);
	throw redirect(303, '/');
};