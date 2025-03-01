"use client"

import * as React from "react"
import { Column } from "@tanstack/react-table"
import { PlusCircle } from "lucide-react"

import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Separator } from "@/components/ui/separator"

interface DataTableFacetedFilterProps<TData, TValue> {
  column?: Column<TData, TValue>
  title?: string
  options: {
    label: string
    value: string
    icon?: React.ComponentType<{ className?: string }>
  }[]
}

export function DataTableFacetedFilter<TData, TValue>({
  column,
  title,
  options,
}: DataTableFacetedFilterProps<TData, TValue>) {
  const facets = column?.getFacetedUniqueValues()
  const selectedValues = new Set(column?.getFilterValue() as string[])

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline" size="sm" className="h-8 border-dashed">
          <PlusCircle className="mr-2 h-4 w-4" />
          {title}
          {selectedValues?.size > 0 && (
            <>
              <Separator orientation="vertical" className="mx-2 h-4" />
              <Badge
                variant="secondary"
                className="rounded-sm px-1 font-normal lg:hidden"
              >
                {selectedValues.size}
              </Badge>
              <div className="hidden space-x-1 lg:flex">
                {selectedValues.size > 2 ? (
                  <Badge
                    variant="secondary"
                    className="rounded-sm px-1 font-normal"
                  >
                    {selectedValues.size} selected
                  </Badge>
                ) : (
                  options
                    .filter((option) => selectedValues.has(option.value))
                    .map((option) => (
                      <Badge
                        variant="secondary"
                        key={option.value}
                        className="rounded-sm px-1 font-normal"
                      >
                        {option.label}
                      </Badge>
                    ))
                )}
              </div>
            </>
          )}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-2" align="start">
        <div className="space-y-2">
          <h4 className="text-sm font-medium px-1">{title}</h4>
          <div className="space-y-1">
            {options.map((option) => {
              const isSelected = selectedValues.has(option.value);
              return (
                <label 
                  key={option.value}
                  className="flex items-center space-x-2 p-1 rounded hover:bg-accent cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => {
                      const newValues = new Set(selectedValues);
                      if (isSelected) {
                        newValues.delete(option.value);
                      } else {
                        newValues.add(option.value);
                      }
                      column?.setFilterValue(newValues.size ? Array.from(newValues) : undefined);
                    }}
                    className="h-4 w-4 accent-primary"
                  />
                  <span className="text-sm">{option.label}</span>
                  {option.icon && (
                    <option.icon className="h-4 w-4 text-muted-foreground" />
                  )}
                  {facets?.get(option.value) && (
                    <span className="ml-auto text-xs text-muted-foreground">
                      {facets.get(option.value)}
                    </span>
                  )}
                </label>
              );
            })}
          </div>
          {selectedValues.size > 0 && (
            <button
              onClick={() => column?.setFilterValue(undefined)}
              className="w-full text-xs text-primary hover:underline text-center pt-1"
            >
              Clear filters
            </button>
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}
