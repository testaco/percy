export interface BoardData {
  last_updated: string;
  test_results: Array<{
    test_id: string;
    timestamp: string;
    model_name: string;
    provider: string;
    license_class: string;
    parameters: {
      temperature: number;
      used_cot: boolean;
      used_rag: boolean;
      context_window: number;
      param_count: number | null;
    };
    results: {
      total_questions: number;
      correct_answers: number;
      score_percentage: number;
      passed: boolean;
      margin_to_pass: number;
    };
    performance: {
      duration_seconds: number;
      tokens_per_second: number;
      total_tokens: number;
      prompt_tokens: number;
      completion_tokens: number;
    };
    costs: {
      total_cost: number;
      prompt_cost: number;
      completion_cost: number;
      cost_per_question: number;
    };
  }>;
}
