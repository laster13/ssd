import type { LayoutServerLoad } from './$types';
import { ensureCsrfCookie } from '$lib/server/security';
import { apiFetchWithAuth } from '$lib/server/api';
import type { ForumNotificationCount } from '$lib/types/notification';

export const load: LayoutServerLoad = async ({ locals, cookies, url }) => {
	const csrfToken = ensureCsrfCookie(cookies, locals.token);

	let unreadNotifications = 0;

	if (locals.user && locals.token) {
		const response = await apiFetchWithAuth(locals.token, '/notifications/unread-count');

		if (response.ok) {
			const payload: ForumNotificationCount = await response.json();
			unreadNotifications = payload.unread_count;
		}
	}

	return {
		user: locals.user,
		csrfToken,
		unreadNotifications,
		pathname: url.pathname
	};
};