"use client"

import { ColumnDef } from "@tanstack/react-table"
import { TestResultQuestionAnswer } from "@/types/test-result"

export const columns: ColumnDef<TestResultQuestionAnswer>[] = [
  {
    accessorKey: "question_id",
    header: "Question ID",
    enableSorting: true,
    enableColumnFilter: true,
  },
  {
    accessorKey: "is_correct",
    header: "Correct",
    cell: ({ row }) => row.getValue("is_correct") ? "✅" : "❌",
    enableSorting: true,
    enableColumnFilter: true,
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  {
    accessorKey: "has_image",
    header: "Has Image",
    cell: ({ row }) => row.getValue("has_image") ? "Yes" : "No",
    enableSorting: true,
    enableColumnFilter: true,
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  }
]
