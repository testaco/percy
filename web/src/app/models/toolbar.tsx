"use client"

import { Table } from "@tanstack/react-table"
import { Input } from "@/components/ui/input"
import { DataTableFacetedFilter } from "./faceted-filter"
import { DataTableViewOptions } from "@/components/ui/data-table-view-options"

interface ToolbarProps<TData> {
  table: Table<TData>
}

export function Toolbar<TData>({ table }: ToolbarProps<TData>) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <Input
          placeholder="Filter models..."
          value={(table.getColumn("name")?.getFilterValue() as string) ?? ""}
          onChange={e => table.getColumn("name")?.setFilterValue(e.target.value)}
          className="h-8 w-[150px] lg:w-[250px]"
        />
        
        <DataTableFacetedFilter
          column={table.getColumn("organization")}
          title="Organization"
          options={Array.from(new Set(
            table.getRowModel().rows.map(row => row.original.organization)
          )).map(org => ({ label: org as string, value: org as string }))}
        />
        
        <DataTableFacetedFilter
          column={table.getColumn("passes_technician")}
          title="Passes Tech"
          options={[
            { label: "Yes", value: "true" },
            { label: "No", value: "false" }
          ]}
        />

        <DataTableFacetedFilter
          column={table.getColumn("passes_general")}
          title="Passes General"
          options={[
            { label: "Yes", value: "true" },
            { label: "No", value: "false" }
          ]}
        />

        <DataTableFacetedFilter
          column={table.getColumn("passes_extra")}
          title="Passes Extra"
          options={[
            { label: "Yes", value: "true" },
            { label: "No", value: "false" }
          ]}
        />
      </div>
      <DataTableViewOptions table={table} />
    </div>
  )
}
