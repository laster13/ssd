import type { Tutorial } from './types';

export const googleOAuth2TraefikSsdv2: Tutorial = {
  slug: 'google-oauth2-traefik-ssdv2',
  title: 'Mise en place Google OAuth2 — Traefik (SSDV2)',
  description:
    'Guide premium pour activer Google OAuth2 avec Traefik : création du projet Google Cloud, écran d’autorisation, client OAuth Web, DNS Cloudflare, et bonus bypass API pour NZB360/LunaSea via labels Traefik.',
  summary:
    'Google OAuth2 permet d’utiliser un compte Google pour accéder à vos services via Traefik, avec SSO et 2FA selon votre compte. Ce tutoriel couvre la création du projet Google Cloud, l’écran d’autorisation, le client OAuth Web, la Redirect URI, la récupération du Client ID / Client Secret, et un bonus avancé pour gérer un bypass API strict pour les apps mobiles.',
  level: 'intermédiaire',
  duration: '30 à 60 min',
  estimatedTime:
    'Environ 30 à 60 minutes pour la partie OAuth, plus du temps supplémentaire pour le bypass API avancé.',
  category: 'OAuth2',
  group: 'Sécurité',
  icon: 'shield',
  tags: [
    'ssdv2',
    'traefik',
    'oauth2',
    'google',
    'sso',
    'security',
    'cloudflare',
    'nzb360',
    'lunasea'
  ],
  prerequisites: [
    'Un nom de domaine opérationnel',
    'Traefik déployé via SSDV2',
    'Accès à la Google Cloud Console avec le bon compte Google',
    'Optionnel : Cloudflare pour automatiser les enregistrements DNS via le script'
  ],
  access: [
    {
      label: 'Google Cloud Resource Manager',
      url: 'https://console.cloud.google.com/cloud-resource-manager'
    },
    {
      label: 'Console développeurs Google',
      url: 'https://console.developers.google.com'
    }
  ],
  links: [
    {
      label: 'Google Cloud Resource Manager',
      url: 'https://console.cloud.google.com/cloud-resource-manager'
    },
    {
      label: 'Console développeurs Google',
      url: 'https://console.developers.google.com'
    }
  ],
  callouts: [
    {
      tone: 'abstract',
      title: 'En Bref',
      content: [
        'Google OAuth2 permet d’utiliser un compte Google pour accéder à vos services via Traefik, avec SSO et 2FA selon votre compte.',
        'Cette page détaille : la création d’un projet Google Cloud, la configuration de l’écran d’autorisation, la génération d’un Client ID / Client Secret (application Web), et un bonus avancé : bypass d’auth via headers/query pour conserver l’accès depuis NZB360 / LunaSea tout en gardant une sécurité élevée.'
      ]
    },
    {
      tone: 'tip',
      title: 'Principe',
      content: [
        'Web = OAuth.',
        'Mobile/API = bypass strict par apikey.',
        'Le bon modèle est : 2 routes, 2 priorités, 2 middlewares.'
      ]
    }
  ],
  warnings: [
    'Assurez-vous d’être connecté au bon compte Google.',
    'Si vous avez plusieurs comptes Google, utilisez une fenêtre de navigation privée.',
    'Le bypass API doit rester strict et limité au nécessaire.',
    'Une API key doit être traitée comme un secret au même niveau qu’un mot de passe.',
    'Ne publiez jamais une API key dans un repo public, une capture ou des logs.'
  ],
  sections: [
    {
      id: 'tldr',
      title: 'l’essentiel en quelques points',
      icon: 'rocket',
      items: [
        'Créer un projet Google Cloud oauth',
        'Configurer l’écran d’autorisation en Externe',
        'Créer un client OAuth de type Application Web',
        'Définir Redirect URI : https://oauth.example.com/_oauth',
        'Récupérer Client ID et Client Secret puis configurer SSDV2/Traefik',
        'Valider le SSO',
        'Bonus : ajouter un router bypass API pour NZB360 / LunaSea'
      ]
    },
    {
      id: 'pourquoi-google-oauth2',
      title: 'Pourquoi Google OAuth2 ?',
      icon: 'key',
      items: [
        'Authentification unique SSO',
        '2FA Google selon votre configuration',
        'Liste blanche de comptes autorisés',
        'Moins de demandes de connexion répétitives',
        'Sécurité renforcée'
      ]
    },
    {
      id: 'dns-cloudflare',
      title: 'DNS (CNAME) — note Cloudflare',
      icon: 'server',
      tabs: [
        {
          label: 'Cloudflare',
          content: [
            'Si vous utilisez Cloudflare, la création du CNAME est automatisée par le script.'
          ]
        },
        {
          label: 'DNS manuel',
          content: [
            'Si vous n’utilisez pas Cloudflare, créez le CNAME chez votre registrar ou votre provider DNS.'
          ]
        }
      ],
      images: [
        {
          src: 'https://user-images.githubusercontent.com/64525827/105626357-56f06100-5e2f-11eb-815d-684ea953c4c8.png',
          alt: 'Cloudflare DNS records',
          caption: 'Exemple de records DNS Cloudflare.'
        }
      ]
    },
    {
      id: 'workflow-global',
      title: 'Vue d’ensemble (workflow)',
      icon: 'sync',
      diagrams: [
        {
          title: 'Workflow global',
          code:
            'flowchart TD\n' +
            '  A["Choisir domaine OAuth\\nex: oauth.votre_domaine.fr"] --> B["Créer projet Google Cloud (oauth)"]\n' +
            '  B --> C["Configurer écran d\\\'autorisation (externe)"]\n' +
            '  C --> D["Créer identifiants OAuth (Client ID)"]\n' +
            '  D --> E["Type: Application Web"]\n' +
            '  E --> F["Définir Redirect URI\\nhttps://oauth.example.com/_oauth"]\n' +
            '  F --> G["Récupérer Client ID + Client Secret"]\n' +
            '  G --> H["Configurer Traefik/SSDV2 avec ces identifiants"]\n' +
            '  H --> I["Valider login SSO Google"]\n' +
            '  I --> J["(Bonus) Bypass API pour apps mobiles (NZB360/LunaSea)"]'
        }
      ]
    },
    {
      id: 'creer-un-projet-google-cloud',
      title: 'Créer un projet Google Cloud',
      icon: 'rocket',
      body: [
        'Console (resource manager) : https://console.cloud.google.com/cloud-resource-manager',
        'Cliquez sur Créer un projet.',
        'Nom du projet : oauth, puis cliquez sur Créer.',
        'Dans la notification, cliquez sur “sélectionner un projet”.'
      ],
      images: [
        {
          src: 'https://user-images.githubusercontent.com/64525827/119948392-14839000-bf99-11eb-96a0-c7509bde74e9.png',
          alt: 'Créer un projet',
          caption: 'Étape de création du projet.'
        },
        {
          src: 'https://user-images.githubusercontent.com/64525827/119948566-3f6de400-bf99-11eb-8ddf-ce61d54a76b4.png',
          alt: 'Création projet',
          caption: 'Nommage du projet oauth.'
        },
        {
          src: 'https://user-images.githubusercontent.com/64525827/119949044-c28f3a00-bf99-11eb-8c9f-3342f6c0649e.png',
          alt: 'Notification sélectionner un projet',
          caption: 'Sélection du projet créé.'
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Le projet oauth est sélectionné en haut de la console Google Cloud.'
          ]
        }
      ]
    },
    {
      id: 'acceder-aux-identifiants',
      title: 'Accéder aux identifiants',
      icon: 'key',
      body: [
        'Après sélection du projet, cliquez sur Identifiants.',
        'Puis cliquez sur Créer des identifiants.',
        'Ensuite cliquez sur ID client OAuth.'
      ],
      images: [
        {
          src: 'https://user-images.githubusercontent.com/64525827/119950352-0a629100-bf9b-11eb-923c-fd49240cc6e0.png',
          alt: 'Identifiants',
          caption: 'Accès à la section des identifiants.'
        },
        {
          src: 'https://user-images.githubusercontent.com/64525827/119950515-33832180-bf9b-11eb-9e12-14995ab54f3c.png',
          alt: 'Créer des identifiants',
          caption: 'Création d’un ID client OAuth.'
        }
      ]
    },
    {
      id: 'configurer-lecran-dautorisation',
      title: 'Configurer l’écran d’autorisation',
      icon: 'settings',
      body: [
        'Cliquez sur Configurer l’écran d’autorisation.',
        'Choisissez Externe puis Créer.',
        'Renseignez le nom de l’application, l’email support et l’email développeur.',
        'À chaque étape, cliquez sur Enregistrer.'
      ],
      images: [
        {
          src: 'https://user-images.githubusercontent.com/64525827/119950915-af7d6980-bf9b-11eb-9d4a-f51a90294427.png',
          alt: 'Configurer écran',
          caption: 'Point d’entrée vers l’écran d’autorisation.'
        },
        {
          src: 'https://user-images.githubusercontent.com/64525827/119951092-dc318100-bf9b-11eb-8fb2-79b59052fecf.png',
          alt: 'Externe',
          caption: 'Choix du mode Externe.'
        },
        {
          src: 'https://user-images.githubusercontent.com/64525827/119951704-8a3d2b00-bf9c-11eb-9632-8c3698a45e5d.png',
          alt: 'Étapes enregistrer',
          caption: 'Validation des écrans successifs.'
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'L’écran d’autorisation est configuré et vous pouvez créer un client OAuth.'
          ]
        }
      ]
    },
    {
      id: 'creer-lid-client-oauth',
      title: 'Créer l’ID client OAuth (Application Web)',
      icon: 'shield',
      body: [
        'Retournez à Identifiants.',
        'Cliquez sur Créer des identifiants puis ID client OAuth.',
        'Choisissez le type Application web.',
        'Nom : identique au projet, par exemple oauth.',
        'URI de redirection : https://oauth.example.com/_oauth.'
      ],
      images: [
        {
          src: 'https://user-images.githubusercontent.com/64525827/119953309-2451a300-bf9e-11eb-9a85-fb8414e3c667.png',
          alt: 'OAuth Web redirect URI',
          caption: 'Configuration de l’URI de redirection.'
        },
        {
          src: 'https://user-images.githubusercontent.com/64525827/119952283-236c4180-bf9d-11eb-9937-86ca1d319f1c.png',
          alt: 'Identifiants OK',
          caption: 'Client ID et Secret générés.'
        },
        {
          src: 'https://user-images.githubusercontent.com/64525827/105181463-1ee5d700-5b2c-11eb-85b1-55a14668ea34.jpeg',
          alt: 'Client ID et secret',
          caption: 'Copie des identifiants dans un bloc-notes sécurisé.'
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Conservez ces identifiants',
          content: [
            'Vous en aurez besoin pour activer OAuth2 côté SSDV2 / Traefik et parfois Rclone selon le setup.'
          ]
        }
      ]
    },
    {
      id: 'retrouver-les-identifiants',
      title: 'Retrouver les identifiants si vous avez fermé la fenêtre',
      icon: 'settings',
      body: [
        'Ouvrez la console des identifiants sur https://console.developers.google.com.',
        'Cherchez la section Identifiants du projet oauth pour revoir le Client ID et le Client Secret.'
      ],
      images: [
        {
          src: 'https://user-images.githubusercontent.com/64525827/105181488-2907d580-5b2c-11eb-9b8b-cc39e3e2ed04.jpg',
          alt: 'Dashboard identifiants',
          caption: 'Retrouver les identifiants plus tard.'
        }
      ],
      accordions: [
        {
          title: 'J’ai fermé la fenêtre juste après la création',
          content: [
            'Ce n’est pas bloquant. Retourne dans la console développeurs Google, puis ouvre la section Identifiants du projet oauth.'
          ]
        },
        {
          title: 'Je ne vois pas le bon projet',
          content: [
            'Vérifie que tu es connecté avec le bon compte Google et que le projet oauth est bien sélectionné en haut de la console.'
          ]
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Astuce',
          content: [
            'Cherchez la section Identifiants du projet oauth pour revoir Client ID et Secret.'
          ]
        }
      ]
    },
    {
      id: 'bonus-oauth-apps-mobiles',
      title: 'Bonus — OAuth + apps mobiles',
      icon: 'wrench',
      body: [
        'Objectif : permettre l’accès web via OAuth et l’accès API via NZB360 ou LunaSea sans blocage.',
        'Principe : deux routers Traefik.',
        'Le bypass a une priorité haute et matche une API key header ou query pour appliquer no-auth.',
        'Le router auth a une priorité plus basse et applique OAuth pour tout le reste.'
      ],
      callouts: [
        {
          tone: 'warning',
          title: 'Sécurité',
          content: [
            'Le bypass doit être strict, exact et limité au nécessaire.',
            'Considérez une API key comme un secret au même niveau qu’un mot de passe.'
          ]
        }
      ],
      tabs: [
        {
          label: 'Principe',
          content: [
            'Le trafic web classique doit passer par OAuth.',
            'Le trafic mobile ou API doit passer par une route dédiée strictement conditionnée par une API key.'
          ]
        },
        {
          label: 'Architecture',
          content: [
            'Router bypass : priorité haute.',
            'Router auth : priorité plus basse.',
            'Les deux pointent vers le même service, mais pas avec les mêmes middlewares.'
          ]
        }
      ]
    },
    {
      id: 'exemple-sabnzbd',
      title: 'Exemple : Sabnzbd',
      icon: 'server',
      tabs: [
        {
          label: 'Avant',
          codeBlocks: [
            {
              title: 'Configuration avant bypass',
              language: 'yaml',
              code:
                "traefik.enable: 'true'\n" +
                '## HTTP Routers\n' +
                "traefik.http.routers.sabnzbd-rtr.entrypoints: 'https'\n" +
                "traefik.http.routers.sabnzbd-rtr.rule: 'Host(`sabnzbd.domain`)'\n" +
                "traefik.http.routers.sabnzbd-rtr.tls: 'true'\n" +
                '## Middlewares\n' +
                `traefik.http.routers.sabnzbd-rtr.middlewares: "{{ 'chain-oauth@file' if oauth_enabled | default(false) else 'chain-basic-auth@file' }}"\n` +
                '## HTTP Services\n' +
                "traefik.http.routers.sabnzbd-rtr.service: 'sabnzbd-svc'\n" +
                "traefik.http.services.sabnzbd-svc.loadbalancer.server.port: '8080'"
            }
          ]
        },
        {
          label: 'Après (bypass + oauth)',
          codeBlocks: [
            {
              title: 'Configuration avec bypass + OAuth',
              language: 'yaml',
              code:
                "traefik.enable: 'true'\n" +
                "traefik.http.routers.sabnzbd-rtr-bypass.entrypoints: 'https'\n" +
                "traefik.http.routers.sabnzbd-rtr-bypass.rule: 'Query(`apikey`, `api_de_sabnzbd`)'\n" +
                "traefik.http.routers.sabnzbd-rtr-bypass.priority: '100'\n" +
                "traefik.http.routers.sabnzbd-rtr-bypass.tls: 'true'\n" +
                '## HTTP Routers Auth\n' +
                "traefik.http.routers.sabnzbd-rtr.entrypoints: 'https'\n" +
                "traefik.http.routers.sabnzbd-rtr.rule: 'Host(`sabnzbd.domain`)'\n" +
                "traefik.http.routers.sabnzbd-rtr.priority: '99'\n" +
                "traefik.http.routers.sabnzbd-rtr.tls: 'true'\n" +
                '## Middlewares\n' +
                "traefik.http.routers.sabnzbd-rtr-bypass.middlewares: 'chain-no-auth@file'\n" +
                "traefik.http.routers.sabnzbd-rtr.middlewares: 'chain-oauth@file'\n" +
                '## HTTP Services\n' +
                "traefik.http.routers.sabnzbd-rtr.service: 'sabnzbd-svc'\n" +
                "traefik.http.routers.sabnzbd-rtr-bypass.service: 'sabnzbd-svc'\n" +
                "traefik.http.services.sabnzbd-svc.loadbalancer.server.port: '8080'"
            }
          ]
        }
      ],
      accordions: [
        {
          title: 'À faire absolument',
          content: [
            'Remplacez api_de_sabnzbd par votre vraie clé API Sabnzbd.',
            'Ensuite, réinitialisez l’application avec le script SSDV2 pour réappliquer la recette.'
          ]
        }
      ]
    },
    {
      id: 'sonarr-radarr-lidarr',
      title: 'Sonarr / Radarr / Lidarr',
      icon: 'server',
      tabs: [
        {
          label: 'Header',
          codeBlocks: [
            {
              title: 'Bypass via header',
              language: 'yaml',
              code:
                "traefik.http.routers.sonarr-rtr-bypass.rule: 'Headers(`X-Api-Key`, `api_sonarr`)'"
            }
          ]
        },
        {
          label: 'Header OU Query',
          codeBlocks: [
            {
              title: 'Règle combinée',
              language: 'yaml',
              code:
                "traefik.http.routers.sonarr-rtr-bypass.rule: 'Headers(`X-Api-Key`, `b12d1732186a4376b80bdb3875a0f39d`) || Query(`apikey`, `b12d1732186a4376b80bdb3875a0f39d`)'"
            }
          ]
        }
      ],
      callouts: [
        {
          tone: 'danger',
          title: 'Confidentialité',
          content: [
            'Une API key exposée = accès potentiellement total au service.',
            'Ne la publiez jamais dans un repo public, une capture ou des logs.',
            'Traitez-la comme un mot de passe.'
          ]
        }
      ]
    },
    {
      id: 'rutorrent',
      title: 'RuTorrent',
      icon: 'shield',
      codeBlocks: [
        {
          title: 'Bypass Path + double couche',
          language: 'yaml',
          code:
            "traefik.enable: 'true'\n" +
            "traefik.http.routers.rutorrent-rtr-bypass.entrypoints: 'https'\n" +
            "traefik.http.routers.rutorrent-rtr-bypass.rule: 'Path(`/RPC2`)'\n" +
            "traefik.http.routers.rutorrent-rtr-bypass.priority: '100'\n" +
            "traefik.http.routers.rutorrent-rtr-bypass.tls: 'true'\n" +
            '## HTTP Routers Auth\n' +
            "traefik.http.routers.rutorrent-rtr.entrypoints: 'https'\n" +
            "traefik.http.routers.rutorrent-rtr.rule: 'Host(`rutorrent.domain`)'\n" +
            "traefik.http.routers.rutorrent-rtr.priority: '99'\n" +
            "traefik.http.routers.rutorrent-rtr.tls: 'true'\n" +
            '## Middlewares\n' +
            "traefik.http.routers.rutorrent-rtr-bypass.middlewares: 'chain-basic-auth@file'\n" +
            "traefik.http.routers.rutorrent-rtr.middlewares: 'chain-oauth@file'\n" +
            '## HTTP Services\n' +
            "traefik.http.routers.rutorrent-rtr.service: 'rutorrent-svc'\n" +
            "traefik.http.routers.rutorrent-rtr-bypass.service: 'rutorrent-svc'\n" +
            "traefik.http.services.rutorrent-svc.loadbalancer.server.port: '8080'"
        }
      ],
      accordions: [
        {
          title: 'Pourquoi basic auth en bypass ?',
          content: [
            'On ajoute une couche basique pour limiter l’accès API-like tout en gardant OAuth pour le web.'
          ]
        }
      ]
    },
    {
      id: 'diagramme-sequence',
      title: 'Diagramme de séquence',
      icon: 'sync',
      diagrams: [
        {
          title: 'Web OAuth vs bypass API',
          code:
            'sequenceDiagram\n' +
            '  autonumber\n' +
            '  actor W as Utilisateur (Web)\n' +
            '  actor M as App mobile (NZB360/LunaSea)\n' +
            '  participant T as Traefik\n' +
            '  participant O as Google OAuth\n' +
            '  participant S as Service (Sonarr/Radarr/Sabnzbd)\n\n' +
            '  W->>T: Requête Web (sans clé API)\n' +
            '  T->>O: Déclenche OAuth (SSO)\n' +
            '  O-->>T: Token OK\n' +
            '  T-->>S: Accès autorisé (chain-oauth)\n' +
            '  S-->>W: Interface Web OK\n\n' +
            '  M->>T: Requête API (Header/Query apikey)\n' +
            '  T-->>S: Accès bypass (chain-no-auth / basic-auth)\n' +
            '  S-->>M: Réponse API OK'
        }
      ]
    }
  ],
  steps: [
    {
      title: 'Créer le projet Google Cloud oauth',
      text:
        'Crée un projet Google Cloud nommé oauth depuis la console resource manager puis sélectionne-le immédiatement pour travailler dans le bon contexte.',
      result: 'Le projet oauth doit être créé et sélectionné.',
      icon: 'rocket'
    },
    {
      title: 'Configurer l’écran d’autorisation en mode Externe',
      text:
        'Configure l’écran d’autorisation OAuth en choisissant Externe, puis renseigne le nom de l’application, l’email support et l’email développeur.',
      result: 'L’écran d’autorisation doit être prêt.',
      icon: 'settings'
    },
    {
      title: 'Créer un client OAuth de type Application Web',
      text:
        'Crée un client OAuth Web et définis précisément l’URI de redirection suivante : https://oauth.example.com/_oauth.',
      result: 'Le client OAuth Web doit être créé avec la bonne Redirect URI.',
      icon: 'shield'
    },
    {
      title: 'Copier le Client ID et le Client Secret',
      text:
        'Sauvegarde immédiatement le Client ID et le Client Secret dans un endroit sûr.',
      result: 'Les identifiants OAuth doivent être disponibles pour la suite.',
      icon: 'key'
    },
    {
      title: 'Configurer SSDV2 / Traefik',
      text:
        'Injecte le Client ID et le Client Secret dans ta configuration SSDV2 / Traefik afin d’activer Google OAuth2 côté reverse proxy.',
      result: 'Traefik doit être prêt à déclencher Google OAuth.',
      icon: 'shield'
    },
    {
      title: 'Valider le SSO',
      text:
        'Teste l’accès à un service protégé afin de confirmer que le flux web passe bien par Google OAuth avec SSO.',
      result: 'La connexion SSO doit fonctionner avec les comptes autorisés.',
      icon: 'sparkles'
    },
    {
      title: 'Ajouter le bypass API si nécessaire',
      text:
        'Si tu utilises NZB360, LunaSea ou d’autres clients mobiles, ajoute un router bypass strict avec priorité haute et garde un router OAuth avec priorité plus basse pour le web.',
      result:
        'Le web doit passer par OAuth et les apps mobiles doivent continuer à fonctionner.',
      icon: 'wrench'
    }
  ],
  troubleshooting: [
    'Si tu as plusieurs comptes Google, utilise une fenêtre privée.',
    'Si le login OAuth échoue, vérifie d’abord l’URI de redirection exacte.',
    'Si tu ne retrouves plus les identifiants, retourne dans la section Identifiants du projet oauth.',
    'Si le web fonctionne mais pas l’app mobile, vérifie la priorité des routers et la clé API exacte.',
    'Après modification d’une recette SSDV2, réinitialise l’application pour réappliquer la configuration.',
    'Ne publie jamais une API key en clair.'
  ],
  checklist: [
    { text: 'Projet Google Cloud oauth créé et sélectionné' },
    { text: 'Écran d’autorisation configuré en Externe' },
    { text: 'Client OAuth Web créé' },
    { text: 'Redirect URI correcte : https://oauth.example.com/_oauth' },
    { text: 'Client ID et Client Secret copiés et stockés' },
    { text: 'OAuth activé côté SSDV2 / Traefik' },
    { text: 'Connexion SSO OK avec compte autorisé' },
    { text: 'Bonus bypass API strict appliqué si nécessaire' }
  ],
  finalChecklist: [
    'Le web passe par OAuth avec SSO Google',
    'Les comptes autorisés peuvent se connecter proprement',
    'Les apps mobiles continuent de fonctionner via un bypass strict si nécessaire'
  ]
};