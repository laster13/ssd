export type TutorialLevel = 'débutant' | 'intermédiaire' | 'avancé';

export type TutorialIcon =
  | 'rocket'
  | 'settings'
  | 'database'
  | 'shield'
  | 'key'
  | 'sync'
  | 'sparkles'
  | 'server'
  | 'bug'
  | 'wrench'
  | 'book'
  | 'search'
  | 'folder';

export type TutorialCalloutTone =
  | 'abstract'
  | 'tip'
  | 'info'
  | 'warning'
  | 'danger'
  | 'success';

export type TutorialLink = {
  label: string;
  url: string;
};

export type TutorialImage = {
  src: string;
  alt: string;
  caption?: string;
};

export type TutorialDiagram = {
  title?: string;
  code: string;
};

export type TutorialCodeBlock = {
  title?: string;
  language?: string;
  code: string;
};

export type TutorialChecklistItem = {
  text: string;
};

export type TutorialCallout = {
  tone: TutorialCalloutTone;
  title: string;
  content: string[];
};

export type TutorialTabItem = {
  label: string;
  content?: string[];
  codeBlocks?: TutorialCodeBlock[];
  callouts?: TutorialCallout[];
};

export type TutorialAccordionItem = {
  title: string;
  content?: string[];
  callouts?: TutorialCallout[];
  codeBlocks?: TutorialCodeBlock[];
};

export type TutorialStep = {
  title: string;
  text: string;
  code?: string;
  result?: string;
  icon?: TutorialIcon;
};

export type TutorialSection = {
  id?: string;
  title: string;
  items?: string[];
  body?: string[];
  icon?: TutorialIcon;
  callouts?: TutorialCallout[];
  images?: TutorialImage[];
  diagrams?: TutorialDiagram[];
  codeBlocks?: TutorialCodeBlock[];
  tabs?: TutorialTabItem[];
  accordions?: TutorialAccordionItem[];
};

export type Tutorial = {
  slug: string;
  title: string;
  description: string;
  summary?: string;
  level: TutorialLevel;
  duration: string;
  estimatedTime?: string;
  category: string;
  group?: string;
  icon?: TutorialIcon;
  tags?: string[];
  prerequisites?: string[];
  access?: TutorialLink[];
  links?: TutorialLink[];
  warnings?: string[];
  sections?: TutorialSection[];
  steps: TutorialStep[];
  troubleshooting?: string[];
  finalChecklist?: string[];
  checklist?: TutorialChecklistItem[];
  callouts?: TutorialCallout[];
  images?: TutorialImage[];
  diagrams?: TutorialDiagram[];
  codeBlocks?: TutorialCodeBlock[];
};

export type DocsNavItem = {
  title: string;
  slug: string;
  category: string;
  group: string;
};

export type DocsNavGroup = {
  name: string;
  categories: {
    name: string;
    items: DocsNavItem[];
  }[];
};

export type TocItem = {
  id: string;
  label: string;
  level?: 1 | 2 | 3;
};