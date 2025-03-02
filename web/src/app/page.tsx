import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function Home() {
  return (
    <div className="container mx-auto pt-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">Welcome to Percy</h1>
        <p className="text-lg text-muted-foreground mb-8">
          Platform for Evaluating Radio Compliance in Language Models
        </p>

        <div className="grid gap-4 md:grid-cols-2">
          <Card className="p-6">
            <h2 className="text-2xl font-semibold mb-2">Leaderboard</h2>
            <p className="text-muted-foreground mb-4">
              View performance rankings of various LLMs on amateur radio licensing exams
            </p>
            <Button asChild>
              <Link href="/models">Browse Models</Link>
            </Button>
          </Card>

          <Card className="p-6">
            <h2 className="text-2xl font-semibold mb-2">Handbook</h2>
            <p className="text-muted-foreground mb-4">
              Study materials and curriculum for amateur radio licensing
            </p>
            <Button asChild variant="outline">
              <Link href="/handbook">View Handbook</Link>
            </Button>
          </Card>
        </div>
      </div>
    </div>
  );
}
