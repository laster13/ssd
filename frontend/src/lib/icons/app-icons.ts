export type AppVisual = {
	svg: string;
	color: string;
	bg: string;
	accent: string;
};

const THEMES = {
	blue: {
		color: '#7dd3fc',
		bg: 'linear-gradient(135deg, rgba(56,189,248,0.18), rgba(37,99,235,0.14))',
		accent: 'linear-gradient(90deg, #38bdf8, #2563eb)'
	},
	green: {
		color: '#86efac',
		bg: 'linear-gradient(135deg, rgba(34,197,94,0.18), rgba(16,185,129,0.14))',
		accent: 'linear-gradient(90deg, #22c55e, #10b981)'
	},
	purple: {
		color: '#c4b5fd',
		bg: 'linear-gradient(135deg, rgba(168,85,247,0.18), rgba(124,58,237,0.14))',
		accent: 'linear-gradient(90deg, #a855f7, #7c3aed)'
	},
	orange: {
		color: '#fdba74',
		bg: 'linear-gradient(135deg, rgba(249,115,22,0.18), rgba(234,88,12,0.14))',
		accent: 'linear-gradient(90deg, #f97316, #ea580c)'
	},
	pink: {
		color: '#f9a8d4',
		bg: 'linear-gradient(135deg, rgba(236,72,153,0.18), rgba(219,39,119,0.14))',
		accent: 'linear-gradient(90deg, #ec4899, #db2777)'
	},
	yellow: {
		color: '#fde68a',
		bg: 'linear-gradient(135deg, rgba(245,158,11,0.18), rgba(234,179,8,0.14))',
		accent: 'linear-gradient(90deg, #f59e0b, #eab308)'
	},
	slate: {
		color: '#cbd5e1',
		bg: 'linear-gradient(135deg, rgba(148,163,184,0.18), rgba(100,116,139,0.14))',
		accent: 'linear-gradient(90deg, #94a3b8, #64748b)'
	}
};

function svgWrap(inner: string, color: string) {
	return `<svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="${color}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${inner}</svg>`;
}

const ICONS = {
	shield: (color: string) =>
		svgWrap('<path d="M12 3l7 4v5c0 5-3.5 8-7 9-3.5-1-7-4-7-9V7l7-4z"/>', color),
	folder: (color: string) =>
		svgWrap('<path d="M3 7h5l2 2h11v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7z"/>', color),
	book: (color: string) =>
		svgWrap('<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 17A2.5 2.5 0 0 0 4 19.5V5a2 2 0 0 1 2-2h14v14"/>', color),
	image: (color: string) =>
		svgWrap('<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.5"/><path d="M21 15l-5-5-8 8"/>', color),
	play: (color: string) =>
		svgWrap('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M10 9l5 3-5 3z"/>', color),
	cloud: (color: string) =>
		svgWrap('<path d="M18 18H7a4 4 0 1 1 .8-7.9A5 5 0 0 1 18 9a4 4 0 1 1 0 9z"/>', color),
	database: (color: string) =>
		svgWrap('<ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v6c0 1.7 3.1 3 7 3s7-1.3 7-3V5"/><path d="M5 11v6c0 1.7 3.1 3 7 3s7-1.3 7-3v-6"/>', color),
	monitor: (color: string) =>
		svgWrap('<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8"/><path d="M12 16v4"/>', color),
	gamepad: (color: string) =>
		svgWrap('<path d="M6 12h12a3 3 0 0 1 3 3v1a3 3 0 0 1-3 3h-1l-2-2H9l-2 2H6a3 3 0 0 1-3-3v-1a3 3 0 0 1 3-3z"/><path d="M8 12V9a4 4 0 0 1 8 0v3"/><path d="M8 15h2"/><path d="M9 14v2"/><circle cx="16.5" cy="14.5" r=".5"/><circle cx="18.5" cy="16.5" r=".5"/>', color),
	rss: (color: string) =>
		svgWrap('<path d="M5 19a2 2 0 1 0 0-.01"/><path d="M4 11a9 9 0 0 1 9 9"/><path d="M4 4a16 16 0 0 1 16 16"/>', color),
	music: (color: string) =>
		svgWrap('<path d="M9 18V6l10-2v12"/><circle cx="6" cy="18" r="3"/><circle cx="16" cy="16" r="3"/>', color),
	globe: (color: string) =>
		svgWrap('<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18"/><path d="M12 3a15 15 0 0 0 0 18"/>', color),
	file: (color: string) =>
		svgWrap('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/>', color),
	download: (color: string) =>
		svgWrap('<path d="M12 3v12"/><path d="M7 10l5 5 5-5"/><path d="M5 21h14"/>', color),
	harddrive: (color: string) =>
		svgWrap('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h.01"/><path d="M11 10h6"/><path d="M7 14h.01"/><path d="M11 14h6"/>', color),
	search: (color: string) =>
		svgWrap('<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.3-4.3"/>', color),
	users: (color: string) =>
		svgWrap('<path d="M16 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="9.5" cy="7" r="3"/><path d="M20 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 4.13a3 3 0 0 1 0 5.74"/>', color),
	server: (color: string) =>
		svgWrap('<rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><path d="M7 7h.01"/><path d="M7 17h.01"/>', color),
	film: (color: string) =>
		svgWrap('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 5v14"/><path d="M17 5v14"/><path d="M3 9h4"/><path d="M17 9h4"/><path d="M3 15h4"/><path d="M17 15h4"/>', color),
	boxes: (color: string) =>
		svgWrap('<path d="M3 7l9-4 9 4-9 4-9-4z"/><path d="M3 7v10l9 4 9-4V7"/><path d="M12 11v10"/>', color),
	terminal: (color: string) =>
		svgWrap('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3"/><path d="M13 15h4"/>', color),
	lock: (color: string) =>
		svgWrap('<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>', color),
	layout: (color: string) =>
		svgWrap('<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18"/><path d="M9 10v10"/>', color),
	mail: (color: string) =>
		svgWrap('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', color),
	calendar: (color: string) =>
		svgWrap('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4"/><path d="M8 3v4"/><path d="M3 11h18"/>', color),
	activity: (color: string) =>
		svgWrap('<path d="M3 12h4l2-5 4 10 2-5h6"/>', color),
	help: (color: string) =>
		svgWrap('<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 4.2 1.8c-.9.8-1.7 1.3-1.7 2.7"/><path d="M12 17h.01"/>', color)
};

