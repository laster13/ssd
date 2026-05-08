import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

import { apiFetch, apiFetchWithAuth } from '$lib/server/api';
import { validateCsrf } from '$lib/server/security';
import type { ForumCategory } from '$lib/types/forum';

type ForumNewValues = {
	category_slug: string;
	related_tutorial_slug: string;
	title: string;
	content: string;
};

function cleanQueryValue(value: string | null) {
	return (value ?? '').trim().slice(0, 300);
}

function buildPrefilledValues(url: URL): ForumNewValues {
	const relatedTutorialSlug = cleanQueryValue(url.searchParams.get('tutorial'));
	const queryTitle = cleanQueryValue(url.searchParams.get('title'));
	const queryContent = cleanQueryValue(url.searchParams.get('content'));

	const title = queryTitle || (relatedTutorialSlug ? `[Aide] ${relatedTutorialSlug}` : '');

	const content =
		queryContent ||
		(relatedTutorialSlug
			? `Bonjour,

Je bloque sur le tutoriel : ${queryTitle || relatedTutorialSlug}
Lien : /tutos/${relatedTutorialSlug}

Mon problème :
...

L'étape où je bloque :
...

Ce que j'ai déjà essayé :
...

Message d'erreur éventuel :
...`
			: '');

	return {
		category_slug: 'tutoriels',
		related_tutorial_slug: relatedTutorialSlug,
		title,
		content
	};
}

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

export const load: PageServerLoad = async ({ locals, cookies, url }) => {
	const csrfToken = cookies.get('csrf_token') ?? '';
	const categoriesResponse = await apiFetch('/forum/categories');
	const values = buildPrefilledValues(url);

	if (!categoriesResponse.ok) {
		return {
			categories: [],
			user: locals.user ?? null,
			csrfToken,
			values
		};
	}

	const categories: ForumCategory[] = await categoriesResponse.json();

	return {
		categories,
		user: locals.user ?? null,
		csrfToken,
		values
	};
};

export const actions: Actions = {
	default: async ({ request, cookies, url, locals }) => {
		if (!locals.user || !locals.token) {
			return fail(401, {
				error: 'Tu dois être connecté pour créer un sujet.',
				values: buildPrefilledValues(url)
			});
		}

		const formData = await validateCsrf({
			request,
			cookies,
			url,
			sessionToken: locals.token
		});

		const category_slug = String(formData.get('category_slug') ?? '').trim();
		const related_tutorial_slug = String(formData.get('related_tutorial_slug') ?? '').trim();
		const title = String(formData.get('title') ?? '').trim();
		const content = String(formData.get('content') ?? '').trim();

		const values = {
			category_slug,
			related_tutorial_slug,
			title,
			content
		};

		if (!category_slug || !title || !content) {
			return fail(400, {
				error: 'Tous les champs requis doivent être remplis.',
				values
			});
		}

		const response = await apiFetchWithAuth(locals.token, '/forum/topics', {
			method: 'POST',
			body: JSON.stringify({
				category_slug,
				related_tutorial_slug: related_tutorial_slug || null,
				title,
				content
			})
		});

		if (!response.ok) {
			const error = await getApiErrorMessage(response, 'Impossible de créer le sujet.');

			return fail(response.status, {
				error,
				values
			});
		}

		const topic = await response.json();

		throw redirect(303, `/forum/${topic.slug}`);
	}
};