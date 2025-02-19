import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// This would normally come from your data source
const mockData = {
  models: [
    {
      name: "GPT-4",
      provider: "OpenAI",
      license_class: "Extra",
      score: 85.7,
      pass_rate: "92%",
      avg_time: "45s"
    },
    {
      name: "Claude 2",
      provider: "Anthropic", 
      license_class: "General",
      score: 82.3,
      pass_rate: "88%",
      avg_time: "52s"
    },
    {
      name: "Llama 2",
      provider: "Meta",
      license_class: "Technician",
      score: 78.9,
      pass_rate: "84%",
      avg_time: "48s"
    }
  ]
}

export default function LeaderboardPage() {
  return (
    <div className="py-6 space-y-8">
      <div className="space-y-4">
        <h1 className="text-3xl font-bold tracking-tight">LLM Leaderboard</h1>
        <p className="text-muted-foreground">
          Analysis and comparison of AI models across amateur radio license exams
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Model Performance</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Model</TableHead>
                <TableHead>Provider</TableHead>
                <TableHead>License Class</TableHead>
                <TableHead className="text-right">Score</TableHead>
                <TableHead className="text-right">Pass Rate</TableHead>
                <TableHead className="text-right">Avg. Time</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockData.models.map((model, index) => (
                <TableRow key={index}>
                  <TableCell className="font-medium">{model.name}</TableCell>
                  <TableCell>{model.provider}</TableCell>
                  <TableCell>{model.license_class}</TableCell>
                  <TableCell className="text-right">{model.score}%</TableCell>
                  <TableCell className="text-right">{model.pass_rate}</TableCell>
                  <TableCell className="text-right">{model.avg_time}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
