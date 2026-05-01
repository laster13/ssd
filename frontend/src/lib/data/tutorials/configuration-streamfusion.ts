import type { Tutorial } from './types';

export const configurationStreamFusion: Tutorial = {
  slug: 'configuration-streamfusion',
  title: 'Configuration StreamFusion',
  description:
    'Guide complet de configuration, synchronisation, enrichissement IMDB et sauvegarde après installation via SSDv2.',
  summary:
    'Ce tutoriel accompagne la mise en route complète de StreamFusion après installation. Il couvre l’accès admin, les synchronisations initiales, la vérification de la base DuckDB, le Parsing RTN, l’IMDB Enrich, la sauvegarde PostgreSQL et la création d’une clé API utilisateur.',
  level: 'intermédiaire',
  duration: '15 h',
  estimatedTime:
    'Environ 15 heures au total, dont environ 10 heures pour les synchronisations initiales.',
  category: 'Configuration',
  group: 'Guides',
  icon: 'settings',
  tags: [
    'streamfusion',
    'ssdv2',
    'configuration',
    'synchronisation',
    'imdb',
    'duckdb',
    'postgresql',
    'backup'
  ],
  access: [
    {
      label: 'Panneau admin',
      url: 'https://streamfusion.ltd/admin'
    },
    {
      label: 'Configuration utilisateur',
      url: 'https://streamfusion.ltd/configure'
    },
    {
      label: 'Documentation officielle',
      url: 'https://docs.streamfusion.link/'
    }
  ],
  links: [
    {
      label: 'Admin StreamFusion',
      url: 'https://streamfusion.ltd/admin'
    },
    {
      label: 'Configuration StreamFusion',
      url: 'https://streamfusion.ltd/configure'
    },
    {
      label: 'Documentation officielle',
      url: 'https://docs.streamfusion.link/'
    }
  ],
  prerequisites: [
    'StreamFusion doit déjà être installé via SSDv2',
    'Le domaine streamfusion.ltd doit pointer vers ton instance',
    'Tu dois disposer de l’API key définie lors de l’installation',
    'Les conteneurs Docker StreamFusion et PostgreSQL doivent être démarrés',
    'Les volumes nécessaires doivent être montés correctement'
  ],
  callouts: [
    {
      tone: 'abstract',
      title: 'Résumé',
      content: [
        'Ce guide explique la configuration complète de StreamFusion après installation via SSDv2.',
        'Il couvre l’accès au panneau admin, les synchronisations initiales, la vérification de la base DuckDB, le Parsing RTN, l’IMDB Enrich, la sauvegarde PostgreSQL et la finalisation côté utilisateur.'
      ]
    }
  ],
  warnings: [
    'La première synchronisation peut être très longue. Ne coupe pas les traitements pendant leur exécution.',
    'Si une tâche semble bloquée, utilise “Libérer le verrou” avant de relancer.',
    'Vérifie bien le nom réel de tes conteneurs Docker avant d’exécuter les commandes.'
  ],
  sections: [
    {
      id: 'essentiel',
      title: 'L’essentiel',
      icon: 'rocket',
      items: [
        'Ouvrir le panneau admin et se connecter avec l’API key d’installation',
        'Lancer DDM Sync, Sync U2P Nostr et IMDB Synch',
        'Vérifier que la base DuckDB IMDB se construit correctement',
        'Lancer Parsing RTN puis IMDB Enrich',
        'Créer une sauvegarde PostgreSQL',
        'Générer une nouvelle clé API utilisateur et finaliser la configuration'
      ]
    },
    {
      id: 'acces',
      title: 'Accès utiles',
      icon: 'server',
      tabs: [
        {
          label: 'Admin',
          content: [
            'Le panneau d’administration est accessible à l’adresse https://streamfusion.ltd/admin.',
            'Tu dois t’y connecter avec l’API key définie pendant l’installation.'
          ]
        },
        {
          label: 'Configuration',
          content: [
            'La configuration utilisateur finale se fait à l’adresse https://streamfusion.ltd/configure.',
            'Tu y colleras la nouvelle clé API générée après la fin des traitements.'
          ]
        },
        {
          label: 'Documentation',
          content: [
            'La documentation officielle est disponible sur https://docs.streamfusion.link/.'
          ]
        }
      ]
    },
    {
      id: 'objectif-du-guide',
      title: 'Objectif du guide',
      icon: 'sparkles',
      items: [
        'Accéder au panneau admin et s’authentifier',
        'Lancer les synchronisations DDM, U2P Nostr et IMDB',
        'Contrôler la construction de la base DuckDB',
        'Exécuter Parsing RTN puis IMDB Enrich',
        'Créer une sauvegarde PostgreSQL',
        'Générer une nouvelle clé API utilisateur et finaliser la configuration'
      ]
    },
    {
      id: 'synchronisations-initiales',
      title: 'Synchronisations initiales',
      icon: 'sync',
      tabs: [
        {
          label: 'Tâches à lancer',
          content: [
            'Depuis le panneau admin, lance les trois tâches prioritaires suivantes : DDM Sync, Sync U2P Nostr et IMDB Synch.',
            'Ces traitements doivent être démarrés dès le départ pour initialiser correctement les données.'
          ]
        },
        {
          label: 'Durée',
          content: [
            'La phase initiale est longue et peut prendre environ 15 heures.',
            'Dans cette période, le plus important est de laisser les traitements se dérouler sans interruption.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Si la synchronisation ne démarre pas',
          content: [
            'Si les données ne chargent pas, si une tâche semble bloquée dès le début ou si l’interface ne progresse pas, clique sur “Libérer le verrou”, puis relance la tâche concernée.'
          ]
        },
        {
          title: 'Si aucun fichier IMDB n’apparaît',
          content: [
            'Vérifie le conteneur StreamFusion et les volumes montés.',
            'L’absence de fichiers IMDB peut indiquer que la synchronisation n’a pas réellement démarré.'
          ]
        }
      ]
    },
    {
      id: 'verification-duckdb',
      title: 'Vérification de la base DuckDB',
      icon: 'database',
      body: [
        'Pendant la synchronisation, vérifie que la base DuckDB IMDB se construit correctement dans le conteneur StreamFusion.',
        'Cette vérification permet de confirmer que la partie IMDB avance réellement.'
      ],
      codeBlocks: [
        {
          title: 'Commande de vérification',
          language: 'bash',
          code: 'docker exec -it -w /data/imdb_db streamfusion ls'
        }
      ],
      tabs: [
        {
          label: 'Résultat attendu',
          content: [
            'Les éléments wheel et imdb.duckdb doivent apparaître dans le dossier.'
          ]
        },
        {
          label: 'Interprétation',
          content: [
            'Si imdb.duckdb est présent, la base se construit correctement.',
            'Si wheel est présent, le processus semble actif.',
            'Si aucun fichier n’est visible, la synchronisation n’a peut-être pas démarré.',
            'En cas d’erreur Docker, vérifie le nom exact du conteneur StreamFusion.'
          ]
        }
      ]
    },
    {
      id: 'enrichissement-des-donnees',
      title: 'Parsing RTN et IMDB Enrich',
      icon: 'sparkles',
      body: [
        'Une fois les synchronisations initiales terminées, retourne dans le panneau admin.',
        'Lance d’abord Parsing RTN pour analyser et préparer les résultats.',
        'Quand Parsing RTN est terminé, lance IMDB Enrich pour enrichir les données avec les métadonnées IMDB.'
      ],
      accordions: [
        {
          title: 'Ordre recommandé',
          content: [
            '1. Parsing RTN',
            '2. Attendre la fin complète du traitement',
            '3. IMDB Enrich'
          ]
        },
        {
          title: 'Point d’attention',
          content: [
            'Ne lance pas IMDB Enrich avant la fin réelle du Parsing RTN.'
          ]
        }
      ]
    },
    {
      id: 'sauvegarde-postgresql',
      title: 'Sauvegarde PostgreSQL',
      icon: 'shield',
      body: [
        'Cette étape est optionnelle mais fortement recommandée.',
        'Elle permet de sauvegarder uniquement la base PostgreSQL StreamFusion dans un fichier réutilisable.'
      ],
      codeBlocks: [
        {
          title: 'Sauvegarde PostgreSQL',
          language: 'bash',
          code:
            'docker exec stremio-postgres pg_dump -U streamfusion -d streamfusion -F c -f /tmp/streamfusion.backup\n' +
            'docker cp stremio-postgres:/tmp/streamfusion.backup ./streamfusion.backup\n' +
            'docker exec stremio-postgres rm /tmp/streamfusion.backup'
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Le fichier streamfusion.backup doit être récupéré sur ta machine.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Point à vérifier',
          content: [
            'Assure-toi que le nom du conteneur PostgreSQL est bien correct avant d’exécuter les commandes.'
          ]
        }
      ]
    },
    {
      id: 'finalisation-utilisateur',
      title: 'Finalisation côté utilisateur',
      icon: 'key',
      body: [
        'Quand tous les traitements sont terminés, retourne dans le panneau admin.',
        'Ouvre la section “Clés API”, crée une nouvelle clé API utilisateur, puis copie la clé générée.',
        'Ouvre ensuite https://streamfusion.ltd/configure puis colle cette nouvelle clé pour terminer la configuration utilisateur.'
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Une nouvelle clé API utilisateur doit être créée puis utilisée pour finaliser la configuration côté utilisateur.'
          ]
        }
      ]
    }
  ],
  steps: [
    {
      title: 'Ouvrir le panneau admin',
      text:
        'Une fois StreamFusion installé via SSDv2, ouvre le panneau d’administration à l’adresse https://streamfusion.ltd/admin puis connecte-toi avec l’API key renseignée au moment de l’installation.',
      result:
        'Le panneau admin doit être accessible et l’authentification validée.',
      icon: 'key'
    },
    {
      title: 'Lancer les synchronisations initiales',
      text:
        'Depuis le panneau admin, lance les trois tâches prioritaires suivantes : DDM Sync, Sync U2P Nostr et IMDB Synch. Elles doivent être démarrées dès le départ pour initialiser correctement les données.',
      result:
        'Les trois synchronisations doivent être déclenchées depuis l’interface admin.',
      icon: 'sync'
    },
    {
      title: 'Débloquer une tâche si nécessaire',
      text:
        'Si les données ne chargent pas, si une tâche semble bloquée dès le début ou si l’interface ne progresse pas, clique sur “Libérer le verrou”, puis relance la tâche concernée.',
      result:
        'Les tâches bloquées doivent pouvoir repartir après déverrouillage.',
      icon: 'wrench'
    },
    {
      title: 'Laisser les traitements se dérouler',
      text:
        'À partir de cette étape, il faut surtout laisser les traitements se dérouler sans interruption. La phase initiale peut prendre environ 15 heures.',
      result:
        'Les premières synchronisations doivent continuer jusqu’à leur fin complète.',
      icon: 'rocket'
    },
    {
      title: 'Vérifier la base DuckDB',
      text:
        'Pendant la synchronisation, vérifie que la base DuckDB IMDB se construit correctement dans le conteneur StreamFusion.',
      code: 'docker exec -it -w /data/imdb_db streamfusion ls',
      result:
        'Les éléments wheel et imdb.duckdb doivent apparaître dans le dossier.',
      icon: 'database'
    },
    {
      title: 'Lancer Parsing RTN',
      text:
        'Une fois les synchronisations initiales terminées, retourne dans le panneau admin puis lance Parsing RTN.',
      result:
        'Le Parsing RTN doit se lancer et aller jusqu’au bout sans interruption.',
      icon: 'sparkles'
    },
    {
      title: 'Lancer IMDB Enrich',
      text:
        'Quand Parsing RTN est terminé, lance IMDB Enrich pour enrichir les résultats avec les métadonnées IMDB.',
      result:
        'Les données doivent être enrichies avec les informations IMDB.',
      icon: 'database'
    },
    {
      title: 'Créer une sauvegarde PostgreSQL',
      text:
        'Cette étape est optionnelle mais fortement recommandée. Elle permet de sauvegarder uniquement la base PostgreSQL StreamFusion dans un fichier réutilisable.',
      code:
        'docker exec stremio-postgres pg_dump -U streamfusion -d streamfusion -F c -f /tmp/streamfusion.backup\n' +
        'docker cp stremio-postgres:/tmp/streamfusion.backup ./streamfusion.backup\n' +
        'docker exec stremio-postgres rm /tmp/streamfusion.backup',
      result:
        'Le fichier streamfusion.backup doit être récupéré sur ta machine.',
      icon: 'shield'
    },
    {
      title: 'Créer une nouvelle clé API utilisateur',
      text:
        'Quand tous les traitements sont terminés, retourne dans le panneau admin, ouvre la section “Clés API”, crée une nouvelle clé API utilisateur, puis copie la clé générée.',
      result:
        'Une clé API utilisateur doit être créée et prête à être utilisée.',
      icon: 'key'
    },
    {
      title: 'Finaliser la configuration côté utilisateur',
      text:
        'Ouvre ensuite https://streamfusion.ltd/configure puis colle la nouvelle clé API afin de terminer la configuration utilisateur.',
      result:
        'La configuration utilisateur doit être finalisée correctement.',
      icon: 'settings'
    }
  ],
  troubleshooting: [
    'Si les données ne chargent pas, clique sur “Libérer le verrou” puis relance la tâche',
    'Si une tâche reste bloquée dès le départ, libère le verrou avant de recommencer',
    'Si aucun fichier IMDB n’apparaît, vérifie le conteneur StreamFusion et les volumes montés',
    'Si le panneau admin ne répond pas, attends un peu puis consulte les logs Docker',
    'Si la commande DuckDB échoue, vérifie le nom exact du conteneur',
    'Ne coupe pas les traitements pendant la synchronisation initiale, le Parsing RTN ou l’IMDB Enrich'
  ],
  checklist: [
    { text: 'Panneau admin accessible' },
    { text: 'Connexion validée avec l’API key d’installation' },
    { text: 'DDM Sync lancé' },
    { text: 'Sync U2P Nostr lancé' },
    { text: 'IMDB Synch lancé' },
    { text: 'wheel et imdb.duckdb visibles dans le conteneur' },
    { text: 'Parsing RTN terminé' },
    { text: 'IMDB Enrich terminé' },
    { text: 'Sauvegarde PostgreSQL créée' },
    { text: 'Nouvelle API key utilisateur générée' },
    { text: 'Configuration finale terminée sur /configure' }
  ],
  finalChecklist: [
    'Le panneau admin est accessible',
    'Les synchronisations initiales ont bien été lancées',
    'La base DuckDB IMDB est bien construite',
    'Parsing RTN et IMDB Enrich sont terminés',
    'La sauvegarde PostgreSQL est disponible',
    'La configuration utilisateur finale est terminée'
  ]
};