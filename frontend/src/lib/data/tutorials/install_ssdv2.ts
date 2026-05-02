import type { Tutorial } from './types';

export const introductionPrerequisSsdv2: Tutorial = {
  slug: 'introduction-prerequis-ssdv2',
  title: 'Introduction & prérequis — SSDV2',
  description:
    'Guide d’onboarding SSDV2 : architecture globale, prérequis techniques, domaine, VPS, compatibilité OS/CPU, coûts estimés et checklist avant installation.',
  summary:
    'Cette page sert de point d’entrée SSDV2. Elle explique la logique globale du setup — domaine, serveur, Docker, Traefik, apps et AllDebrid — puis détaille les prérequis indispensables pour démarrer proprement. Le guide est pensé pour être suivi dans l’ordre afin de limiter les erreurs classiques et poser une base propre avant l’installation.',
  level: 'débutant',
  duration: '15 à 30 min',
  estimatedTime:
    'Environ 15 à 30 minutes pour vérifier les prérequis, préparer le serveur, valider le domaine, et confirmer que l’environnement est prêt pour la suite.',
  category: 'Installation',
  group: 'Installation SSDv2',
  icon: 'rocket',
  tags: [
    'ssdv2',
    'introduction',
    'prerequis',
    'vps',
    'plex',
    'alldebrid',
    'domaine',
    'docker',
    'traefik',
    'onboarding'
  ],
  prerequisites: [
    'Un serveur ou VPS prêt à être utilisé',
    'Un accès SSH fonctionnel ou la possibilité de le configurer',
    'Un nom de domaine avec accès DNS',
    'Un compte AllDebrid',
    'Optionnel : Cloudflare pour faciliter la gestion DNS',
    'Optionnel : Plex Pass selon votre usage'
  ],
  access: [],
  links: [],
  callouts: [
    {
      tone: 'abstract',
      title: 'Abstract',
      content: [
        'SSDV2 vous guide de zéro à un serveur opérationnel : préparation du système, sécurisation SSH, mise en place de Docker et Traefik, puis intégration des applications médias.',
        'Cette page pose les fondations : architecture, prérequis, ordre logique de progression, coûts et checklist avant de passer aux étapes d’installation.'
      ]
    },
    {
      tone: 'tip',
      title: 'Raccourci mental',
      content: [
        'Domaine = accès propre via sous-domaines.',
        'Serveur = exécution des conteneurs.',
        'Apps = services métiers.',
        'AllDebrid = source contenu selon votre pipeline.'
      ]
    }
  ],
  warnings: [
    'Ne commencez pas par les apps avant d’avoir validé la base système et l’accès SSH.',
    'N’exposez jamais plus de ports que nécessaire.',
    'Privilégiez 80/443 via reverse proxy plutôt qu’une exposition brute de multiples services.',
    'Assurez-vous d’avoir un utilisateur non-root fonctionnel avant de renforcer la sécurité SSH.',
    'Le coût réel dépend surtout du VPS et de la stratégie d’hébergement choisie.'
  ],
  sections: [
    {
      id: 'tldr',
      title: 'l’essentiel en quelques points',
      icon: 'rocket',
      items: [
        'Préparer un serveur compatible avec au moins 4 vCores et 8 Go de RAM',
        'Prendre un nom de domaine et idéalement utiliser Cloudflare',
        'Créer les comptes nécessaires, notamment AllDebrid',
        'Vérifier la compatibilité OS et architecture',
        'Suivre l’ordre du guide : sécurité → installation → configuration apps → optimisation'
      ]
    },
    {
      id: 'introduction',
      title: 'Introduction',
      icon: 'sparkles',
      body: [
        'Bienvenue dans ce guide complet d’installation et de configuration d’un serveur avec SSDV2.',
        'Il a été pensé pour accompagner à la fois les débutants, avec des étapes guidées et des choix simplifiés, et les utilisateurs avancés, avec des options, optimisations et bonnes pratiques.',
        'L’objectif est d’obtenir une plateforme sécurisée, performante et personnalisée pour le streaming, le stockage et l’automatisation média.'
      ],
      tabs: [
        {
          label: 'Débutants',
          content: [
            'Le guide donne une progression claire, avec un ordre logique et des garde-fous pour éviter les erreurs classiques.'
          ]
        },
        {
          label: 'Utilisateurs avancés',
          content: [
            'Le guide reste compatible avec une approche plus experte, orientée optimisation, modularité et bonnes pratiques d’infrastructure.'
          ]
        }
      ]
    },
    {
      id: 'architecture-globale',
      title: 'Architecture globale',
      icon: 'server',
      body: [
        'Le domaine sert à exposer vos services proprement via des sous-domaines.',
        'Le serveur héberge Docker et exécute l’ensemble des services.',
        'Traefik centralise l’accès HTTP/HTTPS et joue le rôle de reverse proxy.',
        'Les applications comme Plex, les Arr, Prowlarr ou Overseerr communiquent entre elles pour automatiser le pipeline.',
        'AllDebrid s’intègre dans la chaîne selon votre usage et votre organisation.'
      ],
      diagrams: [
        {
          title: 'Vue d’ensemble SSDV2',
          code:
            'flowchart LR\n' +
            '  U["👤 Utilisateur"] --> O["🌐 Domaine + DNS\\n(sous-domaines)"]\n' +
            '  U --> P["🖥️ VPS / Serveur\\n(Ubuntu/Debian)"]\n' +
            '  P --> S["🔐 SSH\\n(non-root)"]\n' +
            '  P --> D["🐳 Docker/Compose\\n+ Traefik"]\n' +
            '  D --> A["🧩 Apps\\nPlex, Arr, Prowlarr,\\nOverseerr..."]\n' +
            '  A --> M["📚 Médias\\nFilms/Séries/4K"]\n' +
            '  AD["⚡ AllDebrid"] --> A\n' +
            '  A --> UX["✅ UX\\nStreaming + Requests\\n+ Automatisation"]'
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Lecture rapide',
          content: [
            'Le domaine structure l’accès.',
            'Le serveur exécute Docker.',
            'Traefik expose les services proprement.',
            'AllDebrid alimente la chaîne selon votre pipeline.',
            'Les apps s’interconnectent pour automatiser le tout.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Pourquoi cette séparation est importante ?',
          content: [
            'Séparer mentalement domaine, reverse proxy, serveur et applications évite beaucoup de confusion pendant l’installation. Chaque couche a un rôle précis, ce qui simplifie la maintenance et le diagnostic.'
          ]
        }
      ]
    },
    {
      id: 'prerequis',
      title: 'Prérequis',
      icon: 'check-circle',
      body: [
        'Avant de lancer l’installation, vous devez valider quatre blocs : le serveur, la compatibilité OS/CPU, les comptes/services, et le budget.',
        'Plus cette base est propre au départ, moins vous rencontrerez de problèmes ensuite.'
      ],
      tabs: [
        {
          label: 'Technique',
          content: [
            'Serveur compatible, OS supporté, accès SSH, DNS maîtrisé.'
          ]
        },
        {
          label: 'Services',
          content: [
            'Compte AllDebrid, nom de domaine, éventuellement Plex Pass.'
          ]
        },
        {
          label: 'Méthode',
          content: [
            'Suivre l’ordre recommandé : sécurité d’abord, apps ensuite.'
          ]
        }
      ]
    },
    {
      id: 'serveur',
      title: 'Serveur',
      icon: 'cpu',
      body: [
        'Pour une expérience confortable, SSDV2 vise un serveur capable de gérer plusieurs services simultanément sans saturation rapide.',
        'Ce palier évite de se retrouver limité trop tôt lorsque Docker, Plex, les apps Arr, les indexers et les tâches de fond tournent ensemble.'
      ],
      table: {
        columns: ['Composant', 'Recommandé', 'Pourquoi'],
        rows: [
          ['CPU', '≥ 4 vCores', 'Indexations, scans, services multiples'],
          ['RAM', '≥ 8 Go', 'Marge pour Docker, apps et monitoring'],
          ['Réseau', '1 Gb/s', 'Accès rapide et bonne stabilité'],
          ['Stockage', 'Selon usage', 'Dépend du volume et de votre stratégie']
        ]
      },
      callouts: [
        {
          tone: 'info',
          title: 'Direct play',
          content: [
            'Pour une expérience fluide, surtout en direct play, ce niveau de ressources représente un bon équilibre entre coût et confort.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Est-ce que moins peut fonctionner ?',
          content: [
            'Oui, dans certains cas. Mais le guide part d’une base confortable pour réduire les compromis et éviter les lenteurs dès que plusieurs services tournent en parallèle.'
          ]
        }
      ]
    },
    {
      id: 'pare-feu-ports',
      title: 'Pare-feu / ports',
      icon: 'shield',
      body: [
        'Plex utilise classiquement le port 32400.',
        'Selon votre architecture, notamment avec reverse proxy, tunnel ou exposition directe, l’ouverture réelle des ports peut varier.',
        'L’approche recommandée consiste à réduire au strict minimum la surface exposée.'
      ],
      tabs: [
        {
          label: 'Approche recommandée',
          content: [
            'Privilégiez une exposition contrôlée via 80/443 à travers Traefik lorsque c’est possible.'
          ]
        },
        {
          label: 'À éviter',
          content: [
            'Ouvrir de nombreux ports applicatifs sans nécessité ni logique d’ensemble.'
          ]
        }
      ],
      callouts: [
        {
          tone: 'warning',
          title: 'Exposition réseau',
          content: [
            'N’exposez jamais tout.',
            'Ouvrez uniquement le nécessaire.',
            'Passez par un reverse proxy quand c’est possible.'
          ]
        }
      ]
    },
    {
      id: 'compatibilite-os-cpu',
      title: 'Compatibilité processeurs & OS',
      icon: 'settings',
      body: [
        'La cible principale reste Ubuntu Server 24.04 en amd64.',
        'Les compatibilités annoncées couvrent également Ubuntu Server 18.04 à 24.04, Debian 9 à 12, ainsi que les architectures amd64 et arm64.'
      ],
      tabs: [
        {
          label: 'Cible principale',
          content: [
            'Ubuntu Server 24.04 (amd64).'
          ]
        },
        {
          label: 'Compatibilités annoncées',
          content: [
            'Ubuntu Server 18.04 à 24.04.',
            'Debian 9 à 12.',
            'Architectures amd64 et arm64.'
          ]
        }
      ],
      callouts: [
        {
          tone: 'tip',
          title: 'Choix recommandé',
          content: [
            'Si vous partez de zéro, privilégiez une version stable, récente et largement supportée comme Ubuntu 20.04/24.04 ou Debian 11/12.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Pourquoi rester sur une base très standard ?',
          content: [
            'Plus l’OS est courant et bien supporté, plus les recettes, conteneurs, dépendances et procédures de dépannage restent prévisibles.'
          ]
        }
      ]
    },
    {
      id: 'comptes-services',
      title: 'Comptes & services',
      icon: 'key',
      table: {
        columns: ['Service', 'Obligatoire', 'Coût estimé', 'Rôle'],
        rows: [
          ['AllDebrid', 'Oui', '~32 €/an', 'Source ou accès contenus selon pipeline'],
          ['Nom de domaine', 'Oui', '~15 €/an', 'Sous-domaines pour apps et panels'],
          ['Plex Pass', 'Non', '~60 €/an', 'Confort Plex mobile selon usage']
        ]
      },
      callouts: [
        {
          tone: 'tip',
          title: 'Priorité',
          content: [
            'Si vous devez arbitrer, commencez par le domaine et AllDebrid. Plex Pass reste optionnel selon votre usage.'
          ]
        }
      ]
    },
    {
      id: 'couts-estimes',
      title: 'Coûts estimés',
      icon: 'wallet',
      items: [
        '~21,41 € / mois',
        '~257 € / an'
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Variables',
          content: [
            'Le coût réel dépend principalement du VPS, du domaine, des options éventuelles comme Plex Pass et de votre mode d’hébergement.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Quel est le vrai poste principal ?',
          content: [
            'Dans la plupart des cas, le VPS reste le premier poste de dépense. Le domaine et AllDebrid sont généralement plus stables et plus faciles à anticiper.'
          ]
        }
      ]
    },
    {
      id: 'checklist-pret-a-commencer',
      title: 'Checklist prêt à commencer',
      icon: 'check-circle',
      items: [
        'Serveur prêt avec au moins 4 vCores et 8 Go de RAM',
        'OS compatible Ubuntu/Debian en amd64 ou arm64',
        'Compte AllDebrid créé',
        'Nom de domaine disponible avec accès DNS',
        'Accès SSH fonctionnel',
        'Ordre du guide compris : sécurité → installation → intégrations'
      ]
    },
    {
      id: 'onboarding-sequence',
      title: 'Onboarding (séquence)',
      icon: 'sync',
      diagrams: [
        {
          title: 'Séquence de démarrage SSDV2',
          code:
            'sequenceDiagram\n' +
            '  autonumber\n' +
            '  actor U as Utilisateur\n' +
            '  participant VPS as Serveur (VPS)\n' +
            '  participant DNS as Domaine/DNS\n' +
            '  participant SSD as SSDV2\n' +
            '  participant Apps as Apps (Plex/Arr/Indexers)\n\n' +
            '  U->>VPS: Provisionner serveur + SSH\n' +
            '  U->>VPS: Préparer OS (updates, user non-root)\n' +
            '  U->>DNS: Configurer domaine + sous-domaines\n' +
            '  U->>SSD: Lancer installation SSDV2\n' +
            '  SSD->>Apps: Déployer apps (Docker)\n' +
            '  U->>Apps: Configurer Plex/Arr/Prowlarr/Overseerr\n' +
            '  Apps-->>U: Streaming + requests + automatisation OK'
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Une plateforme stable, accessible via sous-domaines, sécurisée et prête pour l’automatisation.'
          ]
        }
      ]
    }
  ],
  steps: [
    {
      title: 'Préparer le serveur',
      text:
        'Choisissez un VPS ou un serveur avec une base confortable, idéalement 4 vCores, 8 Go de RAM et une connectivité correcte.',
      result:
        'Vous devez disposer d’une machine capable d’héberger Docker, Traefik et plusieurs applications.',
      icon: 'server'
    },
    {
      title: 'Valider l’OS et l’architecture',
      text:
        'Assurez-vous que votre système correspond à une base compatible, idéalement Ubuntu 20.04/22.04 ou Debian 11/12 en amd64 ou arm64.',
      result:
        'Le socle système doit être cohérent avec SSDV2 et ses recettes.',
      icon: 'settings'
    },
    {
      title: 'Préparer le domaine et le DNS',
      text:
        'Achetez ou utilisez un domaine existant et assurez-vous d’avoir la main sur sa gestion DNS pour créer vos futurs sous-domaines.',
      result:
        'Le domaine doit être prêt pour exposer proprement vos services.',
      icon: 'globe'
    },
    {
      title: 'Créer les comptes nécessaires',
      text:
        'Préparez votre compte AllDebrid et, selon vos usages, Plex Pass si vous en avez besoin.',
      result:
        'Les services externes nécessaires doivent être prêts avant la configuration applicative.',
      icon: 'key'
    },
    {
      title: 'Vérifier l’accès SSH',
      text:
        'Confirmez que vous pouvez administrer le serveur à distance sans risque de lock-out, idéalement avec un utilisateur non-root prêt à être utilisé.',
      result:
        'La base d’administration du serveur doit être saine et fiable.',
      icon: 'shield'
    },
    {
      title: 'Suivre l’ordre du guide',
      text:
        'Commencez par la sécurité, continuez avec l’installation, puis passez à la configuration des apps et enfin aux optimisations.',
      result:
        'Vous avancez dans le bon ordre avec une base propre et maintenable.',
      icon: 'sparkles'
    }
  ],
  troubleshooting: [
    'Si votre serveur est trop léger, vous risquez des lenteurs dès que plusieurs apps tournent ensemble.',
    'Si vous n’avez pas encore de domaine, ne sautez pas cette étape : elle structure toute l’exposition du setup.',
    'Si votre SSH n’est pas fiable, corrigez cela avant tout durcissement.',
    'Si vous hésitez entre plusieurs OS, choisissez une version stable et largement supportée.',
    'Si le budget est serré, gardez en priorité le domaine et AllDebrid, puis adaptez le VPS.'
  ],
  checklist: [
    { text: 'Serveur prêt avec au moins 4 vCores et 8 Go de RAM' },
    { text: 'OS compatible Ubuntu ou Debian validé' },
    { text: 'Architecture amd64 ou arm64 confirmée' },
    { text: 'Compte AllDebrid créé' },
    { text: 'Nom de domaine disponible avec accès DNS' },
    { text: 'Accès SSH fonctionnel' },
    { text: 'Ordre du parcours SSDV2 compris' }
  ],
  finalChecklist: [
    'Le serveur est prêt pour SSDV2',
    'Le domaine et les accès essentiels sont disponibles',
    'Le compte AllDebrid est prêt',
    'Vous pouvez commencer la séquence sécurité → installation → intégrations'
  ]
};