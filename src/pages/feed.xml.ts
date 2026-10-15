import rss from '@astrojs/rss'
import { project } from '@layouts/project'
import type { APIContext } from 'astro'
import { getCollection } from 'astro:content'

export async function GET(context: APIContext) {
  const posts = await getCollection('posts')

  return rss({
    title: project.meta.title,
    description: project.meta.description,
    site: context.site!,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `posts/${post.id}`,
      customData: `<language>${post.data.language || 'de'}</language>`,
    })),
  })
}
