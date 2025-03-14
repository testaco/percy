'use client'

import { useRouter } from 'next/navigation'
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from '@/components/ui/select'
import { TOC } from '@/types/handbook'

export function HandbookNav({ toc, groupTitles = {} }: { toc: TOC, groupTitles?: Record<string, string> }) {
  const router = useRouter()

  return (
    <Select onValueChange={(value) => router.push(`/handbook/${value}`)}>
      <SelectTrigger className="w-[300px]">
        <SelectValue placeholder="Select a chapter..." />
      </SelectTrigger>
      <SelectContent>
        {toc.map(([chapterNum, chapterTitle, groups]) => (
          <SelectGroup key={chapterNum}>
            <SelectLabel>Chapter {chapterNum}: {chapterTitle}</SelectLabel>
            {groups.map((groupId) => (
              <SelectItem key={groupId} value={groupId}>
                {groupId}{groupTitles[groupId] ? ` - ${groupTitles[groupId]}` : ''}
              </SelectItem>
            ))}
          </SelectGroup>
        ))}
      </SelectContent>
    </Select>
  )
}
