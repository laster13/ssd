import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';
import type { ForumNotification, ForumNotificationCount } from '$lib/types/notification';

export const load: PageServerLoad = async ({ locals, url }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login?next=/notifications');
	}

	const onlyUnread = url.searchParams.get('unread') === '1';
	const query = onlyUnread ? '/notifications?only_unread=true' : '/notifications';

	const [notificationsResponse, unreadCountResponse] = await Promise.all([
		apiFetchWithAuth(locals.token, query),
		apiFetchWithAuth(locals.token, '/notifications/unread-count')
	]);

	let notifications: ForumNotification[] = [];
	let unreadCount = 0;

	if (notificationsResponse.ok) {
		notifications = await notificationsResponse.json();
	}

	if (unreadCountResponse.ok) {
		const payload: ForumNotificationCount = await unreadCountResponse.json();
		unreadCount = payload.unread_count;
	}

	return {
		notifications,
		unreadCount,
		onlyUnread
	};
};

export const actions: Actions = {
	markRead: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, { error: 'Connexion requise.' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const notificationId = String(formData.get('notification_id') ?? '').trim();

		const response = await apiFetchWithAuth(
			locals.token,
			`/notifications/${notificationId}/read`,
			{ method: 'POST' }
		);

		if (!response.ok) {
			return fail(response.status, { error: 'Impossible de marquer la notification comme lue.' });
		}

		return { ok: true };
	},

	markAllRead: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, { error: 'Connexion requise.' });
		}

		await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const response = await apiFetchWithAuth(locals.token, '/notifications/read-all', {
			method: 'POST'
		});

		if (!response.ok) {
			return fail(response.status, { error: 'Impossible de tout marquer comme lu.' });
		}

		return { ok: true };
	}
};