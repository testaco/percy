'use client'

import { useRouter } from 'next/navigation'
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from '@/components/ui/select'

export function HandbookNav({ toc }: { toc: any[] }) {
  const router = useRouter()

  return (
    <Select onValueChange={(value) => router.push(`/handbook/${value}`)}>
      <SelectTrigger className="w-[300px]">
        <SelectValue placeholder="Select a chapter..." />
      </SelectTrigger>
      <SelectContent>
        {toc.map((chapter) => (
          <SelectGroup key={chapter[0]}>
            <SelectLabel>Chapter {chapter[0]}: {chapter[1]}</SelectLabel>
            {chapter[2].map((groupId: string) => (
              <SelectItem key={groupId} value={groupId}>
                {groupId}
              </SelectItem>
            ))}
          </SelectGroup>
        ))}
      </SelectContent>
    </Select>
  )
}
