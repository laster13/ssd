import { fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetch, apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';
import type { ForumTopicListItem } from '$lib/types/forum';

export const load: PageServerLoad = async ({ params }) => {
	const response = await apiFetch(
		`/forum/topics?related_tutorial_slug=${encodeURIComponent(params.slug)}`
	);

	let forumTopics: ForumTopicListItem[] = [];

	if (response.ok) {
		forumTopics = await response.json();
	}

	return {
		forumTopics
	};
};

export const actions: Actions = {
	createTopic: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				createTopicError: 'Tu dois être connecté pour créer un sujet.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const category_slug = String(formData.get('category_slug') ?? '').trim();
		const title = String(formData.get('title') ?? '').trim();
		const content = String(formData.get('content') ?? '').trim();
		const related_tutorial_slug = String(formData.get('related_tutorial_slug') ?? '').trim();

		if (!category_slug || !title || !content || !related_tutorial_slug) {
			return fail(400, {
				createTopicError: 'Tous les champs sont requis.',
				title,
				content
			});
		}

		const response = await apiFetchWithAuth(locals.token, '/forum/topics', {
			method: 'POST',
			body: JSON.stringify({
				category_slug,
				title,
				content,
				related_tutorial_slug
			})
		});

		if (!response.ok) {
			let createTopicError = 'Impossible de créer le sujet.';

			try {
				const payload = await response.json();
				if (typeof payload?.detail === 'string' && payload.detail.trim()) {
					createTopicError = payload.detail.trim();
				}
			} catch {
				// noop
			}

			return fail(response.status, {
				createTopicError,
				title,
				content
			});
		}

		return {
			createTopicSuccess: true,
			title: '',
			content: ''
		};
	}
};