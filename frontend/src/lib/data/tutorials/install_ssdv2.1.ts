import type { Tutorial } from './types';

export const configurationInitialeSshUtilisateurNonRootSsdv2: Tutorial = {
  slug: 'configuration-initiale-ssh-utilisateur-non-root-ssdv2',
  title: 'Configuration initiale — SSH, utilisateur non-root et préparation SSDV2',
  description:
    'Guide premium de démarrage SSDV2 : connexion SSH via PuTTY, création d’un utilisateur non-root avec sudo, mises à jour système, installation de Git, bascule root vers non-root, clonage du dépôt SSDV2 et correction des permissions.',
  summary:
    'Cette page couvre la configuration initiale d’un serveur avant d’installer ou d’administrer SSDV2. Elle détaille la connexion SSH, la création d’un utilisateur non-root, l’ajout au groupe sudo, la mise à jour du système, l’installation de Git, la sortie propre du compte root, puis le clonage du dépôt SSDV2 et la correction des permissions pour repartir sur une base saine et sécurisée.',
  level: 'débutant',
  duration: '15 à 30 min',
  estimatedTime:
    'Environ 15 à 30 minutes pour établir la connexion SSH, créer l’utilisateur non-root, préparer le système et cloner SSDV2 avec des permissions propres.',
  category: 'Installation',
  group: 'Installation SSDv2',
  icon: 'shield',
  tags: [
    'ssdv2',
    'ssh',
    'putty',
    'linux',
    'security',
    'git',
    'sudo',
    'root',
    'non-root',
    'permissions'
  ],
  prerequisites: [
    'Un serveur ou VPS accessible à distance',
    'L’adresse IP ou le hostname du serveur',
    'Les identifiants de connexion initiaux fournis par l’hébergeur',
    'Un accès root initial ou équivalent',
    'PuTTY sur Windows, ou un client SSH équivalent',
    'Une connexion réseau stable pour administrer le serveur'
  ],
  access: [
    {
      label: 'Site officiel PuTTY',
      url: 'https://www.putty.org/'
    }
  ],
  links: [
    {
      label: 'Site officiel PuTTY',
      url: 'https://www.putty.org/'
    }
  ],
  callouts: [
    {
      tone: 'abstract',
      title: 'Abstract',
      content: [
        'Cette section couvre la configuration initiale d’un serveur avant d’installer ou d’administrer SSDV2 : connexion SSH via PuTTY, création d’un utilisateur non-root avec sudo, mise à jour du système, installation de Git, bascule propre root vers non-root, puis clonage et correction des permissions du dépôt SSDV2.',
        'L’objectif est de poser une base saine, sécurisée et cohérente avant d’aller plus loin dans le déploiement.'
      ]
    },
    {
      tone: 'tip',
      title: 'Raccourci mental',
      content: [
        'Root = dépannage ponctuel.',
        'Non-root + sudo = exploitation normale.',
        'Session root fermée dès que possible.'
      ]
    }
  ],
  warnings: [
    'Pour la suite du guide, il est impératif de ne plus utiliser root au quotidien.',
    'Continuer en root provoque souvent des permissions incohérentes et des erreurs difficiles à diagnostiquer.',
    'Vérifiez soigneusement l’IP, le port SSH et l’identité du serveur lors de la première connexion.',
    'Ne clonez pas SSDV2 dans un dossier appartenant à root si vous comptez l’exécuter ensuite en non-root.',
    'Une mauvaise gestion des permissions au départ peut compliquer toutes les étapes suivantes.'
  ],
  sections: [
    {
      id: 'tldr',
      title: 'l’essentiel en quelques points',
      icon: 'rocket',
      items: [
        'Se connecter en SSH avec PuTTY ou un client équivalent',
        'Créer un utilisateur non-root et l’ajouter au groupe sudo',
        'Mettre à jour le système puis installer Git',
        'Abandonner root pour la suite du guide',
        'Cloner SSDV2 puis remettre le dossier au bon propriétaire'
      ]
    },
    {
      id: 'objectif-regles-dor',
      title: 'Objectif & règles d’or',
      icon: 'shield',
      items: [
        'Se connecter au serveur en SSH',
        'Créer un utilisateur non-root et lui donner les droits sudo',
        'Mettre à jour le système et installer Git',
        'Arrêter d’utiliser root pour la suite du guide',
        'Cloner SSDV2 et corriger les permissions'
      ],
      callouts: [
        {
          tone: 'danger',
          title: 'Sécurité',
          content: [
            'Pour la suite du guide, il est impératif de ne plus utiliser le compte root.',
            'Le compte root augmente le risque d’erreurs destructives, de permissions incohérentes et de mauvaises pratiques d’exploitation.'
          ]
        }
      ]
    },
    {
      id: 'vue-densemble',
      title: 'Vue d’ensemble (ordre recommandé)',
      icon: 'sync',
      diagrams: [
        {
          title: 'Workflow de préparation initiale',
          code:
            'flowchart TD\n' +
            '  A["Connexion SSH (PuTTY)"] --> B["Création utilisateur non-root"]\n' +
            '  B --> C["Ajout au groupe sudo"]\n' +
            '  C --> D["Mise à jour système (apt)"]\n' +
            '  D --> E["Installation Git"]\n' +
            '  E --> F["Bascule root -> non-root"]\n' +
            '  F --> G["Clonage SSDV2"]\n' +
            '  G --> H["Correction permissions (chown)"]\n' +
            '  H --> I["Configuration initiale terminée ✅"]'
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Ordre recommandé',
          content: [
            'Le plus important est de sortir de root tôt, puis de continuer tout le reste avec un utilisateur standard disposant de sudo.'
          ]
        }
      ]
    },
    {
      id: 'connexion-ssh',
      title: 'Connexion SSH',
      icon: 'server',
      body: [
        'La première étape consiste à établir une connexion distante au serveur.',
        'PuTTY reste un choix très courant sous Windows, mais toute alternative SSH fiable peut convenir.'
      ],
      tabs: [
        {
          label: 'Installer PuTTY',
          content: [
            'Rendez-vous sur le site officiel https://www.putty.org/.',
            'Téléchargez la version adaptée à votre système.',
            'Lancez l’installation puis ouvrez PuTTY.'
          ]
        },
        {
          label: 'Se connecter',
          content: [
            'Renseignez Host Name avec l’IP ou le hostname du serveur.',
            'Utilisez le port 22 par défaut, sauf configuration différente.',
            'Choisissez le protocole SSH.',
            'Optionnel : enregistrez la session dans Saved Sessions.',
            'Cliquez sur Open, acceptez la clé inconnue à la première connexion, puis saisissez login et mot de passe.'
          ]
        },
        {
          label: 'Alternative',
          content: [
            'Sous Windows 10/11, Windows Terminal avec ssh natif peut aussi convenir.',
            'PuTTY reste cependant parfaitement valide et très répandu.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Que signifie l’alerte de clé inconnue ?',
          content: [
            'Lors de la première connexion, le client SSH ne connaît pas encore l’identité du serveur. C’est normal. En environnement sensible, comparez l’empreinte de clé avec celle fournie par votre hébergeur ou votre console VPS.'
          ]
        }
      ],
      callouts: [
        {
          tone: 'warning',
          title: 'Bon réflexe sécurité',
          content: [
            'Si vous avez un accès console ou panel VPS, vérifiez l’empreinte de la clé SSH lors de la première connexion.'
          ]
        }
      ]
    },
    {
      id: 'creation-utilisateur-non-root',
      title: 'Création d’un utilisateur non-root',
      icon: 'user',
      body: [
        'Le compte root ne doit servir qu’au bootstrap initial ou au dépannage ponctuel.',
        'Le bon fonctionnement quotidien du serveur doit se faire via un utilisateur standard bénéficiant de sudo.'
      ],
      codeBlocks: [
        {
          title: 'Créer un utilisateur standard',
          language: 'bash',
          code: 'adduser nom_utilisateur'
        },
        {
          title: 'Ajouter l’utilisateur au groupe sudo',
          language: 'bash',
          code: 'usermod -aG sudo nom_utilisateur'
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Validation rapide',
          content: [
            'Une fois connecté avec le nouvel utilisateur, exécutez sudo -v.',
            'Si le mot de passe est demandé puis accepté, les droits sudo sont opérationnels.'
          ]
        }
      ],
      accordions: [
        {
          title: 'Pourquoi ne pas continuer directement avec root ?',
          content: [
            'Parce que root peut modifier, supprimer ou casser n’importe quoi sans garde-fou. Travailler au quotidien avec un compte standard réduit fortement le risque d’erreurs irréversibles.'
          ]
        }
      ]
    },
    {
      id: 'mise-a-jour-paquets',
      title: 'Mise à jour des paquets',
      icon: 'refresh-cw',
      body: [
        'Avant d’installer quoi que ce soit, il est préférable de repartir sur une base système à jour.',
        'Cela réduit les surprises liées aux dépendances, aux correctifs de sécurité et aux écarts de versions.'
      ],
      codeBlocks: [
        {
          title: 'Mettre à jour le système',
          language: 'bash',
          code: 'sudo apt update && sudo apt upgrade -y'
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Pourquoi maintenant ?',
          content: [
            'Installer SSDV2 sur une base à jour améliore la compatibilité et limite les problèmes évitables.'
          ]
        }
      ]
    },
    {
      id: 'installation-git',
      title: 'Installation de Git',
      icon: 'download',
      body: [
        'Git est nécessaire pour récupérer le dépôt SSDV2.',
        'Installez-le une fois la base système mise à jour.'
      ],
      codeBlocks: [
        {
          title: 'Installer Git',
          language: 'bash',
          code: 'sudo apt install -y git'
        }
      ]
    },
    {
      id: 'passage-root-non-root',
      title: 'Passage de root à non-root (obligatoire)',
      icon: 'shield',
      body: [
        'À partir de cette étape, vous devez cesser d’utiliser root pour la suite du guide.',
        'L’idée est d’éviter de créer des fichiers, des dossiers et des exécutions sous le mauvais propriétaire.'
      ],
      tabs: [
        {
          label: 'Méthode 1 — Reconnexion',
          content: [
            'Fermez la session root.',
            'Rouvrez votre client SSH.',
            'Reconnectez-vous avec nom_utilisateur.',
            'C’est la méthode recommandée car elle repart d’un environnement propre.'
          ]
        },
        {
          label: 'Méthode 2 — su -l',
          content: [
            'Dans la session actuelle, exécutez su -l nom_utilisateur.',
            'Saisissez ensuite le mot de passe du nouvel utilisateur.',
            'Le -l simule une vraie connexion avec un environnement utilisateur propre.'
          ]
        }
      ],
      codeBlocks: [
        {
          title: 'Basculer dans la même session',
          language: 'bash',
          code: 'su -l nom_utilisateur'
        }
      ],
      callouts: [
        {
          tone: 'tip',
          title: 'Pourquoi su -l ?',
          content: [
            'su -l simule une vraie connexion et évite des incohérences d’environnement, de chemins et parfois de permissions.'
          ]
        },
        {
          tone: 'danger',
          title: 'Risque permissions',
          content: [
            'Continuer en root entraîne souvent des permissions incohérentes et des erreurs difficiles à diagnostiquer.',
            'Passez non-root maintenant, pas plus tard.'
          ]
        }
      ]
    },
    {
      id: 'clonage-ssdv2',
      title: 'Clonage du script SSDV2',
      icon: 'git-branch',
      body: [
        'Une fois connecté en non-root, vous pouvez récupérer le dépôt SSDV2.',
        'Le dépôt est cloné dans le home de l’utilisateur courant, dans un dossier seedbox-compose.'
      ],
      codeBlocks: [
        {
          title: 'Cloner SSDV2',
          language: 'bash',
          code: 'sudo git clone https://github.com/projetssd/ssdv2.git /home/${USER}/seedbox-compose'
        }
      ],
      callouts: [
        {
          tone: 'info',
          title: 'Pourquoi sudo ici ?',
          content: [
            'Selon le système et le chemin visé, l’écriture peut demander des droits élevés.',
            'L’étape suivante remet ensuite l’arborescence au bon propriétaire.'
          ]
        }
      ]
    },
    {
      id: 'permissions-dossier',
      title: 'Appropriation des droits sur le dossier SSDV2',
      icon: 'folder-lock',
      body: [
        'Après le clonage, assurez-vous que le dossier appartient bien à votre utilisateur.',
        'Cela évite les blocages ultérieurs lors de l’exécution, des modifications ou des mises à jour.'
      ],
      codeBlocks: [
        {
          title: 'Corriger les permissions',
          language: 'bash',
          code: 'sudo chown -R ${USER}: /home/${USER}/seedbox-compose'
        }
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Validation',
          content: [
            'Votre utilisateur doit être propriétaire du dossier seedbox-compose.',
            'Vous évitez ainsi les galères de permissions pour la suite.'
          ]
        }
      ]
    },
    {
      id: 'checklist-finale',
      title: 'Checklist finale (validation)',
      icon: 'check-circle',
      items: [
        'Connexion SSH OK',
        'Utilisateur non-root créé',
        'Utilisateur ajouté à sudo',
        'Système à jour',
        'Git installé',
        'Session root abandonnée',
        'Dépôt SSDV2 cloné dans /home/${USER}/seedbox-compose',
        'Permissions corrigées avec chown'
      ]
    },
    {
      id: 'diagramme-sequence',
      title: 'Diagramme de séquence (résumé)',
      icon: 'sync',
      diagrams: [
        {
          title: 'SSH, utilisateur non-root et préparation SSDV2',
          code:
            'sequenceDiagram\n' +
            '  autonumber\n' +
            '  actor U as Admin\n' +
            '  participant P as PuTTY\n' +
            '  participant S as Serveur\n' +
            '  participant A as APT\n' +
            '  participant G as Git\n' +
            '  participant R as Repo SSDV2\n\n' +
            '  U->>P: Ouvre session SSH (root)\n' +
            '  P->>S: Connexion\n' +
            '  U->>S: adduser nom_utilisateur\n' +
            '  U->>S: usermod -aG sudo nom_utilisateur\n' +
            '  alt Reconnexion (recommandé)\n' +
            '    U->>P: Ferme session root\n' +
            '    U->>P: Ouvre session non-root\n' +
            '  else su -l (rapide)\n' +
            '    U->>S: su -l nom_utilisateur\n' +
            '  end\n' +
            '  U->>A: sudo apt update && sudo apt upgrade -y\n' +
            '  U->>A: sudo apt install -y git\n' +
            '  U->>G: sudo git clone SSDV2\n' +
            '  G->>R: Clone dépôt\n' +
            '  U->>S: sudo chown -R ${USER}: /home/${USER}/seedbox-compose\n' +
            '  S-->>U: Prêt pour la suite ✅'
        }
      ]
    },
    {
      id: 'felicitations',
      title: 'Félicitations',
      icon: 'sparkles',
      body: [
        'La configuration initiale est terminée.',
        'Vous pouvez maintenant continuer SSDV2 dans de bonnes conditions : sécurité, permissions propres et base système saine.'
      ],
      callouts: [
        {
          tone: 'success',
          title: 'Résultat attendu',
          content: [
            'Le serveur est prêt pour la suite du guide avec un utilisateur non-root, une base à jour, Git installé et un dépôt SSDV2 exploitable.'
          ]
        }
      ]
    }
  ],
  steps: [
    {
      title: 'Établir la connexion SSH',
      text:
        'Installez PuTTY ou utilisez un client SSH équivalent, puis connectez-vous au serveur avec les identifiants initiaux fournis.',
      result:
        'Vous devez obtenir un shell distant opérationnel sur le serveur.',
      icon: 'server'
    },
    {
      title: 'Créer un utilisateur non-root',
      text:
        'Créez un utilisateur standard dédié à l’administration courante du serveur, puis ajoutez-le au groupe sudo.',
      result:
        'Vous devez disposer d’un compte non-root capable d’exécuter des commandes administratives avec sudo.',
      icon: 'user'
    },
    {
      title: 'Mettre à jour le système',
      text:
        'Lancez sudo apt update && sudo apt upgrade -y pour repartir d’une base saine et à jour.',
      result:
        'Le système doit être mis à jour avant d’aller plus loin.',
      icon: 'refresh-cw'
    },
    {
      title: 'Installer Git',
      text:
        'Installez Git pour pouvoir récupérer le dépôt SSDV2 directement depuis sa source.',
      result:
        'Git doit être disponible sur le serveur.',
      icon: 'download'
    },
    {
      title: 'Quitter root',
      text:
        'Fermez la session root et reconnectez-vous avec le nouvel utilisateur, ou utilisez su -l pour basculer proprement.',
      result:
        'La suite du guide doit être exécutée en non-root.',
      icon: 'shield'
    },
    {
      title: 'Cloner SSDV2',
      text:
        'Clonez le dépôt SSDV2 dans le home de l’utilisateur courant, dans un dossier seedbox-compose.',
      result:
        'Le dépôt doit être présent localement sur le serveur.',
      icon: 'git-branch'
    },
    {
      title: 'Corriger les permissions',
      text:
        'Remettez l’arborescence clonée au bon propriétaire avec chown pour éviter les conflits de permissions.',
      result:
        'Votre utilisateur doit posséder le dossier SSDV2 et pouvoir l’exploiter correctement.',
      icon: 'folder-lock'
    }
  ],
  troubleshooting: [
    'Si PuTTY refuse la connexion, vérifiez l’IP, le port SSH et les règles de pare-feu.',
    'Si sudo ne fonctionne pas avec le nouvel utilisateur, revérifiez son appartenance au groupe sudo.',
    'Si vous restez en root trop longtemps, vous risquez de créer des fichiers qui bloqueront ensuite l’exécution en non-root.',
    'Si git clone échoue, vérifiez la connectivité réseau du serveur et la présence de Git.',
    'Si vous voyez des erreurs de permissions sur seedbox-compose, appliquez de nouveau chown -R ${USER}: /home/${USER}/seedbox-compose.',
    'Si su -l donne un environnement étrange, fermez la session et reconnectez-vous proprement avec l’utilisateur non-root.'
  ],
  checklist: [
    { text: 'Connexion SSH fonctionnelle' },
    { text: 'Utilisateur non-root créé' },
    { text: 'Utilisateur ajouté au groupe sudo' },
    { text: 'Système mis à jour' },
    { text: 'Git installé' },
    { text: 'Session root abandonnée pour la suite' },
    { text: 'Dépôt SSDV2 cloné dans /home/${USER}/seedbox-compose' },
    { text: 'Permissions du dossier corrigées' }
  ],
  finalChecklist: [
    'Vous administrez désormais le serveur en non-root avec sudo',
    'Le système est à jour et prêt pour la suite',
    'Le dépôt SSDV2 est cloné avec des permissions propres',
    'La base de travail est sécurisée et cohérente pour continuer'
  ]
};