"use client"

import { ColumnDef } from "@tanstack/react-table"
import { TestResultQuestionAnswer } from "@/types/test-result"
import { ArrowUpDown } from "lucide-react"
import { Button } from "@/components/ui/button"

export const columns: ColumnDef<TestResultQuestionAnswer>[] = [
  {
    accessorKey: "question_id",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Question ID
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    enableSorting: true,
    enableColumnFilter: true,
  },
  {
    accessorKey: "is_correct",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Correct
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => row.getValue("is_correct") ? "✅" : "❌",
    enableSorting: true,
    enableColumnFilter: true,
    filterFn: (row, id, value) => {
      // Return true (show row) if no filters selected
      if (!value || value.length === 0) return true
      const rowValue = row.getValue(id) ? "true" : "false"
      return value.includes(rowValue)
    },
  },
  {
    accessorKey: "has_image",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Has Image
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
    cell: ({ row }) => row.getValue("has_image") ? "Yes" : "No",
    enableSorting: true,
    enableColumnFilter: true,
    filterFn: (row, id, value) => {
      // Return true (show row) if no filters selected
      if (!value || value.length === 0) return true
      const rowValue = row.getValue(id) ? "true" : "false"
      return value.includes(rowValue)
    },
  }
]
