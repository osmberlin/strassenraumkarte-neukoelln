import { astroPostsDefinition } from 'cms/postsAstro'
import { astroReleasesDefinition } from 'cms/releasesAstro'

export const collections = {
  posts: astroPostsDefinition,
  releases: astroReleasesDefinition,
}
