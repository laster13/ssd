import type { Handle } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';
import { PUBLIC_BACKEND_URL } from '$env/static/public';

const BACKEND_URL = PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export const handle: Handle = async ({ event, resolve }) => {
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
				event.cookies.delete('token', {
					path: '/',
					httpOnly: true,
					sameSite: 'lax',
					secure: false
				});
				event.locals.token = null;
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