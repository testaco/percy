"use client"
import { ColumnDef } from "@tanstack/react-table"
import Link from "next/link"
import { DataTableColumnHeader } from "@/components/ui/data-table-column-header"

export type ModelRow = {
  id: string
  name: string
  organization: string
  passes_technician: boolean
  passes_general: boolean
  passes_extra: boolean
  release_date: string
  param_count?: number | null
  input_context_size: number
  output_context_size: number
  license: string
  multimodal: boolean
  web_hydrated: boolean
}

export const columns: ColumnDef<ModelRow>[] = [
  {
    accessorKey: "name",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Model Name" />
    ),
    cell: ({ row }) => (
      <Link 
        href={`/models/${row.original.id}`}
        className="font-medium text-primary hover:underline"
      >
        {row.getValue("name")}
      </Link>
    ),
    enableHiding: false,
  },
  {
    accessorKey: "organization",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Organization" />
    ),
    enableHiding: false,
  },
  {
    accessorKey: "passes_technician",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Passes Technician" />
    ),
    cell: ({ row }) => row.getValue("passes_technician") ? "Yes" : "No",
    filterFn: (row, id, value) => {
      if (!value || value.length === 0) return true
      const rowValue = row.getValue(id) ? "true" : "false"
      return value.includes(rowValue)
    },
  },
  {
    accessorKey: "passes_general",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Passes General" />
    ),
    cell: ({ row }) => row.getValue("passes_general") ? "Yes" : "No",
    filterFn: (row, id, value) => {
      if (!value || value.length === 0) return true
      const rowValue = row.getValue(id) ? "true" : "false"
      return value.includes(rowValue)
    },
  },
  {
    accessorKey: "passes_extra",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Passes Extra" />
    ),
    cell: ({ row }) => row.getValue("passes_extra") ? "Yes" : "No",
    filterFn: (row, id, value) => {
      if (!value || value.length === 0) return true
      const rowValue = row.getValue(id) ? "true" : "false"
      return value.includes(rowValue)
    },
  },
  {
    accessorKey: "release_date",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Release Date" />
    ),
    cell: ({ row }) => new Date(row.getValue("release_date")).toLocaleDateString(),
  },
  {
    accessorKey: "param_count",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Parameters" />
    ),
    cell: ({ row }) => {
      const paramCount = row.getValue("param_count");
      return paramCount ? `${paramCount}B` : "Unknown";
    },
  },
  {
    accessorKey: "input_context_size",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Context Size" />
    ),
    cell: ({ row }) => `${row.getValue<number>("input_context_size").toLocaleString()} tokens`,
  },
  {
    accessorKey: "multimodal",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Multimodal" />
    ),
    cell: ({ row }) => row.getValue("multimodal") ? "Yes" : "No",
    filterFn: (row, id, value) => {
      if (!value || value.length === 0) return true
      const rowValue = row.getValue(id) ? "true" : "false"
      return value.includes(rowValue)
    },
  },
  {
    accessorKey: "web_hydrated",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="Web Access" />
    ),
    cell: ({ row }) => row.getValue("web_hydrated") ? "Yes" : "No",
    filterFn: (row, id, value) => {
      if (!value || value.length === 0) return true
      const rowValue = row.getValue(id) ? "true" : "false"
      return value.includes(rowValue)
    },
  },
  {
    accessorKey: "license",
    header: ({ column }) => (
      <DataTableColumnHeader column={column} title="License" />
    ),
  },
];
