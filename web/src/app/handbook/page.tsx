import fs from 'fs'
import path from 'path'
import Link from 'next/link'
import { HandbookNav } from '@/components/handbook/navigation'

function getGroupTitle(groupId: string) {
  const mdPath = path.join(process.cwd(), 'src/handbook/md', `${groupId}.md`)
  const content = fs.readFileSync(mdPath, 'utf8')
  return content.split('\n')[0].replace('# ', '')
}

export default function HandbookTOC() {
  const tocPath = path.join(process.cwd(), 'src/handbook/toc.json')
  const toc = JSON.parse(fs.readFileSync(tocPath, 'utf8'))

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Handbook Contents</h1>
      <HandbookNav toc={toc} />
      
      <div className="mt-8 space-y-6">
        {toc.map(([num, title, groups]: [number, string, string[]]) => (
          <div key={num}>
            <h2 className="text-2xl font-semibold mb-3">Chapter {num}: {title}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {groups.map((groupId) => (
                <Link
                  key={groupId}
                  href={`/handbook/${groupId}`}
                  className="p-4 border rounded-lg hover:bg-gray-50"
                >
                  <h3 className="font-medium">{groupId}</h3>
                  <p className="text-sm text-gray-600">{getGroupTitle(groupId)}</p>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
