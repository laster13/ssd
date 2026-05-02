export type TutorialTheme = {
	badge: string;
	title: string;
	sectionTitle: string;
	panel: string;
	panelSoft: string;
	border: string;
	callout: string;
	code: string;
};

function normalize(value: string) {
	return value
		.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')
		.trim()
		.toLowerCase();
}

const fallbackTheme: TutorialTheme = {
	badge:
		'border-zinc-200 bg-zinc-50 text-zinc-700 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-200',
	title:
		'bg-gradient-to-r from-zinc-900 via-zinc-700 to-zinc-900 bg-clip-text text-transparent dark:from-white dark:via-zinc-200 dark:to-white',
	sectionTitle: 'text-zinc-900 dark:text-zinc-100',
	panel: 'border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900',
	panelSoft: 'bg-zinc-50 dark:bg-zinc-800/40',
	border: 'bg-zinc-200 dark:bg-zinc-800',
	callout:
		'border-zinc-200 bg-zinc-50 text-zinc-700 dark:border-zinc-700 dark:bg-zinc-800/50 dark:text-zinc-200',
	code: 'border-zinc-200 bg-zinc-950 text-zinc-100 dark:border-zinc-700 dark:bg-black'
};

const sharedTheme: TutorialTheme = {
	badge:
		'border-sky-200 bg-sky-50 text-sky-700 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-300',
	title:
		'bg-gradient-to-r from-sky-500 via-blue-600 to-cyan-500 bg-clip-text text-transparent',
	sectionTitle: 'text-sky-700 dark:text-sky-300',
	panel: 'border-sky-100 bg-white dark:border-sky-500/10 dark:bg-zinc-900',
	panelSoft: 'bg-sky-50 dark:bg-sky-500/8',
	border: 'bg-sky-200 dark:bg-sky-500/20',
	callout:
		'border-sky-200 bg-sky-50 text-sky-800 dark:border-sky-500/20 dark:bg-sky-500/10 dark:text-sky-200',
	code: 'border-sky-200 bg-slate-950 text-sky-50 dark:border-sky-500/20 dark:bg-black'
};

export function getTutorialTheme(category?: string): TutorialTheme {
	const key = normalize(category ?? '');

	if (
		key === 'configuration' ||
		key === 'securite' ||
		key === 'installation'
	) {
		return sharedTheme;
	}

	return fallbackTheme;
}