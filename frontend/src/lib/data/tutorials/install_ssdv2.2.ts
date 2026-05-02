import type { Tutorial } from './types';

export const lancementScriptConfigurationSsdv2: Tutorial = {
  slug: 'lancement-script-configuration-ssdv2',
  title: 'Lancement du script et configuration — SSDV2',
  description:
    'Guide pour exécuter seedbox.sh, choisir la langue, définir les répertoires, gérer le groupe docker, configurer l’authentification et Cloudflare, installer les composants de base et créer les dossiers médias.',
  summary:
    'Cette page couvre le premier lancement du script SSDV2 et les principaux choix de configuration initiaux. Elle détaille le choix de la langue, la définition des chemins, l’ajout éventuel de l’utilisateur au groupe docker avec reconnexion obligatoire, la configuration de l’authentification et de Cloudflare, l’installation des composants de base comme Traefik, puis la création des dossiers médias pour terminer sur une base propre et fonctionnelle.',
  level: 'débutant',
  duration: '15 à 35 min',
  estimatedTime:
    'Environ 15 à 35 minutes selon la vitesse du serveur, la phase d’installation des dépendances et le nombre de choix de configuration à renseigner.',
  category: 'Installation',
  group: 'Installation SSDv2',
  icon: 'rocket',
  tags: [
    'ssdv2',
    'installation',
    'seedbox',
    'docker',
    'cloudflare',
    'traefik',
    'script',
    'auth',
    'medias'
  ],
  prerequisites: [
    'Le dépôt SSDV2 doit déjà être cloné sur le serveur',
    'Vous devez être connecté avec un utilisateur non-root',
    'Git et les prérequis système doivent être installés',
    'Le domaine doit être prêt si vous utilisez Cloudflare',
    'La Global API Key Cloudflare doit être disponible si vous activez le DNS Cloudflare',
    'L’accès SSH doit être stable car plusieurs reconnexions peuvent être nécessaires'
  ],
  access: [],
  links: [],
  callouts: [
    {
      tone: 'abstract',
      title: 'Abstract',
      content: [
        'Cette section couvre le premier lancement du script SSDV2 seedbox.sh et les choix de configuration initiaux : langue, chemins de stockage, ajout éventuel de l’utilisateur au groupe docker, configuration de l’authentification, intégration Cloudflare, installation des composants de base et création des dossiers médias.',
        'L’objectif est d’aboutir à un environnement prêt pour la suite, avec Docker fonctionnel, Traefik configuré et une structure de dossiers média cohérente.'
      ]
    },
    {
      tone: 'tip',
      title: 'Principe',
      content: [
        'Dès qu’on touche aux permissions ou au groupe docker, on applique : changer → reconnecter → relancer.',
        'Cette discipline évite une grande partie des erreurs liées au groupe docker.'
      ]
    }
  ],
  warnings: [
    'Lisez attentivement tous les messages du script, en particulier ceux liés aux permissions et au groupe docker.',
    'Après un ajout au groupe docker, une déconnexion puis reconnexion est obligatoire.',
    'Si vous continuez sans reconnecter, Docker peut être inaccessible ou se comporter de manière incohérente.',
    'Une erreur de saisie sur le domaine, les identifiants Cloudflare ou les paramètres d’authentification peut compliquer les étapes suivantes.',
    'Ne copiez jamais vos secrets n’importe où : mot de passe et API key doivent rester confidentiels.'
  ],
  sections: [
    {
      id: 'tldr',
      title: 'l’essentiel en quelques points',
      icon: 'rocket',
      items: [
        'Lancer ./seedbox.sh puis choisir la langue',
        'Définir le répertoire seedbox',
        'Si ajout au groupe docker : se reconnecter puis relancer le script',
        'Renseigner mot de passe, mail et domaine',
        'Activer Cloudflare si souhaité avec email et API key',
        'Configurer Traefik en auth basique pour commencer',
        'Créer les dossiers médias puis effectuer la reconnexion finale'
      ]
    },
    {
      id: 'attention-instructions',
      title: 'Soyez attentif aux instructions',
      icon: 'shield',
      body: [
        'Le script vous guide à travers plusieurs étapes : choix de la langue, configuration des dossiers, gestion des permissions et installation des composants.',
        'Des messages d’alerte peuvent apparaître au sujet de la restauration, des permissions ou du groupe docker.',
        'Il est important de les lire attentivement et d’appliquer exactement les actions demandées.'
      ],
      callouts: [
        {
          tone: 'warning',
          title: 'Point critique : groupe Docker',
          content: [
            'Quand votre utilisateur est ajouté au groupe docker, une déconnexion puis reconnexion est nécessaire.',
            'Si vous continuez sans reconnecter, vous risquez des erreurs Docker ou un comportement incohérent.'
          ]
        }
      ]
    },
    {
      id: 'workflow-global',
      title: 'Vue d’ensemble (workflow)',
      icon: 'sync',
      diagrams: [
        {
          title: 'Workflow du premier lancement',
          code:
            'flowchart TD\n' +
            '  A["Lancer ./seedbox.sh"] --> B["Choisir la langue"]\n' +
            '  B --> C["Message restauration (info)"]\n' +
            '  C --> D["Configurer répertoire seedbox"]\n' +
            '  D --> E{"Utilisateur dans groupe docker ?"}\n' +
            '  E -->|Non| F["Ajout au groupe docker + reconnexion"]\n' +
            '  F --> G["Déconnexion / reconnexion SSH"]\n' +
            '  G --> H["Relancer ./seedbox.sh"]\n' +
            '  E -->|Oui| H\n' +
            '  H --> I["Configurer auth basique"]\n' +
            '  I --> J{"DNS Cloudflare ?"}\n' +
            '  J -->|Oui| K["Entrer mail + API key Cloudflare"]\n' +
            '  J -->|Non| L["Gestion DNS manuelle"]\n' +
            '  K --> M["Installation composants"]\n' +
            '  L --> M\n' +
            '  M --> N["Traefik : sous-domaine ?"]\n' +
            '  N --> O["Traefik auth : basique"]\n' +
            '  O --> P["Créer dossiers Medias"]\n' +
            '  P --> Q["Reconnexion finale"]\n' +
            '  Q --> R["Accueil script OK ✅"]'
        }
      ]
    },
    {
      id: 'lancement-script',
      title: 'Lancement du script',
      icon: 'server',
      body: [
        'Placez-vous dans le répertoire du dépôt SSDV2 puis exécutez le script principal.',
        'C’est le point d’entrée du setup interactif.'
      ],
      codeBlocks: [
        {
          title: 'Lancer seedbox.sh',
          language: 'bash',
          code: 'cd /home/${USER}/seedbox-compose && ./seedbox.sh'
        }
      ]
    },
    {
      id: 'choix-langue',
      title: 'Choix de la langue',
      icon: 'settings',
      body: [
        'Le script vous propose une interface multilingue dès le démarrage.',
        'Choisissez la langue qui vous permettra de suivre le setup plus confortablement.'
      ],
      codeBlocks: [
        {
          title: 'Sélection de langue',
          language: 'bash',
          code: '1. Anglais/English\n2. Français/French'
        }
      ],
      callouts: [
        {
          tone: 'tip',
          title: 'Choix recommandé',
          content: [
            'Choisissez 2 pour Français si vous souhaitez suivre le guide dans le même vocabulaire que la documentation.'
          ]
        }
      ]
    },
    {
      id: 'message-restauration',
      title: 'Message relatif à une éventuelle restauration',
      icon: 'info',
      body: [
        'Le script peut afficher un message indiquant que la restauration ne fonctionne que si l’installation est réalisée depuis le même répertoire et vers la même destination.',
        'Il s’agit d’une information utile si vous restaurez une sauvegarde existante.'
      ],
      codeBlocks: [
        {
          title: 'Message affiché',
          language: 'bash',
          code:
            "Actuellement, la restauration ne fonctionne que si le script a été installé depuis le même répertoire que celui qui a servi à faire la sauvegarde, et a été installé sur la même destination."
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Pourquoi ce message ?',
          content: [
            'La restauration dépend du chemin d’installation et de la destination utilisée pour la sauvegarde.',
            'Même répertoire et même cible sont requis pour un comportement cohérent.'
          ]
        }
      ]
    },
    {
      id: 'configuration-repertoires',
      title: 'Configuration des répertoires',
      icon: 'folder-lock',
      body: [
        'Le script vous demande le répertoire de stockage des réglages et données liées à la seedbox.',
        'Dans la plupart des cas, le chemin dans le home de l’utilisateur est le bon choix.'
      ],
      codeBlocks: [
        {
          title: 'Répertoire seedbox',
          language: 'bash',
          code: '/home/VOTRE_USER/seedbox'
        }
      ],
      callouts: [
        {
          tone: 'tip',
          title: 'Rappel',
          content: [
            'Remplacez VOTRE_USER par votre utilisateur Linux non-root créé précédemment.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Pourquoi ce chemin est-il recommandé ?',
          content: [
            'Parce qu’il garde la structure du setup dans le home de l’utilisateur courant, avec une logique simple à comprendre et à maintenir.'
          ]
        }
      ]
    },
    {
      id: 'groupe-docker',
      title: 'Ajout de votre utilisateur au groupe Docker',
      icon: 'shield',
      body: [
        'Si votre utilisateur n’est pas déjà dans le groupe docker, le script peut l’y ajouter automatiquement.',
        'Dans ce cas, la session en cours ne prend pas immédiatement en compte le nouveau groupe.'
      ],
      codeBlocks: [
        {
          title: 'Message typique',
          language: 'bash',
          code:
            'IMPORTANT !\n===================================================\nVotre utilisateur n’était pas dans le groupe docker\nIl a été ajouté, mais vous devez vous déconnecter/reconnecter pour que la suite du process puisse fonctionner'
        }
      ],
      callouts: [
        {
          tone: 'danger',
          title: 'Risque Docker KO',
          content: [
            'Si vous ne reconnectez pas votre session, Docker peut refuser certaines actions ou se comporter de façon incohérente.'
          ]
        }
      ],
      tabs: [
        {
          label: 'Ce qu’il faut faire',
          content: [
            'Fermez votre session SSH.',
            'Reconnectez-vous avec votre utilisateur non-root.',
            'Relancez ensuite ./seedbox.sh.'
          ]
        },
        {
          label: 'À ne pas faire',
          content: [
            'Continuer dans la même session en espérant que le groupe docker sera pris en compte immédiatement.'
          ]
        }
      ]
    },
    {
      id: 'relancer-apres-reconnexion',
      title: 'Relancer le script après reconnexion',
      icon: 'refresh-cw',
      body: [
        'Une fois reconnecté, relancez le script pour poursuivre l’installation dans une session propre.',
        'Le script reprend alors la suite des composants à installer ou configurer.'
      ],
      codeBlocks: [
        {
          title: 'Relancer seedbox.sh',
          language: 'bash',
          code: 'cd /home/${USER}/seedbox-compose && ./seedbox.sh'
        },
        {
          title: 'Message de poursuite',
          language: 'bash',
          code:
            'Certains composants doivent encore être installés/réglés\nCette opération va prendre plusieurs minutes selon votre système'
        }
      ]
    },
    {
      id: 'authentification-basique',
      title: 'Configuration de l’authentification basique',
      icon: 'key',
      body: [
        'Le script vous demande ensuite de renseigner les informations de base pour l’authentification.',
        'Pour un premier setup, l’authentification basique est la voie la plus simple.'
      ],
      codeBlocks: [
        {
          title: 'Prompts typiques',
          language: 'bash',
          code:
            '↘️ Mot de passe | Appuyer sur [Enter] :\n↘️ Mail | Appuyer sur [Enter] :\n↘️ Domaine | Appuyer sur [Enter] :'
        }
      ],
      callouts: [
        {
          tone: 'tip',
          title: 'Format attendu',
          content: [
            'Le domaine doit être saisi sans https://, par exemple domaine.fr.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Pourquoi commencer en auth basique ?',
          content: [
            'Parce que cela simplifie le démarrage et réduit les variables. Vous pourrez toujours migrer plus tard vers OAuth ou Authelia.'
          ]
        }
      ]
    },
    {
      id: 'cloudflare',
      title: 'Gestion des DNS avec Cloudflare',
      icon: 'globe',
      body: [
        'Si vous utilisez Cloudflare, le script peut automatiser une partie de la gestion DNS.',
        'Cela réduit les manipulations manuelles et limite les erreurs de configuration.'
      ],
      codeBlocks: [
        {
          title: 'Question Cloudflare',
          language: 'bash',
          code: 'Souhaitez vous utiliser les DNS Cloudflare ? (y/n)'
        }
      ],
      callouts: [
        {
          tone: 'tip',
          title: 'Pourquoi Cloudflare ?',
          content: [
            'Le script peut automatiser la gestion DNS, ce qui accélère l’installation et réduit fortement les erreurs.'
          ]
        }
      ],
      tabs: [
        {
          label: 'Réponse recommandée',
          content: [
            'Répondez y si votre domaine est bien géré par Cloudflare.',
            'Renseignez ensuite votre email Cloudflare et votre API key.'
          ]
        },
        {
          label: 'DNS manuel',
          content: [
            'Si vous ne passez pas par Cloudflare, vous devrez gérer les entrées DNS manuellement.'
          ]
        }
      ]
    },
    {
      id: 'installation-composants',
      title: 'Installation des composants',
      icon: 'wrench',
      body: [
        'Le script lance ensuite une phase d’installation plus longue, généralement via des tâches automatisées.',
        'Pendant cette étape, certaines tâches peuvent sembler figées quelques instants.'
      ],
      codeBlocks: [
        {
          title: 'Exemple de progression',
          language: 'bash',
          code:
            'TASK [Add Debian repositories] ***************************************************************\nTASK [Install common packages] ***************************************************************'
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Comportement attendu',
          content: [
            'La durée dépend de la puissance du serveur.',
            'Une phase silencieuse peut être normale : ne stoppez pas le script prématurément.'
          ]
        }
      ]
    },
    {
      id: 'traefik',
      title: 'Traefik — sous-domaine et authentification',
      icon: 'shield',
      body: [
        'Le script vous propose ensuite de personnaliser ou non le sous-domaine Traefik, puis de choisir le mode d’authentification.',
        'Pour un démarrage simple et conforme au guide, gardez la configuration basique.'
      ],
      codeBlocks: [
        {
          title: 'Sous-domaine Traefik',
          language: 'bash',
          code:
            'Adresse par défault: https://traefik.cinecast.tv\n\nSouhaitez-vous personnaliser le sous-domaine ? (y/n)'
        },
        {
          title: 'Authentification Traefik',
          language: 'bash',
          code:
            "Choix de l'authentification pour Traefik [ Entrée ] : 1 => basique | 2 => oauth | 3 => authelia"
        }
      ],
      tabs: [
        {
          label: 'Choix recommandé',
          content: [
            'Répondez n pour ne pas personnaliser le sous-domaine au départ.',
            'Choisissez 1 pour l’authentification basique.'
          ]
        },
        {
          label: 'Évolution plus tard',
          content: [
            'Vous pourrez migrer ensuite vers OAuth Google ou Authelia lorsque le socle sera validé.'
          ]
        }
      ]
    },
    {
      id: 'dossiers-medias',
      title: 'Création des dossiers médias',
      icon: 'folder-lock',
      body: [
        'Le script vous permet ensuite de créer les dossiers qui structureront vos bibliothèques médias.',
        'Vous pouvez rester sur une structure simple ou préparer des bibliothèques séparées 4K.'
      ],
      codeBlocks: [
        {
          title: 'Prompt de création',
          language: 'bash',
          code:
            'Noms de dossiers à créer dans Medias (ex : Films, Series, Films d’animation, etc.) | Appuyez sur [Entrée] | Tapez "stop" une fois terminé.'
        }
      ],
      tabs: [
        {
          label: 'Configuration classique',
          content: [
            'Films',
            'Series',
            'stop'
          ]
        },
        {
          label: 'Configuration 4K',
          content: [
            'Films',
            'Series',
            'Films4K',
            'Series4K',
            'stop'
          ]
        }
      ],
      images: [
        {
          src: 'https://i.imgur.com/CNsarEa.png',
          alt: 'Création des dossiers médias',
          caption: 'Exemple de saisie lors de la création des dossiers Medias.'
        }
      ],
      accordions: [
        {
          title: 'Pourquoi préparer les dossiers dès maintenant ?',
          content: [
            'Parce que cette structure sera réutilisée ensuite par les applications médias. Partir d’une arborescence claire évite les réorganisations plus tard.'
          ]
        }
      ]
    },
    {
      id: 'reconnexion-finale',
      title: 'Fin de l’installation : reconnexion obligatoire',
      icon: 'sync',
      body: [
        'En fin d’installation, le script peut indiquer qu’une reconnexion est encore nécessaire pour bénéficier pleinement des changements.',
        'Appliquez cette reconnexion avant d’aller plus loin.'
      ],
      codeBlocks: [
        {
          title: 'Message final typique',
          language: 'bash',
          code:
            "Pour bénéficier des changements, vous devez vous déconnecter/reconnecter.\nL'installation est maintenant terminée.\nPour le configurer ou modifier les applications, vous pouvez le relancer :\ncd /home/ubuntu/seedbox-compose\n./seedbox.sh"
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Après reconnexion, vous devez accéder à l’accueil du script sans erreur et avec Docker pleinement fonctionnel.'
          ]
        }
      ]
    },
    {
      id: 'checklist-finale',
      title: 'Checklist finale',
      icon: 'check-circle',
      items: [
        'Script lancé avec ./seedbox.sh',
        'Langue choisie',
        'Répertoire seedbox défini',
        'Utilisateur ajouté au groupe docker si nécessaire',
        'Reconnexion effectuée après ajout au groupe docker',
        'Mot de passe, mail et domaine saisis',
        'Cloudflare activé si applicable',
        'Traefik configuré en auth basique',
        'Dossiers médias créés',
        'Reconnexion finale effectuée'
      ]
    },
    {
      id: 'bravo',
      title: 'Bravo',
      icon: 'sparkles',
      body: [
        'Vous avez maintenant accès à l’accueil du script.',
        'Vous êtes prêt pour l’installation des applications et la configuration des services comme Plex, Arr, Prowlarr ou Overseerr.'
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Suite logique',
          content: [
            'La base est maintenant prête pour la phase d’installation applicative et les intégrations.'
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
          title: 'Premier lancement SSDV2',
          code:
            'sequenceDiagram\n' +
            '  autonumber\n' +
            '  actor U as Utilisateur\n' +
            '  participant S as seedbox.sh\n' +
            '  participant D as Docker\n' +
            '  participant C as Cloudflare\n' +
            '  participant T as Traefik\n\n' +
            '  U->>S: Lance ./seedbox.sh\n' +
            '  S-->>U: Choix langue + répertoire\n' +
            '  alt Utilisateur pas dans groupe docker\n' +
            '    S-->>U: Ajout au groupe docker\n' +
            '    U->>S: Déconnexion / reconnexion\n' +
            '    U->>S: Relance ./seedbox.sh\n' +
            '  end\n' +
            '  S-->>U: Auth basique (mdp / mail / domaine)\n' +
            '  alt Cloudflare activé\n' +
            '    U->>C: Fournit mail + API key\n' +
            '  end\n' +
            '  S->>D: Installation composants\n' +
            '  S->>T: Configuration Traefik\n' +
            '  S-->>U: Création dossiers médias\n' +
            '  S-->>U: Reconnexion finale requise\n' +
            '  U->>S: Nouvelle session SSH\n' +
            '  S-->>U: Script prêt ✅'
        }
      ]
    }
  ],
  steps: [
    {
      title: 'Lancer le script',
      text:
        'Exécutez seedbox.sh depuis le dépôt SSDV2 pour démarrer l’installation interactive.',
      result:
        'Le script doit afficher son interface et commencer le questionnaire de configuration.',
      icon: 'rocket'
    },
    {
      title: 'Choisir la langue et les chemins',
      text:
        'Sélectionnez la langue souhaitée puis renseignez le répertoire seedbox, généralement dans le home de votre utilisateur.',
      result:
        'La base de configuration du setup doit être définie proprement.',
      icon: 'settings'
    },
    {
      title: 'Gérer le groupe docker',
      text:
        'Si le script ajoute votre utilisateur au groupe docker, fermez la session, reconnectez-vous puis relancez immédiatement le script.',
      result:
        'Votre session doit reconnaître correctement les droits Docker.',
      icon: 'shield'
    },
    {
      title: 'Renseigner l’authentification',
      text:
        'Entrez le mot de passe, l’email et le domaine en suivant exactement les prompts du script.',
      result:
        'L’authentification de base doit être initialisée.',
      icon: 'key'
    },
    {
      title: 'Configurer Cloudflare si utilisé',
      text:
        'Activez l’option Cloudflare si votre domaine y est géré, puis fournissez email et API key.',
      result:
        'Le script doit pouvoir automatiser la gestion DNS si ce mode est choisi.',
      icon: 'globe'
    },
    {
      title: 'Configurer Traefik',
      text:
        'Laissez le sous-domaine non personnalisé si vous suivez le chemin standard, puis choisissez l’authentification basique.',
      result:
        'Le socle d’exposition principal doit être en place et cohérent.',
      icon: 'wrench'
    },
    {
      title: 'Créer les dossiers médias',
      text:
        'Créez les dossiers correspondant à votre organisation actuelle, avec ou sans bibliothèques 4K séparées.',
      result:
        'La structure média doit être prête pour la suite.',
      icon: 'folder-lock'
    },
    {
      title: 'Effectuer la reconnexion finale',
      text:
        'Appliquez la dernière reconnexion demandée par le script avant de continuer.',
      result:
        'Vous devez revenir sur un environnement propre, avec Docker et le script pleinement opérationnels.',
      icon: 'sync'
    }
  ],
  troubleshooting: [
    'Si Docker semble inaccessible après le lancement, vérifiez d’abord si une reconnexion après ajout au groupe docker a été oubliée.',
    'Si le script semble bloqué pendant les tâches d’installation, laissez-lui du temps : certaines phases peuvent être silencieuses.',
    'Si Cloudflare ne fonctionne pas, vérifiez que le domaine est bien géré par Cloudflare et que l’API key est correcte.',
    'Si le domaine est refusé ou mal pris en compte, assurez-vous de l’avoir saisi sans https://.',
    'Si les dossiers médias ne correspondent pas à votre future organisation, corrigez-les maintenant plutôt que plus tard.',
    'Si le script se relance mais que le comportement semble incohérent, repartez d’une session SSH fraîche.'
  ],
  checklist: [
    { text: 'Script lancé avec succès' },
    { text: 'Langue sélectionnée' },
    { text: 'Répertoire seedbox défini' },
    { text: 'Reconnexion effectuée après ajout au groupe docker si nécessaire' },
    { text: 'Authentification basique renseignée' },
    { text: 'Cloudflare activé si applicable' },
    { text: 'Traefik configuré en auth basique' },
    { text: 'Dossiers médias créés' },
    { text: 'Reconnexion finale effectuée' }
  ],
  finalChecklist: [
    'Le script SSDV2 se lance correctement',
    'Docker fonctionne avec votre session utilisateur',
    'Traefik et les composants de base sont en place',
    'Les dossiers médias sont prêts',
    'Vous pouvez passer à l’installation et à la configuration des applications'
  ]
};