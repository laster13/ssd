import type { DocsNavGroup, Tutorial } from './types';
import { configurationStreamFusion } from './configuration-streamfusion';
import { googleOAuth2TraefikSsdv2 } from './google-oauth2-traefik-ssdv2';

export type {
  Tutorial,
  TutorialIcon,
  TutorialLevel,
  TutorialLink,
  TutorialSection,
  TutorialStep,
  TutorialCallout,
  TutorialCalloutTone,
  TutorialImage,
  TutorialDiagram,
  TutorialCodeBlock,
  TutorialChecklistItem,
  TutorialTabItem,
  TutorialAccordionItem,
  DocsNavItem,
  DocsNavGroup,
  TocItem
} from './types';

export const tutorials: Tutorial[] = [
  configurationStreamFusion,
  googleOAuth2TraefikSsdv2
];

export const docsNavGroups: DocsNavGroup[] = Object.values(
  tutorials.reduce<Record<string, DocsNavGroup>>((acc, tutorial) => {
    const groupName = tutorial.group ?? 'Guides';
    const categoryName = tutorial.category;

    if (!acc[groupName]) {
      acc[groupName] = {
        name: groupName,
        categories: []
      };
    }

    let category = acc[groupName].categories.find((c) => c.name === categoryName);

    if (!category) {
      category = {
        name: categoryName,
        items: []
      };
      acc[groupName].categories.push(category);
    }

    category.items.push({
      title: tutorial.title,
      slug: tutorial.slug,
      category: tutorial.category,
      group: groupName
    });

    return acc;
  }, {})
);