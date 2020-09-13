// import defaultSettings from '@/settings'

const title = 'Prognomic'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
