import fs from 'fs'
import path from 'path'
import { HandbookNav } from '@/components/handbook/navigation'
import ReactMarkdown from 'react-markdown'
import { TOC } from '@/types/handbook'

export async function generateStaticParams() {
  const tocPath = path.join(process.cwd(), 'src/handbook/toc.json')
  const toc: TOC = JSON.parse(fs.readFileSync(tocPath, 'utf8'))
  return toc.flatMap((chapter) => chapter[2]).map((group) => ({ group }))
}

export default function GroupPage({ params }: { params: { group: string } }) {
  const mdPath = path.join(process.cwd(), 'src/handbook/md', `${params.group}.md`)
  const content = fs.readFileSync(mdPath, 'utf8')
  const toc: TOC = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/handbook/toc.json'), 'utf8'))
  const title = content.split('\n')[0].replace('# ', '')

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <HandbookNav toc={toc} />
      
      <article className="prose lg:prose-xl mt-8">
        <h1>{title}</h1>
        <ReactMarkdown>{content.split('\n').slice(1).join('\n')}</ReactMarkdown>
      </article>
    </div>
  )
}
