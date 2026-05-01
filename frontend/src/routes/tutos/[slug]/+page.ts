import { error } from '@sveltejs/kit';
import { docsNavGroups, tutorials, type TocItem } from '$lib/data/tutorials';

function slugify(value: string) {
  return value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

export function load({ params }) {
  const tutorial = tutorials.find((item) => item.slug === params.slug);

  if (!tutorial) {
    throw error(404, 'Tutoriel introuvable');
  }

  const toc: TocItem[] = [
    { id: 'etapes', label: 'Étapes', level: 1 }
  ];

  if (tutorial.callouts?.length) {
    toc.unshift({ id: 'introduction', label: 'Introduction', level: 1 });
  }

  if (tutorial.images?.length) {
    toc.push({ id: 'captures', label: 'Captures', level: 1 });
  }

  if (tutorial.diagrams?.length) {
    toc.push({ id: 'diagrammes', label: 'Diagrammes', level: 1 });
  }

  if (tutorial.codeBlocks?.length) {
    toc.push({ id: 'blocs-configuration', label: 'Blocs de configuration', level: 1 });
  }

  for (const section of tutorial.sections ?? []) {
    toc.push({
      id: section.id ?? slugify(section.title),
      label: section.title,
      level: 2
    });
  }

  return {
    tutorial,
    docsNavGroups,
    toc
  };
}