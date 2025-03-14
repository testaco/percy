import { DataTable } from "./data-table"
import { columns } from "./columns"

async function getCombinedData() {
  try {
    const [llmstats, board] = await Promise.all([
      import('@/../../public/data/llmstats.json').then(m => m.default),
      import('@/../../public/data/board.json').then(m => m.default)
    ]);

    // Get all model IDs that have any evaluations
    const modelIdsWithEvaluations = new Set(
      board.test_results.map(tr => tr.model_id)
    );
    
    // Only return models that have evaluations
    return Object.entries(llmstats)
      .filter(([id]) => modelIdsWithEvaluations.has(id))
      .map(([id, model]) => ({
        id,
        ...model,
        organization: model.providers[0]?.provider_id || 'Unknown',
        passes_technician: board.test_results.some(tr => 
          tr.model_id === id && 
          tr.license_class === 'technician' &&
          tr.results.passed
        ),
        passes_general: board.test_results.some(tr => 
          tr.model_id === id && 
          tr.license_class === 'general' &&
          tr.results.passed
        ),
        passes_extra: board.test_results.some(tr => 
          tr.model_id === id && 
          tr.license_class === 'extra' &&
          tr.results.passed
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
