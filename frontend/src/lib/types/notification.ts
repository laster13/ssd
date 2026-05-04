import type { ForumAuthorSummary } from '$lib/types/forum';

export type ForumNotification = {
	id: string;
	type: string;
	title: string;
	message: string | null;
	link: string | null;
	is_read: boolean;
	read_at: string | null;
	created_at: string;
	actor: ForumAuthorSummary | null;
};

export type ForumNotificationCount = {
	unread_count: number;
};

export type ForumNotificationPreferences = {
	notify_topic_replies: boolean;
	notify_accepted_answer: boolean;
	notify_participated_topic_replies: boolean;
};