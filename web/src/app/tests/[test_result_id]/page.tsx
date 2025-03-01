import { promises as fs } from 'fs'
import path from 'path'
import { DataTable } from "./data-table"
import { columns } from "./columns"
import { TestResult } from "@/types/test-result"
import { AmateurRadioTest } from "@/types/test"
import Image from "next/image"

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
      
      <DataTable 
        columns={columns} 
        data={testResult.questions} 
      />
      
      {questionsWithDetails.map((question) => (
        <dialog key={question.question_id} id={question.question_id} className="modal">
          <div className="modal-box max-w-4xl">
            <h3 className="font-bold text-lg mb-4">{question.question}</h3>
            
            {question.has_image && (
              <div className="relative h-64 mb-4">
                <Image
                  src={`/data/question_pools/${testResult.pool_name}/${question.question_id}.jpg`}
                  alt="Question diagram"
                  fill
                  className="object-contain"
                />
              </div>
            )}
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
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
              <div className="prose mb-4 p-4 bg-blue-50 rounded-md">
                <h4 className="text-blue-800">RAG Context</h4>
                <ul>
                  {question.rag_context.map((ctx, i) => (
                    <li key={i}>{ctx}</li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="grid grid-cols-2 gap-4 mt-4">
              <div>
                <p className="font-semibold">Input Tokens:</p>
                <p>{question.token_usage.input_tokens}</p>
              </div>
              <div>
                <p className="font-semibold">Output Tokens:</p>
                <p>{question.token_usage.output_tokens}</p>
              </div>
            </div>
            
            <div className="modal-action">
              <form method="dialog">
                <button className="btn">Close</button>
              </form>
            </div>
          </div>
        </dialog>
      ))}
    </div>
  )
}
