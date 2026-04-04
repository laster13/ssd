import type { Handle } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';

import { getServerBackendUrl } from '$lib/server/backend';
import { clearSessionCookies } from '$lib/server/security';

const BACKEND_URL = getServerBackendUrl();

function buildCsp(): string {
	return [
		"default-src 'self'",
		"base-uri 'self'",
		"frame-ancestors 'self'",
		"form-action 'self'",
		"object-src 'none'",
		"img-src 'self' data: https:",
		"font-src 'self' data: https:",
		"connect-src 'self' https: wss:",
		"script-src 'self' 'unsafe-inline'",
		"style-src 'self' 'unsafe-inline'",
		'upgrade-insecure-requests'
	].join('; ');
}

function applySecurityHeaders(response: Response): void {
	response.headers.set('Content-Security-Policy', buildCsp());
	response.headers.set(
		'Permissions-Policy',
		'accelerometer=(), autoplay=(), camera=(), display-capture=(), geolocation=(), gyroscope=(), microphone=(), payment=(), usb=()'
	);
	response.headers.set('Cross-Origin-Opener-Policy', 'same-origin');
	response.headers.set('Cross-Origin-Resource-Policy', 'same-origin');
	response.headers.set('Origin-Agent-Cluster', '?1');
}

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get('token') ?? null;

	event.locals.token = token;
	event.locals.user = null;

	if (token) {
		try {
			const response = await event.fetch(`${BACKEND_URL}/auth/me`, {
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
			throw redirect(303, `/login?next=${encodeURIComponent(event.url.pathname + event.url.search)}`);
		}

		if (!event.locals.user.is_admin) {
			throw redirect(303, '/');
		}

		try {
			const statusResponse = await event.fetch(`${BACKEND_URL}/auth/2fa/status`, {
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
		} catch {
			const next = encodeURIComponent(event.url.pathname + event.url.search);
			throw redirect(303, `/login?next=${next}`);
		}
	}

	const response = await resolve(event);
	applySecurityHeaders(response);
	return response;
};