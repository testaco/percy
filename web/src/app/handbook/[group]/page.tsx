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
  
  // Extract title from first line and remove it from content to avoid duplication
  const title = content.split('\n')[0].replace('# ', '');
  const contentWithoutTitle = content.split('\n').slice(1).join('\n');
  
  // Create a map of group IDs to their titles
  const groupTitles: Record<string, string> = {};
  for (const groupId of toc.flatMap(chapter => chapter[2])) {
    try {
      const groupPath = path.join(process.cwd(), 'src/handbook/md', `${groupId}.md`);
      const groupContent = fs.readFileSync(groupPath, 'utf8');
      groupTitles[groupId] = groupContent.split('\n')[0].replace('# ', '');
    } catch (error) {
      console.warn(`Could not read title for group ${groupId} ${error}`);
    }
  }

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <HandbookNav toc={toc} groupTitles={groupTitles} />
      
      <article className="prose lg:prose-xl mt-8">
        <h1 className="text-3xl font-bold mb-6">{title}</h1>
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
          {contentWithoutTitle}
        </ReactMarkdown>
      </article>
    </div>
  )
}
