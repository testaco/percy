import Link from 'next/link';
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { LLMStats } from '@/types/llmstats';

async function getModelsData() {
  try {
    const llmstats: LLMStats = await import('@/../../public/data/llmstats.json').then(m => m.default);
    return llmstats;
  } catch (error) {
    console.error("Error loading models data:", error);
    return {};
  }
}

export default async function ModelsPage() {
  const llmstats = await getModelsData();
  
  // Group models by provider
  const modelsByProvider: Record<string, Array<{ id: string; model: LLMStats[string] }>> = {};
  
  Object.entries(llmstats).forEach(([id, model]) => {
    // Use the first provider as the primary provider for grouping
    const primaryProvider = model.providers[0]?.provider_name || 'Unknown';
    
    if (!modelsByProvider[primaryProvider]) {
      modelsByProvider[primaryProvider] = [];
    }
    
    modelsByProvider[primaryProvider].push({ id, model });
  });

  return (
    <div className="container mx-auto py-8 px-4">
      <h1 className="text-4xl font-bold mb-6">LLM Models</h1>
      <p className="text-lg text-muted-foreground mb-8">
        Browse all models tested in the Percy amateur radio evaluation framework.
      </p>

      {Object.entries(modelsByProvider).map(([provider, models]) => (
        <div key={provider} className="mb-10">
          <h2 className="text-2xl font-bold mb-4">{provider}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {models.map(({ id, model }) => (
              <Link key={id} href={`/models/${id}`}>
                <Card className="h-full hover:shadow-md transition-shadow">
                  <CardHeader>
                    <CardTitle>{model.name}</CardTitle>
                    <CardDescription>
                      {model.release_date && (
                        <span>Released: {new Date(model.release_date).toLocaleDateString()}</span>
                      )}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                      {model.description}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      <Badge variant="outline">
                        {model.input_context_size.toLocaleString()} tokens
                      </Badge>
                      {model.multimodal && <Badge>Multimodal</Badge>}
                      {model.web_hydrated && <Badge>Web Access</Badge>}
                      {model.param_count && (
                        <Badge variant="outline">{model.param_count}B params</Badge>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
