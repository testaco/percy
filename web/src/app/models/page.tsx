import { DataTable } from "./data-table"
import { columns } from "./columns"
import { LLMStats } from "@/types/llmstats";

async function getCombinedData() {
  try {
    const [llmstats, board] = await Promise.all([
      import('@/../../public/data/llmstats.json').then(m => m.default),
      import('@/../../public/data/board.json').then(m => m.default)
    ]);

    return Object.entries(llmstats).map(([id, model]) => ({
      id,
      ...model,
      organization: model.providers[0]?.provider_name || 'Unknown',
      passes_technician: board.test_results.some(tr => 
        tr.model_name === id && 
        tr.test_id === 'technician-2022-2026' &&
        tr.score_percentage === 100
      ),
      passes_general: board.test_results.some(tr => 
        tr.model_name === id && 
        tr.test_id === 'general-2023-2027' &&
        tr.score_percentage === 100
      ),
      passes_extra: board.test_results.some(tr => 
        tr.model_name === id && 
        tr.test_id === 'extra-2024-2028' &&
        tr.score_percentage === 100
      )
    }));
  } catch (error) {
    console.error("Error loading data:", error);
    return [];
  }
}

export default async function ModelsPage() {
  const data = await getCombinedData();

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-6">LLM Leaderboard</h1>
      <p className="text-lg text-muted-foreground mb-8">
        Browse all models tested in the Percy amateur radio evaluation framework.
      </p>
      <DataTable columns={columns} data={data} />
    </div>
  )
}
