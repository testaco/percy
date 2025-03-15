import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function Home() {
  return (
    <>
      <div className="w-full bg-accent py-16">
        <div className="container mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">Welcome to Percy</h1>
          <p className="text-xl text-accent-foreground max-w-2xl mx-auto">
            Platform for Evaluating Radio Compliance in Language Models
          </p>
        </div>
      </div>
      
      <div className="container mx-auto py-12">
        <div className="max-w-4xl mx-auto">

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
    </>
  );
}
