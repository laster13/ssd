import { marked } from 'marked';
import DOMPurify from 'isomorphic-dompurify';

marked.setOptions({
	breaks: true,
	gfm: true
});

export function renderMarkdown(source: string): string {
	const rawHtml = marked.parse(source || '') as string;
	return DOMPurify.sanitize(rawHtml);
}