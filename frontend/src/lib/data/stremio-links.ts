export type LinkCategory =
	| 'agrégateurs'
	| 'catalogues'
	| 'sous-titres'
	| 'guides'
	| 'outils';

export type StremioLink = {
	title: string;
	description: string;
	url: string;
	category: LinkCategory;
	internal?: boolean;
	tags?: string[];
	featured?: boolean;
	status?: 'stable' | 'beta' | 'communauté';
};

export const stremioLinks: StremioLink[] = [
	{
		title: 'StreamFusion',
		description:
			'Agrégateur avancé pour centraliser des sources et affiner les résultats.',
		url: '/settings/streamfusion',
		internal: true,
		category: 'agrégateurs',
		tags: ['agrégateur', 'sources', 'filtres', 'personnalisation'],
		featured: true,
		status: 'stable'
	},
	{
		title: 'Torrentio',
		description:
			'Configuration directe de l’addon avec filtres fournisseurs, qualité et options premium.',
		url: 'https://torrentio.strem.fun/configure',
		category: 'agrégateurs',
		tags: ['torrent', 'configuration', 'fournisseurs', 'qualité'],
		featured: true,
		status: 'stable'
	},
	{
		title: 'Comet',
		description:
			'Moteur rapide de recherche torrent/debrid avec configuration dédiée.',
		url: 'https://comet.elfhosted.com/',
		category: 'agrégateurs',
		tags: ['torrent', 'debrid', 'recherche', 'configuration'],
		featured: true,
		status: 'communauté'
	},
	{
		title: 'Frenchio',
		description:
			'Trackers francophones couplés à debrid ou qBittorrent, avec priorisation des sources.',
		url: 'https://frenchio.elfhosted.com/',
		category: 'agrégateurs',
		tags: ['trackers', 'francophone', 'debrid', 'qBittorrent'],
		featured: true,
		status: 'communauté'
	},
	{
		title: 'WAStream',
		description:
			'Stremio addon to convert DDL to streams via debrid services.',
		url: 'https://wastream.striho.top/configure/',
		category: 'agrégateurs',
		tags: ['ddl', 'streams', 'debrid', 'conversion'],
		featured: true,
		status: 'communauté'
	},
	{
		title: 'AIOLists',
		description:
			'Importe vos listes Trakt, MDBList et autres dans Stremio, avec fusion et recherche unifiée.',
		url: 'https://aiolists.elfhosted.com',
		category: 'outils',
		tags: ['listes', 'trakt', 'mdblist', 'import'],
		featured: true,
		status: 'communauté'
	},
	{
		title: 'AIOStreams',
		description:
			'Interface tout-en-un pour combiner plusieurs addons et centraliser la configuration.',
		url: 'https://aiostreams.elfhosted.com/configure',
		category: 'outils',
		tags: ['tout-en-un', 'multi-addons', 'configuration', 'flux'],
		featured: true,
		status: 'communauté'
	},
	{
		title: 'MediaFusion',
		description:
			'Alternative configurable pour agréger des flux, catalogues et services compatibles.',
		url: 'https://mediafusion.elfhosted.com/configure',
		category: 'agrégateurs',
		tags: ['agrégateur', 'flux', 'catalogues', 'configuration'],
		status: 'communauté'
	},
	{
		title: 'AIOMetadata',
		description:
			'Remplace Cinemeta avec des métadonnées enrichies depuis TMDB et MDBList.',
		url: 'https://aiometadata.elfhosted.com/configure/',
		category: 'catalogues',
		tags: ['métadonnées', 'cinemeta', 'tmdb', 'mdblist'],
		status: 'communauté'
	},
	{
		title: 'The Movie DB',
		description:
			'Intègre les données TMDb dans Stremio pour une meilleure expérience de navigation.',
		url: 'https://tmdb.elfhosted.com/',
		category: 'catalogues',
		tags: ['tmdb', 'métadonnées', 'navigation', 'intégration'],
		status: 'communauté'
	},
	{
		title: 'AIOManager',
		description:
			'Un manager de compte Stremio pensé pour combler tous vos besoins en un seul addon.',
		url: 'https://aiomanager.elfhosted.com/',
		category: 'outils',
		tags: ['gestion', 'compte', 'tout-en-un', 'addon'],
		status: 'communauté'
	},
	{
		title: 'Cyberflix Catalog',
		description:
			'Catalogue orienté découverte pour enrichir la navigation et la sélection de contenus.',
		url: 'https://stremio-addons.com/cyberflix-catalog.html',
		category: 'catalogues',
		tags: ['catalogue', 'découverte', 'navigation', 'sélection'],
		status: 'communauté'
	}
];