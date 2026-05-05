import { error as svelteError, fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { apiFetch, apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';
import type { ForumTopic, ForumTopicListItem } from '$lib/types/forum';

async function getApiErrorMessage(response: Response, fallback: string): Promise<string> {
	try {
		const payload = await response.json();

		if (typeof payload?.detail === 'string' && payload.detail.trim()) {
			return payload.detail.trim();
		}

		if (Array.isArray(payload?.detail)) {
			const messages = payload.detail
				.map((item: unknown) => {
					if (typeof item === 'string') return item.trim();

					if (
						item &&
						typeof item === 'object' &&
						'msg' in item &&
						typeof (item as { msg?: unknown }).msg === 'string'
					) {
						return (item as { msg: string }).msg.trim();
					}

					return '';
				})
				.filter(Boolean);

			if (messages.length > 0) {
				return messages.join(' · ');
			}
		}
	} catch {
		// noop
	}

	return fallback;
}

export const load: PageServerLoad = async ({ params, url, cookies }) => {

        const csrfToken = cookies.get('csrf_token') ?? '';
	const postsSort = url.searchParams.get('posts_sort')?.trim() || 'oldest';

	const response = await apiFetch(
		`/forum/topics/${encodeURIComponent(params.slug)}?posts_sort=${encodeURIComponent(postsSort)}`
	);

	if (!response.ok) {
		const message = await getApiErrorMessage(response, 'Impossible de charger le sujet.');
		throw svelteError(response.status, message);
	}

	const topic: ForumTopic = await response.json();
	let relatedTopics: ForumTopicListItem[] = [];

	if (topic.related_tutorial_slug) {
		const relatedResponse = await apiFetch(
			`/forum/topics?related_tutorial_slug=${encodeURIComponent(topic.related_tutorial_slug)}&sort=active&limit=5`
		);

		if (relatedResponse.ok) {
			const all: ForumTopicListItem[] = await relatedResponse.json();
			relatedTopics = all.filter((item) => item.slug !== topic.slug).slice(0, 5);
		}
	}

	return {
		topic,
		relatedTopics,
		postsSort,
	        csrfToken
	};
};

export const actions: Actions = {
	createReply: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				replyError: 'Tu dois être connecté pour répondre.',
				replyTargetType: 'topic',
				replyTargetId: '',
				replyContent: ''
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const topic_id = String(formData.get('topic_id') ?? '').trim();
		const content = String(formData.get('content') ?? '').trim();
		const parent_post_id_raw = String(formData.get('parent_post_id') ?? '').trim();
		const replyTargetType = String(formData.get('reply_target_type') ?? 'topic').trim();
		const replyTargetId = String(formData.get('reply_target_id') ?? '').trim();

		if (!topic_id || !content) {
			return fail(400, {
				replyError: 'Le contenu de la réponse est requis.',
				replyTargetType,
				replyTargetId,
				replyContent: content
			});
		}

		const response = await apiFetchWithAuth(locals.token, `/forum/topics/${topic_id}/posts`, {
			method: 'POST',
			body: JSON.stringify({
				content,
				parent_post_id: parent_post_id_raw || null
			})
		});

		if (!response.ok) {
			const replyError = await getApiErrorMessage(
				response,
				'Impossible d’ajouter la réponse.'
			);

			return fail(response.status, {
				replyError,
				replyTargetType,
				replyTargetId,
				replyContent: content
			});
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	acceptReply: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				replyError: 'Tu dois être connecté pour valider une réponse.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const post_id = String(formData.get('post_id') ?? '').trim();

		if (!post_id) {
			return fail(400, {
				replyError: 'Message introuvable.'
			});
		}

		const response = await apiFetchWithAuth(locals.token, `/forum/posts/${post_id}/accept`, {
			method: 'POST'
		});

		if (!response.ok) {
			const replyError = await getApiErrorMessage(
				response,
				'Impossible de marquer cette réponse comme solution.'
			);

			return fail(response.status, { replyError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	voteReply: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				replyError: 'Tu dois être connecté pour voter.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const post_id = String(formData.get('post_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/posts/${post_id}/vote`, {
			method: 'POST'
		});

		if (!response.ok) {
			const replyError = await getApiErrorMessage(
				response,
				'Impossible de voter pour cette réponse.'
			);

			return fail(response.status, { replyError });
		}

		throw redirect(303, `/forum/${params.slug}?posts_sort=useful`);
	},

	reportReply: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				replyError: 'Tu dois être connecté pour signaler.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const post_id = String(formData.get('post_id') ?? '').trim();
		const reason = String(formData.get('reason') ?? '').trim();
		const details = String(formData.get('details') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/posts/${post_id}/report`, {
			method: 'POST',
			body: JSON.stringify({
				reason,
				details: details || null
			})
		});

		if (!response.ok) {
			const replyError = await getApiErrorMessage(
				response,
				'Impossible de signaler ce message.'
			);

			return fail(response.status, { replyError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	editReply: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				replyError: 'Tu dois être connecté pour modifier.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const post_id = String(formData.get('post_id') ?? '').trim();
		const content = String(formData.get('content') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/posts/${post_id}`, {
			method: 'PUT',
			body: JSON.stringify({ content })
		});

		if (!response.ok) {
			const replyError = await getApiErrorMessage(
				response,
				'Impossible de modifier cette réponse.'
			);

			return fail(response.status, { replyError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	deleteReply: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				replyError: 'Tu dois être connecté pour supprimer.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const post_id = String(formData.get('post_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/posts/${post_id}`, {
			method: 'DELETE'
		});

		if (!response.ok) {
			const replyError = await getApiErrorMessage(
				response,
				'Impossible de supprimer cette réponse.'
			);

			return fail(response.status, { replyError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	editTopic: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				topicError: 'Tu dois être connecté pour modifier le sujet.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const topic_id = String(formData.get('topic_id') ?? '').trim();
		const title = String(formData.get('title') ?? '').trim();
		const content = String(formData.get('content') ?? '').trim();
		const related_tutorial_slug = String(formData.get('related_tutorial_slug') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/topics/${topic_id}`, {
			method: 'PUT',
			body: JSON.stringify({
				title,
				content,
				related_tutorial_slug: related_tutorial_slug || null
			})
		});

		if (!response.ok) {
			const topicError = await getApiErrorMessage(
				response,
				'Impossible de modifier le sujet.'
			);

			return fail(response.status, { topicError });
		}

		const payload = await response.json();
		throw redirect(303, `/forum/${payload.slug}`);
	},

	deleteTopic: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				topicError: 'Tu dois être connecté pour supprimer le sujet.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const topic_id = String(formData.get('topic_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/topics/${topic_id}`, {
			method: 'DELETE'
		});

		if (!response.ok) {
			const topicError = await getApiErrorMessage(
				response,
				'Impossible de supprimer le sujet.'
			);

			return fail(response.status, { topicError });
		}

		throw redirect(303, '/forum');
	},

	pinTopic: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				topicError: 'Connexion requise.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const topic_id = String(formData.get('topic_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/topics/${topic_id}/pin`, {
			method: 'POST'
		});

		if (!response.ok) {
			const topicError = await getApiErrorMessage(
				response,
				'Impossible d’épingler le sujet.'
			);

			return fail(response.status, { topicError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	unpinTopic: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				topicError: 'Connexion requise.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const topic_id = String(formData.get('topic_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/topics/${topic_id}/unpin`, {
			method: 'POST'
		});

		if (!response.ok) {
			const topicError = await getApiErrorMessage(
				response,
				'Impossible de désépingler le sujet.'
			);

			return fail(response.status, { topicError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	lockTopic: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				topicError: 'Connexion requise.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const topic_id = String(formData.get('topic_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/topics/${topic_id}/lock`, {
			method: 'POST'
		});

		if (!response.ok) {
			const topicError = await getApiErrorMessage(
				response,
				'Impossible de verrouiller le sujet.'
			);

			return fail(response.status, { topicError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	},

	unlockTopic: async ({ request, cookies, url, locals, params }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				topicError: 'Connexion requise.'
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const topic_id = String(formData.get('topic_id') ?? '').trim();

		const response = await apiFetchWithAuth(locals.token, `/forum/topics/${topic_id}/unlock`, {
			method: 'POST'
		});

		if (!response.ok) {
			const topicError = await getApiErrorMessage(
				response,
				'Impossible de déverrouiller le sujet.'
			);

			return fail(response.status, { topicError });
		}

		throw redirect(303, `/forum/${params.slug}`);
	}
};