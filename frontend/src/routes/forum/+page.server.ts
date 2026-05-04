import type { PageServerLoad } from './$types';
import { apiFetch } from '$lib/server/api';
import type { ForumCategory, ForumTopicListItem } from '$lib/types/forum';

export const load: PageServerLoad = async ({ url }) => {
	const tutorialSlug = url.searchParams.get('tutorial')?.trim() || '';
	const categorySlug = url.searchParams.get('category')?.trim() || '';
	const onlyUnsolved = url.searchParams.get('unsolved') === '1';
	const q = url.searchParams.get('q')?.trim() || '';
	const sort = url.searchParams.get('sort')?.trim() || 'recent';
	const page = Number(url.searchParams.get('page') || '1');
	const limit = 20;
	const offset = Math.max(0, (page - 1) * limit);

	const params = new URLSearchParams();
	if (tutorialSlug) params.set('related_tutorial_slug', tutorialSlug);
	if (categorySlug) params.set('category_slug', categorySlug);
	if (onlyUnsolved) params.set('only_unsolved', 'true');
	if (q) params.set('q', q);
	if (sort) params.set('sort', sort);
	params.set('limit', String(limit));
	params.set('offset', String(offset));

	const topicsResponse = await apiFetch(`/forum/topics?${params.toString()}`);
	const categoriesResponse = await apiFetch('/forum/categories');

	let topics: ForumTopicListItem[] = [];
	let categories: ForumCategory[] = [];

	if (topicsResponse.ok) {
		topics = await topicsResponse.json();
	}

	if (categoriesResponse.ok) {
		categories = await categoriesResponse.json();
	}

	return {
		topics,
		categories,
		tutorialSlug,
		categorySlug,
		onlyUnsolved,
		q,
		sort,
		page,
		limit,
		hasNextPage: topics.length === limit
	};
};