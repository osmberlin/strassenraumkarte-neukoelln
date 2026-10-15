import type { LayoutLanguage } from './languages'

// Same shape as `TProjectConfig` in www.osm-verkehrswende.org (`cms/projectsAstro.ts`),
// but static since this site has only one project and no Keystatic.
export type TProjectConfig = {
  name: { name: string; slug: string }
  menus: {
    label?: string | null
    items: { href: string; label: string }[]
  }[]
  menuNews: boolean
  additionalFooterLinks: { href: string; label: string }[]
  meta: {
    title: string
    description: string
    imageAlt: string
    language: LayoutLanguage
  }
}

export const project: TProjectConfig = {
  name: { name: 'Straßenraumkarte', slug: 'strassenraumkarte' },
  menus: [
    {
      label: null,
      items: [
        // The map always opens the latest releases; older ones are picked in the map itself
        { href: '/', label: 'Karte' },
        { href: '/about', label: 'Über das Projekt' },
      ],
    },
  ],
  menuNews: true,
  additionalFooterLinks: [],
  meta: {
    title: 'Straßenraumkarte Neukölln – OpenStreetMap Verkehrswende',
    description: 'Spezialkarten für Neukölln zum Straßenraum und zur Parkplatzdichte.',
    imageAlt: 'Ausschnitt der Parkraumkarte Neukölln mit Visualisierung des Flächenverbrauchs.',
    language: 'de',
  },
}
