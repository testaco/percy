import fs from 'fs'
import path from 'path'
import { HandbookNav } from '@/components/handbook/navigation'
import ReactMarkdown from 'react-markdown'
import { TOC } from '@/types/handbook'
import { cn } from '@/lib/utils'

export async function generateStaticParams() {
  const tocPath = path.join(process.cwd(), 'src/handbook/toc.json')
  const toc: TOC = JSON.parse(fs.readFileSync(tocPath, 'utf8'))
  return toc.flatMap((chapter) => chapter[2]).map((group) => ({ group }))
}

export default async function GroupPage({ params }: { params: Promise<{ group: string }> }) {
  const { group } = await params;
  const mdPath = path.join(process.cwd(), 'src/handbook/md', `${group}.md`);
  const content = fs.readFileSync(mdPath, 'utf8');
  const toc: TOC = JSON.parse(fs.readFileSync(path.join(process.cwd(), 'src/handbook/toc.json'), 'utf8'));
  const title = content.split('\n')[0].replace('# ', '');

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <HandbookNav toc={toc} />
      
      <article className="prose lg:prose-xl mt-8">
        <h1>{title}</h1>
        <ReactMarkdown
          components={{
            h1: ({ className, ...props }) => (
              <h1 className={cn("text-3xl font-bold mt-6 mb-4", className)} {...props} />
            ),
            h2: ({ className, ...props }) => (
              <h2 className={cn("text-2xl font-bold mt-5 mb-3", className)} {...props} />
            ),
            h3: ({ className, ...props }) => (
              <h3 className={cn("text-xl font-bold mt-4 mb-2", className)} {...props} />
            ),
            h4: ({ className, ...props }) => (
              <h4 className={cn("text-lg font-semibold mt-3 mb-2", className)} {...props} />
            ),
            h5: ({ className, ...props }) => (
              <h5 className={cn("text-base font-semibold mt-2 mb-1", className)} {...props} />
            ),
            h6: ({ className, ...props }) => (
              <h6 className={cn("text-sm font-semibold mt-2 mb-1", className)} {...props} />
            ),
          }}
        >
          {content.split('\n').slice(1).join('\n')}
        </ReactMarkdown>
      </article>
    </div>
  )
}
