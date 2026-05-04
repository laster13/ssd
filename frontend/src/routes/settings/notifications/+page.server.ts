import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';
import type { ForumNotificationPreferences } from '$lib/types/notification';

export const load: PageServerLoad = async ({ locals }) => {
	if (!locals.user || !locals.token) {
		throw redirect(303, '/login?next=/settings/notifications');
	}

	const response = await apiFetchWithAuth(locals.token, '/notifications/preferences');

	if (!response.ok) {
		return {
			preferences: {
				notify_topic_replies: true,
				notify_accepted_answer: true,
				notify_participated_topic_replies: true
			},
			loadError: 'Impossible de charger les préférences.'
		};
	}

	const preferences: ForumNotificationPreferences = await response.json();

	return {
		preferences,
		loadError: null
	};
};

export const actions: Actions = {
	default: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, { error: 'Connexion requise.' });
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const notify_topic_replies = formData.get('notify_topic_replies') === 'on';
		const notify_accepted_answer = formData.get('notify_accepted_answer') === 'on';
		const notify_participated_topic_replies =
			formData.get('notify_participated_topic_replies') === 'on';

		const response = await apiFetchWithAuth(locals.token, '/notifications/preferences', {
			method: 'PUT',
			body: JSON.stringify({
				notify_topic_replies,
				notify_accepted_answer,
				notify_participated_topic_replies
			})
		});

		if (!response.ok) {
			return fail(response.status, {
				error: 'Impossible de sauvegarder les préférences.',
				values: {
					notify_topic_replies,
					notify_accepted_answer,
					notify_participated_topic_replies
				}
			});
		}

		const preferences: ForumNotificationPreferences = await response.json();

		return {
			success: true,
			preferences
		};
	}
};