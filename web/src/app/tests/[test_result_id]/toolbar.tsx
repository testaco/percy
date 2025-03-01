"use client"

import { Table } from "@tanstack/react-table"
import { TestResultQuestionAnswer } from "@/types/test-result"
import { Input } from "@/components/ui/input"
import { DataTableFacetedFilter } from "./faceted-filter"

interface ToolbarProps {
  table: Table<TestResultQuestionAnswer>
}

export function Toolbar({ table }: ToolbarProps) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <Input
          placeholder="Filter questions..."
          value={(table.getColumn("question_id")?.getFilterValue() as string) ?? ""}
          onChange={(event) => {
            table.getColumn("question_id")?.setFilterValue(event.target.value)
          }}
          className="h-8 w-[150px] lg:w-[250px]"
        />
        
        <DataTableFacetedFilter
          column={table.getColumn("is_correct")}
          title="Correctness"
          options={[
            { label: "Correct", value: "true" },
            { label: "Incorrect", value: "false" },
          ]}
        />
        
        <DataTableFacetedFilter
          column={table.getColumn("has_image")}
          title="Has Image"
          options={[
            { label: "Has Image", value: "true" },
            { label: "No Image", value: "false" },
          ]}
        />
      </div>
    </div>
  )
}
