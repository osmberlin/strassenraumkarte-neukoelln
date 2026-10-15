import type { WritableAtom } from 'nanostores'
import { atom, onMount } from 'nanostores'

function isRouterClick(event: MouseEvent, link: HTMLAnchorElement) {
  return (
    link &&
    event.button === 0 && // Left mouse button
    link.target !== '_blank' && // Not for new tab
    link.origin === location.origin && // Not external link
    link.rel !== 'external' && // Not external link
    link.target !== '_self' && // Now manually disabled
    !link.download && // Not download link
    !event.altKey && // Not download link by user
    !event.metaKey && // Not open in new tab by user
    !event.ctrlKey && // Not open in new tab by user
    !event.shiftKey && // Not open in new window by user
    !event.defaultPrevented // Click was not cancelled
  )
}

export interface SearchParamsOptions {
  links?: boolean
}

/**
 * Store to watch for `?search` URL part changes.
 *
 * It will track history API and clicks on page’s links.
 */
export interface SearchParamsStore extends WritableAtom<Record<string, string>> {
  /**
   * Change `?search` URL part and update store value.
   *
   * ```js
   * searchParams.open({ sort: 'name', type: 'small' })
   * ```
   *
   * @param path Absolute URL (`https://example.com/a`)
   *             or domain-less URL (`/a`).
   * @param redirect Don’t add entry to the navigation history.
   */
  open(params: Record<string, string | number>, redirect?: boolean): void
}

/**
 * Create {@link SearchParamsStore} store to watch for `?search` URL part.
 *
 * ```js
 * export const searchParams = createSearchParams()
 * ```
 *
 * @param opts Options.
 */
export function createSearchParams(opts?: SearchParamsOptions): SearchParamsStore {
  const store = atom({}) as SearchParamsStore

  const set = store.set
  if (process.env.NODE_ENV !== 'production') {
    // @ts-expect-error
    delete store.set
  }

  let prev: string
  const update = (href: string) => {
    const url = new URL(href)
    if (prev === url.search) return undefined
    prev = url.search
    set(Object.fromEntries(url.searchParams))
  }

  store.open = (params, redirect) => {
    // @ts-expect-error our input type allow values of number which seems to work, so lets ignore the error
    const urlParams = new URLSearchParams(params)
    let search = urlParams.toString()
    if (search) search = '?' + search

    if (prev === search) return
    prev = search

    if (typeof history !== 'undefined') {
      let href = location.pathname + search + location.hash
      if (typeof history !== 'undefined') {
        if (redirect) {
          history.replaceState(null, '', href)
        } else {
          history.pushState(null, '', href)
        }
      }
    }
    set(Object.fromEntries(urlParams.entries()))
  }

  const click = (event: any) => {
    const link = event.target.closest('a')
    if (isRouterClick(event, link)) {
      if (link.search !== prev) {
        prev = link.search
        set(Object.fromEntries(new URL(link.href).searchParams))
      }
      if (link.pathname === location.pathname && link.hash === location.hash) {
        event.preventDefault()
        history.pushState(null, '', link.href)
      }
    }
  }

  const popstate = () => {
    update(location.href)
  }

  if (typeof window !== 'undefined' && typeof location !== 'undefined') {
    onMount(store, () => {
      popstate()
      if (opts?.links !== false) document.body.addEventListener('click', click)
      window.addEventListener('popstate', popstate)
      return () => {
        document.body.removeEventListener('click', click)
        window.removeEventListener('popstate', popstate)
      }
    })
  }

  return store
}