function makeVisual(icon: keyof typeof ICONS, theme: keyof typeof THEMES): AppVisual {
	const t = THEMES[theme];
	return {
		svg: ICONS[icon](t.color),
		color: t.color,
		bg: t.bg,
		accent: t.accent
	};
}

export function resolveAppVisual(slug: string, description: string): AppVisual {
	const text = `${slug} ${description}`.toLowerCase();

	if (['torrent', 'usenet', 'nzb', 'download', 'debrid'].some((w) => text.includes(w))) {
		return makeVisual('download', 'blue');
	}

	if (
		['plex', 'jellyfin', 'emby', 'media', 'video', 'stremio', 'movie', 'series', 'manga'].some((w) =>
			text.includes(w)
		)
	) {
		return makeVisual('film', 'purple');
	}

	if (['music', 'lidarr', 'navidrome', 'subsonic', 'deezer'].some((w) => text.includes(w))) {
		return makeVisual('music', 'pink');
	}

	if (['photo', 'image', 'gallery', 'album', 'immich', 'piwigo', 'chevereto'].some((w) => text.includes(w))) {
		return makeVisual('image', 'pink');
	}

	if (['book', 'ebook', 'pdf', 'wiki', 'reader', 'komga', 'kavita', 'bookstack'].some((w) => text.includes(w))) {
		return makeVisual('book', 'orange');
	}

	if (['auth', 'password', 'security', 'vpn', 'wireguard', 'guard', 'proxy', 'warden'].some((w) => text.includes(w))) {
		return makeVisual('shield', 'orange');
	}

	if (['cloud', 'file', 'files', 'storage', 'webdav', 'sync', 'backup', 'nextcloud', 'seafile'].some((w) =>
			text.includes(w)
		)) {
		return makeVisual('cloud', 'blue');
	}

	if (['docker', 'container', 'compose', 'portainer', 'yacht', 'coolify'].some((w) => text.includes(w))) {
		return makeVisual('boxes', 'blue');
	}

	if (['dashboard', 'monitor', 'monitoring', 'status', 'stats', 'logs', 'health', 'kuma', 'netdata'].some((w) =>
			text.includes(w)
		)) {
		return makeVisual('activity', 'green');
	}

	if (['database', 'crm', 'nocode', 'data', 'bdd', 'baserow', 'nocodb', 'grist'].some((w) => text.includes(w))) {
		return makeVisual('database', 'green');
	}

	if (['browser', 'desktop', 'terminal', 'remote', 'web client', 'vscode', 'kasm', 'neko', 'wetty'].some((w) =>
			text.includes(w)
		)) {
		return makeVisual('monitor', 'purple');
	}

	if (['game', 'minecraft', 'pterodactyl'].some((w) => text.includes(w))) {
		return makeVisual('gamepad', 'green');
	}

	if (['rss', 'news', 'feed', 'flux', 'freshrss', 'ttrss'].some((w) => text.includes(w))) {
		return makeVisual('rss', 'orange');
	}

	if (['mail', 'cypht'].some((w) => text.includes(w))) {
		return makeVisual('mail', 'blue');
	}

	if (['calendar', 'baikal'].some((w) => text.includes(w))) {
		return makeVisual('calendar', 'blue');
	}

	if (['wordpress', 'pastebin', 'microbin', 'stirlingpdf', 'paperless'].some((w) => text.includes(w))) {
		return makeVisual('file', 'orange');
	}

	if (['homarr', 'heimdall', 'organizr', 'homepage'].some((w) => text.includes(w))) {
		return makeVisual('layout', 'blue');
	}

	if (['jitsi', 'mattermost', 'users', 'wizarr', 'monica'].some((w) => text.includes(w))) {
		return makeVisual('users', 'purple');
	}

	if (['search', 'jackett', 'prowlarr', 'hydra', 'ygege', 'zilean'].some((w) => text.includes(w))) {
		return makeVisual('search', 'yellow');
	}

	if (['server'].some((w) => text.includes(w))) {
		return makeVisual('server', 'green');
	}

	return makeVisual('help', 'slate');
}