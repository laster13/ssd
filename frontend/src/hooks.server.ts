import type { Handle } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';
import { clearSessionCookies } from '$lib/server/security';
import { getServerBackendUrl } from '$lib/server/backend';

export const handle: Handle = async ({ event, resolve }) => {
	const BACKEND_URL = getServerBackendUrl();
	const token = event.cookies.get('token');

	event.locals.token = token ?? null;
	event.locals.user = null;

	if (token) {
		try {
			const response = await fetch(`${BACKEND_URL}/auth/me`, {
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			if (response.ok) {
				event.locals.user = await response.json();
			} else {
				clearSessionCookies(event.cookies);
				event.locals.token = null;
				event.locals.user = null;
			}
		} catch {
			event.locals.user = null;
		}
	}

	const isAdminRoute = event.url.pathname.startsWith('/admin');

	if (isAdminRoute) {
		if (!event.locals.user || !event.locals.token) {
			throw redirect(303, '/login');
		}

		if (!event.locals.user.is_admin) {
			throw redirect(303, '/');
		}

		const statusResponse = await fetch(`${BACKEND_URL}/auth/2fa/status`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${event.locals.token}`
			}
		});

		if (statusResponse.ok) {
			const status = await statusResponse.json();

			if (!status.enabled) {
				const next = encodeURIComponent(event.url.pathname + event.url.search);
				throw redirect(303, `/settings/security?required=admin-2fa&next=${next}`);
			}
		}
	}

	return resolve(event);
};