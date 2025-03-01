import { promises as fs } from 'fs'
import path from 'path'
import { DataTable } from "./data-table"
import { columns } from "./columns"
import { TestResult } from "@/types/test-result"
import { AmateurRadioTest } from "@/types/test"
import Image from "next/image"

export async function generateStaticParams() {
  const evaluationsDir = path.join(process.cwd(), 'public/data/evaluations')
  const files = await fs.readdir(evaluationsDir)
  
  return files
    .filter(file => file.endsWith('.json'))
    .map(file => ({
      test_result_id: file.replace(/\.json$/, '')
    }))
}

export default async function TestDetailPage({ params }: { 
  params: Promise<{ test_result_id: string }>
}) {
  const { test_result_id } = await params
  
  // Load test result
  const testResultPath = path.join(process.cwd(), 'public/data/evaluations', `${test_result_id}.json`)
  const testResult: TestResult = JSON.parse(await fs.readFile(testResultPath, 'utf8'))
  
  // Load original test
  const testPath = path.join(process.cwd(), 'public/data/tests', `${testResult.test_id}.json`)
  const originalTest: AmateurRadioTest = JSON.parse(await fs.readFile(testPath, 'utf8'))
  
  // Merge data for modal
  const questionsWithDetails = testResult.questions.map(q => ({
    ...q,
    ...originalTest.questions.find(tq => tq.id === q.question_id)
  }))

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-2xl font-bold mb-6">
        Test Result: {test_result_id}
      </h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-2">Model</h2>
          <p>{testResult.provider}/{testResult.model_name}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-2">Score</h2>
          <p className={testResult.score_percentage >= 74 ? "text-green-600 font-bold" : "text-red-600 font-bold"}>
            {testResult.score_percentage.toFixed(1)}% ({testResult.correct_answers}/{testResult.total_questions})
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-medium mb-2">License Class</h2>
          <p className="capitalize">{testResult.pool_id === "T" ? "Technician" : testResult.pool_id === "G" ? "General" : "Extra"}</p>
        </div>
      </div>
      
      <div className="space-y-4">
        <DataTable 
          columns={columns} 
          data={testResult.questions} 
        />
      </div>
      
      {questionsWithDetails.map((question) => (
        <dialog key={question.question_id} id={question.question_id} className="modal">
          <div className="modal-box max-w-4xl border-2 border-gray-200 shadow-xl rounded-lg p-6 relative">
            {/* Add close button at top right */}
            <form method="dialog" className="absolute right-4 top-4">
              <button className="btn btn-sm btn-circle btn-ghost text-lg">
                ×
              </button>
            </form>
            
            <div className="pt-8"> {/* Add padding to offset close button */}
              <h3 className="font-bold text-2xl mb-6 text-primary">{question.question}</h3>
              
              {question.has_image && (
                <div className="relative h-64 mb-6 bg-gray-50 rounded-xl overflow-hidden">
                  <Image
                    src={`/data/question_pools/${question.image_path}`}
                    alt="Question diagram"
                    fill
                    className="object-contain p-4"
                  />
                </div>
              )}
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {question.answers?.map((answer) => (
                  <div 
                    key={answer.option} 
                    className={`p-3 rounded-md ${
                      answer.option === question.correct_answer 
                        ? "bg-green-100 border border-green-300" 
                        : answer.option === question.model_answer && answer.option !== question.correct_answer
                        ? "bg-red-100 border border-red-300"
                        : "bg-gray-50 border border-gray-200"
                    }`}
                  >
                    <span className="font-medium">{answer.option}:</span> {answer.text}
                  </div>
                ))}
              </div>
              
              {question.rag_context && (
                <div className="prose mb-6 p-4 bg-blue-50 rounded-md border border-blue-200">
                  <h4 className="text-blue-800 font-semibold mb-3">RAG Context</h4>
                  <ul className="space-y-2">
                    {question.rag_context.map((ctx, i) => (
                      <li key={i} className="text-sm text-blue-700">{ctx}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-4 mt-6 bg-gray-50 p-4 rounded-lg">
                <div className="space-y-1">
                  <p className="font-semibold text-gray-600">Input Tokens</p>
                  <p className="text-lg font-mono">{question.token_usage.input_tokens}</p>
                </div>
                <div className="space-y-1">
                  <p className="font-semibold text-gray-600">Output Tokens</p>
                  <p className="text-lg font-mono">{question.token_usage.output_tokens}</p>
                </div>
              </div>
            </div>
          </div>
          
          {/* Click outside to close */}
          <form method="dialog" className="modal-backdrop">
            <button>close</button>
          </form>
        </dialog>
      ))}
    </div>
  )
}
