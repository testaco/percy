import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";

export default function Home() {
  return (
    <>
    <main className="space-y-10">
      {/* Hero Section */}
      <section>
        <Card>
          <CardHeader>
            <CardTitle className="text-3xl">Percy: Amateur Radio Test Bot</CardTitle>
            <CardDescription>
              Evaluate LLM performance on official Amateur Radio exams. Open-book and open-source—see how different models stack up!
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-4">
            <p>
              We’ve tested large and small models (with and without RAG, CoT, 
              or multimodal inputs) to find out what truly passes. Explore 
              the leaderboard for best scores, or open our handbook for 
              study references!
            </p>
          </CardContent>
          <CardFooter className="flex gap-4">
            <Button><Link href="/models">View Leaderboard</Link></Button>
            <Button variant="secondary"><Link href="/handbook">View Handbook</Link></Button>
          </CardFooter>
        </Card>
      </section>

      {/* Model Group Highlights */}
      <section className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          {/* Best Commercial Models */}
          <Card>
            <CardHeader>
              <CardTitle>1. Best Commercial</CardTitle>
              <CardDescription>(OpenAI, Anthropic, etc.)</CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                These top-tier APIs boast high accuracy and advanced reasoning. 
                They generally pass all license classes with robust prompts but 
                come at a higher usage cost.
              </p>
            </CardContent>
          </Card>

          {/* Models < 7B Parameters */}
          <Card>
            <CardHeader>
              <CardTitle>2. Under 7B Params</CardTitle>
              <CardDescription>Small & Efficient</CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Surprisingly capable with retrieval-augmented generation (RAG). 
                Some can pass the Technician test reliably, making them very 
                cost-effective solutions.
              </p>
            </CardContent>
          </Card>

          {/* Models 7B–70B Parameters */}
          <Card>
            <CardHeader>
              <CardTitle>3. 7B–70B Params</CardTitle>
              <CardDescription>Mid-Range All-Stars</CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                Striking a balance between cost and performance, these models 
                often pass Technician or General level. With CoT or RAG, some 
                can tackle Extra with decent success.
              </p>
            </CardContent>
          </Card>

          {/* Models > 70B Parameters */}
          <Card>
            <CardHeader>
              <CardTitle>4. Over 70B Params</CardTitle>
              <CardDescription>Large & In Charge</CardDescription>
            </CardHeader>
            <CardContent>
              <p>
                High-parameter models excel at tough questions and advanced 
                calculations, often passing all license classes. 
                Best-in-class accuracy, but high compute costs.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Interesting Fact / Additional Info */}
      <section>
        <Card>
          <CardHeader>
            <CardTitle>Built With AI Assistance</CardTitle>
            <CardDescription>Code Generation & Automation</CardDescription>
          </CardHeader>
          <CardContent>
            <p>
              Over 99% of Percy’s code was created with AI (using Cursor, Aider, 
              and LLM-based tools) in a Python framework and Next.js app. This 
              helps us quickly iterate and gather new test results for the 
              Amateur Radio exams.
            </p>
          </CardContent>
        </Card>
      </section>
    </main>
    </>
  );
}
