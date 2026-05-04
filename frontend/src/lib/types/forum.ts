export type ForumAuthorSummary = {
	id: string;
	email: string;
};

export type ForumCategory = {
	id: string;
	slug: string;
	name: string;
	description: string | null;
	created_at: string;
	updated_at: string;
};

export type ForumPost = {
	id: string;
	topic_id: string;
	author: ForumAuthorSummary;
	parent_post_id: string | null;
	parent_author: ForumAuthorSummary | null;
	parent_excerpt: string | null;
	content: string;
	is_deleted: boolean;
	is_edited: boolean;
	useful_votes_count: number;
	created_at: string;
	updated_at: string;
};

export type ForumTopicListItem = {
	id: string;
	slug: string;
	title: string;
	content: string;
	related_tutorial_slug: string | null;
	is_locked: boolean;
	is_pinned: boolean;
	is_edited: boolean;
	posts_count: number;
	views_count: number;
	accepted_post_id: string | null;
	created_at: string;
	updated_at: string;
	category: ForumCategory;
	author: ForumAuthorSummary;
};

export type ForumTopic = {
	id: string;
	slug: string;
	title: string;
	content: string;
	related_tutorial_slug: string | null;
	is_locked: boolean;
	is_pinned: boolean;
	is_edited: boolean;
	posts_count: number;
	views_count: number;
	accepted_post_id: string | null;
	created_at: string;
	updated_at: string;
	category: ForumCategory;
	author: ForumAuthorSummary;
	posts: ForumPost[];
};

export type ForumTopicRevision = {
	id: string;
	topic_id: string;
	editor: ForumAuthorSummary;
	previous_title: string;
	previous_content: string;
	created_at: string;
};

export type ForumPostRevision = {
	id: string;
	post_id: string;
	editor: ForumAuthorSummary;
	previous_content: string;
	created_at: string;
};

export type ForumReportPostSummary = {
	id: string;
	topic_id: string;
	topic_slug: string;
	topic_title: string;
	post_author: ForumAuthorSummary;
	post_content: string;
	is_deleted: boolean;
};

export type ForumPostReportAdminItem = {
	id: string;
	reason: string;
	details: string | null;
	status: string;
	created_at: string;
	reviewed_at: string | null;
	reporter: ForumAuthorSummary;
	reviewed_by: ForumAuthorSummary | null;
	post: ForumReportPostSummary;
};