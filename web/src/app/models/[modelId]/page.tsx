import { notFound } from 'next/navigation';
import Link from 'next/link';
import { Card, CardHeader, CardContent, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { CheckCircledIcon, CrossCircledIcon } from '@radix-ui/react-icons';
import { LLMStats } from '@/types/llmstats';
import { BoardData } from '@/types/board';

export async function generateStaticParams() {
  const llmstats: LLMStats = await import('@/../../public/data/llmstats.json').then(m => m.default);
  return Object.keys(llmstats).map((modelId) => ({ modelId }));
}

async function getModelData(modelId: string) {
  try {
    const llmstats: LLMStats = await import('@/../../public/data/llmstats.json').then(m => m.default);
    const board: BoardData = await import('@/../../public/data/board.json').then(m => m.default);
    
    const modelData = llmstats[modelId];
    if (!modelData) return null;
    
    const modelTests = board.test_results.filter(t => t.model_name === modelId);

    return { modelData, modelTests };
  } catch (error) {
    console.error("Error loading model data:", error);
    return null;
  }
}

export default async function ModelPage({ params }: { params: Promise<{ modelId: string }> }) {
  const { modelId } = await params;
  const data = await getModelData(modelId);
  
  if (!data) {
    notFound();
  }
  
  const { modelData, modelTests } = data;

  // Aggregate test results by license class
  const testsByLicense = modelTests.reduce((acc, test) => {
    if (!acc[test.license_class]) {
      acc[test.license_class] = {
        total: 0,
        passed: 0,
        avgScore: 0,
        totalScore: 0
      };
    }
    
    acc[test.license_class].total += 1;
    if (test.results.passed) acc[test.license_class].passed += 1;
    acc[test.license_class].totalScore += test.results.score_percentage;
    acc[test.license_class].avgScore = acc[test.license_class].totalScore / acc[test.license_class].total;
    
    return acc;
  }, {} as Record<string, { total: number; passed: number; avgScore: number; totalScore: number }>);

  // Format date
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-6">
        <Link href="/models" className="text-primary hover:underline mb-4 inline-block">
          ← Back to Models
        </Link>
        <h1 className="text-4xl font-bold mb-2">{modelData.name}</h1>
        <p className="text-muted-foreground mb-4">{modelData.description}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <Card>
          <CardHeader>
            <CardTitle>Model Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-2">
              <div className="text-muted-foreground">Released</div>
              <div>{formatDate(modelData.release_date)}</div>
              
              <div className="text-muted-foreground">License</div>
              <div>{modelData.license}</div>
              
              <div className="text-muted-foreground">Parameters</div>
              <div>{modelData.param_count ? `${modelData.param_count.toLocaleString()} billion` : 'Unknown'}</div>
              
              <div className="text-muted-foreground">Training Tokens</div>
              <div>{modelData.training_tokens ? `${(modelData.training_tokens / 1e9).toFixed(1)}B` : 'Unknown'}</div>
              
              <div className="text-muted-foreground">Knowledge Cutoff</div>
              <div>{modelData.knowledge_cutoff || 'Unknown'}</div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Capabilities</h3>
              <div className="flex flex-wrap gap-2">
                <Badge variant="outline">
                  {modelData.input_context_size.toLocaleString()} token context
                </Badge>
                {modelData.multimodal && <Badge>Multimodal</Badge>}
                {modelData.web_hydrated && <Badge>Web Access</Badge>}
              </div>
            </div>
            
            <div>
              <h3 className="font-semibold mb-2">Resources</h3>
              <div className="space-y-1">
                {modelData.api_ref_link && (
                  <a href={modelData.api_ref_link} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline block">
                    API Documentation
                  </a>
                )}
                {modelData.paper_link && (
                  <a href={modelData.paper_link} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline block">
                    Research Paper
                  </a>
                )}
                {modelData.playground_link && (
                  <a href={modelData.playground_link} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline block">
                    Try in Playground
                  </a>
                )}
                {modelData.repo_link && (
                  <a href={modelData.repo_link} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline block">
                    Source Repository
                  </a>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Amateur Radio Test Performance</CardTitle>
          </CardHeader>
          <CardContent>
            {Object.keys(testsByLicense).length > 0 ? (
              <div className="space-y-6">
                {['technician', 'general', 'extra'].map((license) => {
                  const licenseData = testsByLicense[license];
                  const displayName = license.charAt(0).toUpperCase() + license.slice(1);
                  
                  return licenseData ? (
                    <div key={license} className="border rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <h3 className="font-medium">{displayName}</h3>
                        <div className="flex items-center">
                          {licenseData.passed > 0 ? (
                            <Badge className="bg-green-100 text-green-800">
                              {licenseData.passed}/{licenseData.total} Passed
                            </Badge>
                          ) : (
                            <Badge className="bg-red-100 text-red-800">
                              0/{licenseData.total} Passed
                            </Badge>
                          )}
                        </div>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        Average Score: {licenseData.avgScore.toFixed(1)}%
                      </div>
                    </div>
                  ) : (
                    <div key={license} className="border rounded-lg p-4">
                      <div className="flex justify-between items-center">
                        <h3 className="font-medium">{displayName}</h3>
                        <Badge variant="outline">No Tests</Badge>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                No test data available for this model
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {modelData.qualitative_metrics && modelData.qualitative_metrics.length > 0 && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Benchmark Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {modelData.qualitative_metrics.map((metric) => (
                <div key={metric.dataset_name} className="border rounded-lg p-4">
                  <div className="font-medium mb-1">{metric.dataset_name}</div>
                  <div className="text-2xl font-bold">{metric.score.toFixed(1)}</div>
                  <div className="text-xs text-muted-foreground mt-1">
                    {metric.is_self_reported ? 'Self-reported' : 'Independent'} • {formatDate(metric.date_recorded)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Providers</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Provider</TableHead>
                <TableHead className="text-right">Input Cost</TableHead>
                <TableHead className="text-right">Output Cost</TableHead>
                <TableHead className="text-right">Throughput</TableHead>
                <TableHead className="text-right">Latency</TableHead>
                <TableHead>Last Updated</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {modelData.providers.map((provider) => (
                <TableRow key={provider.provider_name}>
                  <TableCell>
                    <a 
                      href={provider.provider_website} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="hover:underline"
                    >
                      {provider.provider_name}
                    </a>
                  </TableCell>
                  <TableCell className="text-right">${provider.price_per_input_token.toFixed(6)}/token</TableCell>
                  <TableCell className="text-right">${provider.price_per_output_token.toFixed(6)}/token</TableCell>
                  <TableCell className="text-right">{provider.throughput.toLocaleString()} tokens/sec</TableCell>
                  <TableCell className="text-right">{provider.latency.toFixed(2)}ms</TableCell>
                  <TableCell>{formatDate(provider.updated_at)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      {modelTests.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recent Test Runs</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Test ID</TableHead>
                  <TableHead>Date</TableHead>
                  <TableHead>License</TableHead>
                  <TableHead>Features</TableHead>
                  <TableHead className="text-right">Score</TableHead>
                  <TableHead className="text-right">Cost</TableHead>
                  <TableHead>Result</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {modelTests.slice(0, 10).map((test) => (
                  <TableRow key={test.test_id}>
                    <TableCell>
                      <Link href={`/tests/${test.test_result_id}`} className="text-primary hover:underline">
                        {test.test_id}
                      </Link>
                    </TableCell>
                    <TableCell>{formatDate(test.timestamp)}</TableCell>
                    <TableCell className="capitalize">{test.license_class}</TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        {test.parameters.used_cot && <Badge variant="outline">CoT</Badge>}
                        {test.parameters.used_rag && <Badge variant="outline">RAG</Badge>}
                      </div>
                    </TableCell>
                    <TableCell className="text-right">{test.results.score_percentage.toFixed(1)}%</TableCell>
                    <TableCell className="text-right">${test.costs.total_cost.toFixed(2)}</TableCell>
                    <TableCell>
                      {test.results.passed ? (
                        <Badge className="bg-green-100 text-green-800 flex items-center gap-1">
                          <CheckCircledIcon className="h-4 w-4" />
                          Passed
                        </Badge>
                      ) : (
                        <Badge className="bg-red-100 text-red-800 flex items-center gap-1">
                          <CrossCircledIcon className="h-4 w-4" />
                          Failed
                        </Badge>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            {modelTests.length > 10 && (
              <div className="mt-4 text-center">
                <Link href={`/tests?model=${modelId}`} className="text-primary hover:underline">
                  View all {modelTests.length} test runs
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
