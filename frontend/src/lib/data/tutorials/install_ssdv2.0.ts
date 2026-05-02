import type { Tutorial } from './types';

export const prerequisNomDomaineCloudflareSsdv2: Tutorial = {
  slug: 'prerequis-nom-domaine-cloudflare-ssdv2',
  title: 'Nom de domaine & Cloudflare (SSDV2)',
  description:
    'Prérequis essentiels pour suivre le guide SSDV2 : choix d’un nom de domaine compatible, ajout dans Cloudflare, bascule des nameservers, récupération de la Global API Key et configuration SSL/TLS en mode Full.',
  summary:
    'Cette page couvre les prérequis DNS et sécurité nécessaires avant d’utiliser SSDV2. Elle explique comment choisir un registrar fiable, pourquoi Cloudflare est recommandé, comment ajouter un domaine dans Cloudflare, remplacer les nameservers chez le registrar, attendre la propagation DNS, récupérer la Global API Key et régler SSL/TLS en mode Full pour une base stable et compatible avec l’automatisation SSDV2.',
  level: 'débutant',
  duration: '15 à 30 min',
  estimatedTime:
    'Environ 15 à 30 minutes pour ajouter le domaine dans Cloudflare, modifier les nameservers, récupérer la Global API Key et vérifier la configuration SSL/TLS, hors délai éventuel de propagation DNS.',
  category: 'Installation',
  group: 'Installation SSDv2',
  icon: 'globe',
  tags: [
    'ssdv2',
    'prerequis',
    'domaine',
    'cloudflare',
    'dns',
    'ssl',
    'tls',
    'registrar',
    'nameservers',
    'api'
  ],
  prerequisites: [
    'Un nom de domaine acheté chez un registrar fiable',
    'Un accès à la console d’administration du registrar',
    'Un compte Cloudflare ou la possibilité d’en créer un',
    'L’intention d’utiliser SSDV2 avec sous-domaines et automatisation DNS',
    'Un accès au dashboard Cloudflare pour gérer DNS et SSL/TLS'
  ],
  access: [
    {
      label: 'Cloudflare Sign Up',
      url: 'https://dash.cloudflare.com/sign-up'
    },
    {
      label: 'Cloudflare Dashboard',
      url: 'https://dash.cloudflare.com/'
    }
  ],
  links: [
    {
      label: 'Cloudflare Sign Up',
      url: 'https://dash.cloudflare.com/sign-up'
    },
    {
      label: 'Cloudflare Dashboard',
      url: 'https://dash.cloudflare.com/'
    }
  ],
  callouts: [
    {
      tone: 'abstract',
      title: 'Abstract',
      content: [
        'Pour suivre le guide SSDV2, vous avez besoin d’un nom de domaine et, de préférence, d’une configuration Cloudflare pour gérer DNS et sécurité.',
        'Cette page explique comment choisir un registrar compatible, pourquoi Cloudflare est utile, comment ajouter votre domaine, changer les nameservers, récupérer la Global API Key, puis régler SSL/TLS en mode Full.'
      ]
    },
    {
      tone: 'tip',
      title: 'Raccourci mental',
      content: [
        'Domaine = URL propres via sous-domaines.',
        'Cloudflare = DNS + sécurité edge.',
        'API key = automatisation SSDV2.'
      ]
    }
  ],
  warnings: [
    'Certains fournisseurs de domaines gratuits sont incompatibles ou instables avec Cloudflare.',
    'Ne publiez jamais votre Global API Key dans un dépôt, un paste, une capture ou des logs.',
    'La propagation DNS après changement de nameservers peut prendre jusqu’à 24 heures.',
    'Sans contrôle correct des nameservers, SSDV2 ne pourra pas automatiser proprement les entrées DNS.',
    'Un mode SSL/TLS mal configuré peut entraîner des erreurs d’accès ou une chaîne TLS incohérente.'
  ],
  sections: [
    {
      id: 'tldr',
      title: 'l’essentiel en quelques points',
      icon: 'rocket',
      items: [
        'Acheter un domaine fiable chez un registrar classique',
        'Ajouter le domaine dans Cloudflare avec l’offre gratuite',
        'Remplacer les nameservers chez le registrar par ceux de Cloudflare',
        'Attendre la propagation DNS',
        'Récupérer la Global API Key',
        'Configurer SSL/TLS en mode Full'
      ]
    },
    {
      id: 'objectif',
      title: 'Objectif',
      icon: 'target',
      items: [
        'Disposer d’un nom de domaine pour accéder aux applications via sous-domaines',
        'Centraliser et automatiser la gestion DNS idéalement via Cloudflare',
        'Activer un chiffrement SSL/TLS cohérent pour Traefik et les services'
      ]
    },
    {
      id: 'workflow-global',
      title: 'Vue d’ensemble (workflow)',
      icon: 'sync',
      diagrams: [
        {
          title: 'Workflow domaine + Cloudflare',
          code:
            'flowchart TD\n' +
            '  A["Acheter un nom de domaine"] --> B["Créer/ouvrir un compte Cloudflare"]\n' +
            '  B --> C["Ajouter le domaine à Cloudflare"]\n' +
            '  C --> D["Choisir l\\\'offre gratuite"]\n' +
            '  D --> E["Récupérer les nameservers (NS) Cloudflare"]\n' +
            '  E --> F["Modifier les NS chez le registrar"]\n' +
            '  F --> G["Attendre propagation DNS (jusqu\\\'à 24h)"]\n' +
            '  G --> H["Récupérer la Global API Key"]\n' +
            '  H --> I["Configurer SSL/TLS : Full"]\n' +
            '  I --> J["Prêt pour le script SSDV2 ✅"]'
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Vue simple',
          content: [
            'Le domaine donne l’adresse publique.',
            'Cloudflare devient la couche DNS et sécurité.',
            'La Global API Key sert à l’automatisation.',
            'Le mode Full aligne la partie TLS avec le reste du setup.'
          ]
        }
      ]
    },
    {
      id: 'nom-de-domaine',
      title: 'Nom de domaine',
      icon: 'globe',
      body: [
        'L’accès à vos applications nécessite un nom de domaine afin d’utiliser des sous-domaines propres pour chaque service.',
        'Le script SSDV2 facilite ensuite l’ajout et la personnalisation des sous-domaines pour vos applications.'
      ],
      items: [
        'Exemple : https://rutorrent.mondomaine.com'
      ],
      callouts: [
        {
          tone: 'warning',
          title: 'Compatibilité Cloudflare',
          content: [
            'Certains fournisseurs de domaines gratuits, comme Freenom, sont souvent incompatibles ou instables avec Cloudflare.',
            'Pour un setup fiable, privilégiez un registrar classique.'
          ]
        },
        {
          tone: 'tip',
          title: 'Critère premium',
          content: [
            'Choisissez un registrar qui permet de modifier facilement les nameservers, de garder un contrôle DNS propre et d’éviter les limitations des offres gratuites.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Pourquoi un domaine est-il indispensable ?',
          content: [
            'Parce qu’il structure tout le setup public : accès aux applications, sous-domaines, reverse proxy, certificats et ergonomie générale. Sans domaine, l’ensemble est plus fragile, moins lisible et souvent moins automatisable.'
          ]
        }
      ],
      tabs: [
        {
          label: 'Exemples de registrars',
          content: [
            'Gandi',
            'LWS',
            'OVH',
            'Ionos',
            'InternetBS',
            'Et bien d’autres'
          ]
        },
        {
          label: 'À éviter',
          content: [
            'Les solutions gratuites ou très limitées qui compliquent la gestion des nameservers et introduisent de l’instabilité.'
          ]
        }
      ]
    },
    {
      id: 'pourquoi-cloudflare',
      title: 'Configurer Cloudflare',
      icon: 'shield',
      body: [
        'Cloudflare n’est pas seulement un CDN. Dans ce contexte, il sert de couche DNS et sécurité très pratique pour SSDV2.',
        'Il peut améliorer la sécurité, la fiabilité et la cohérence globale du setup.'
      ],
      items: [
        'Sécurité : TLS, règles, protection edge',
        'Performance : optimisation, compression, cache ciblé',
        'Fiabilité : protection DDoS, routage et centralisation DNS'
      ],
      accordions: [
        {
          title: 'Pourquoi Cloudflare est recommandé avec SSDV2 ?',
          content: [
            'Parce qu’il simplifie énormément la gestion DNS, l’automatisation et la couche d’exposition publique. Cela donne un socle plus stable pour Traefik et les sous-domaines applicatifs.'
          ]
        }
      ]
    },
    {
      id: 'creer-compte-et-ajouter-domaine',
      title: 'Créer ou se connecter à un compte Cloudflare',
      icon: 'rocket',
      body: [
        'Commencez par ouvrir un compte Cloudflare ou vous connecter à un compte existant.',
        'Ajoutez ensuite votre domaine racine dans le dashboard, par exemple mondomaine.com.'
      ],
      tabs: [
        {
          label: 'Création du compte',
          content: [
            'Rendez-vous sur https://dash.cloudflare.com/sign-up.',
            'Créez un compte avec email et mot de passe.',
            'Une fois connecté, cliquez sur Ajouter un site.'
          ]
        },
        {
          label: 'Ajout du domaine',
          content: [
            'Entrez le domaine racine, par exemple mondomaine.com.',
            'Cloudflare tente d’importer les enregistrements DNS existants.',
            'Choisissez l’offre gratuite puis confirmez.'
          ]
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Le domaine apparaît dans le dashboard Cloudflare et vous pouvez accéder à sa zone DNS.'
          ]
        }
      ]
    },
    {
      id: 'changer-nameservers',
      title: 'Changer les Nameservers (NS) vers Cloudflare',
      icon: 'server',
      body: [
        'Une fois le domaine ajouté, Cloudflare vous fournit généralement deux nameservers.',
        'Vous devez alors remplacer les nameservers actuels chez votre registrar par ceux fournis par Cloudflare.'
      ],
      items: [
        'Récupérer les nameservers Cloudflare',
        'Ouvrir la console d’administration du registrar',
        'Remplacer les NS actuels par ceux de Cloudflare',
        'Appliquer les changements'
      ],
      callouts: [
        {
          tone: 'tip',
          title: 'Validation rapide',
          content: [
            'Quand la délégation DNS est correctement propagée, Cloudflare indique généralement que le domaine est actif.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Combien de temps faut-il attendre ?',
          content: [
            'La propagation peut prendre jusqu’à 24 heures, même si elle est souvent plus rapide. Tant que la délégation n’est pas complètement vue partout, certaines vérifications peuvent rester en attente.'
          ]
        }
      ]
    },
    {
      id: 'global-api-key',
      title: 'Récupération de la Global API Key Cloudflare',
      icon: 'key',
      body: [
        'Une fois le domaine actif, récupérez la Global API Key dans le dashboard Cloudflare.',
        'Cette clé pourra être utilisée par SSDV2 pour automatiser certaines opérations.'
      ],
      items: [
        'Cliquez sur Aperçu',
        'Cliquez sur Obtenir votre jeton d’API',
        'À côté de Global API Key, cliquez sur Afficher',
        'Conservez la clé dans un endroit sûr'
      ],
      callouts: [
        {
          tone: 'danger',
          title: 'Secret',
          content: [
            'La Global API Key donne un pouvoir élevé sur votre compte.',
            'Ne la publiez jamais dans un repo, un paste, une capture ou des logs.',
            'Évitez aussi de la laisser dans un historique partagé.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Pourquoi cette clé est sensible ?',
          content: [
            'Parce qu’elle permet d’agir à un niveau élevé sur votre compte Cloudflare. Elle doit être traitée comme un secret critique, au même titre qu’un mot de passe très sensible.'
          ]
        }
      ]
    },
    {
      id: 'ssl-tls-full',
      title: 'Configuration SSL/TLS (mode Full)',
      icon: 'shield',
      body: [
        'Dans Cloudflare, réglez SSL/TLS sur Full.',
        'Cela permet à Cloudflare de chiffrer également la liaison entre Cloudflare et votre serveur.'
      ],
      items: [
        'Mode à sélectionner : Full'
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Pourquoi Full ?',
          content: [
            'Cloudflare chiffre aussi la liaison Cloudflare → serveur.',
            'Cela améliore la sécurité, limite certaines erreurs TLS et reste cohérent avec une exposition via Traefik.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Que risque-t-on avec un mauvais mode SSL/TLS ?',
          content: [
            'Un mauvais réglage peut provoquer des erreurs d’accès, des incohérences de chiffrement ou une chaîne TLS difficile à diagnostiquer. Full reste le réglage cohérent dans ce contexte.'
          ]
        }
      ]
    },
    {
      id: 'checklist-prete',
      title: 'Checklist prêt à suivre le guide',
      icon: 'check-circle',
      items: [
        'J’ai un domaine chez un registrar fiable',
        'Mon domaine est ajouté dans Cloudflare',
        'Mes nameservers pointent vers Cloudflare',
        'La propagation DNS est terminée',
        'J’ai récupéré la Global API Key',
        'SSL/TLS Cloudflare est réglé sur Full'
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Vous êtes prêt à lancer SSDV2 avec une base DNS et SSL stable, propre et compatible avec l’automatisation.'
          ]
        }
      ]
    },
    {
      id: 'diagramme-sequence',
      title: 'Diagramme de séquence (mise en place DNS)',
      icon: 'sync',
      diagrams: [
        {
          title: 'Mise en place du domaine dans Cloudflare',
          code:
            'sequenceDiagram\n' +
            '  autonumber\n' +
            '  actor U as Utilisateur\n' +
            '  participant R as Registrar (OVH/Gandi/...)\n' +
            '  participant CF as Cloudflare\n' +
            '  participant DNS as DNS (Propagation)\n\n' +
            '  U->>CF: Crée compte + ajoute domaine\n' +
            '  CF-->>U: Fournit nameservers (NS)\n' +
            '  U->>R: Remplace NS par ceux de Cloudflare\n' +
            '  R-->>DNS: Délégation DNS (propagation)\n' +
            '  DNS-->>CF: Domaine actif / vérifié\n' +
            '  U->>CF: Récupère Global API Key\n' +
            '  U->>CF: Configure SSL/TLS = Full\n' +
            '  CF-->>U: Prêt pour SSDV2 ✅'
        }
      ]
    }
  ],
  steps: [
    {
      title: 'Choisir un domaine fiable',
      text:
        'Achetez un nom de domaine chez un registrar classique qui vous laisse modifier facilement les nameservers et gérer votre zone DNS proprement.',
      result:
        'Vous devez disposer d’un domaine exploitable pour créer des sous-domaines applicatifs.',
      icon: 'globe'
    },
    {
      title: 'Ajouter le domaine dans Cloudflare',
      text:
        'Créez un compte Cloudflare ou connectez-vous, puis ajoutez votre domaine racine dans le dashboard en choisissant l’offre gratuite.',
      result:
        'Le domaine doit apparaître dans Cloudflare avec une zone prête à être activée.',
      icon: 'rocket'
    },
    {
      title: 'Basculer les nameservers',
      text:
        'Récupérez les nameservers fournis par Cloudflare et remplacez ceux du registrar par ces nouveaux NS.',
      result:
        'La délégation DNS doit désormais pointer vers Cloudflare.',
      icon: 'server'
    },
    {
      title: 'Attendre la propagation',
      text:
        'Patientez jusqu’à ce que Cloudflare détecte le domaine comme actif après propagation DNS.',
      result:
        'Le domaine doit être validé et actif dans Cloudflare.',
      icon: 'sync'
    },
    {
      title: 'Récupérer la Global API Key',
      text:
        'Ouvrez les réglages d’API dans Cloudflare et récupérez la Global API Key, puis stockez-la dans un endroit sûr.',
      result:
        'La clé d’automatisation doit être disponible pour SSDV2.',
      icon: 'key'
    },
    {
      title: 'Configurer SSL/TLS en Full',
      text:
        'Réglez la partie SSL/TLS sur le mode Full afin de garder une chaîne de chiffrement cohérente entre Cloudflare et le serveur.',
      result:
        'La base DNS et TLS doit être prête pour la suite du guide.',
      icon: 'shield'
    }
  ],
  troubleshooting: [
    'Si Cloudflare n’active pas le domaine, vérifiez que les nameservers ont bien été remplacés chez le registrar.',
    'Si la propagation semble longue, attendez davantage : cela peut prendre jusqu’à 24 heures.',
    'Si vous utilisez un registrar exotique ou gratuit, des incompatibilités peuvent bloquer ou compliquer l’intégration.',
    'Si vous ne retrouvez pas la Global API Key, repassez par les réglages API du dashboard Cloudflare.',
    'Si votre setup TLS pose problème ensuite, revérifiez que le mode SSL/TLS est bien réglé sur Full.',
    'Si vous ne contrôlez pas les nameservers du domaine, vous ne pourrez pas terminer proprement cette étape.'
  ],
  checklist: [
    { text: 'Nom de domaine acheté chez un registrar fiable' },
    { text: 'Domaine ajouté dans Cloudflare' },
    { text: 'Nameservers Cloudflare appliqués chez le registrar' },
    { text: 'Propagation DNS terminée' },
    { text: 'Global API Key récupérée et stockée en sécurité' },
    { text: 'SSL/TLS réglé sur Full' }
  ],
  finalChecklist: [
    'Le domaine est piloté par Cloudflare',
    'La couche DNS est prête pour les sous-domaines SSDV2',
    'La Global API Key est disponible pour l’automatisation',
    'La configuration SSL/TLS est cohérente pour la suite'
  ]
};