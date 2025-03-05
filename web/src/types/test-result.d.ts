/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

export interface TestResult {
  model: string;
  provider_id: string;
  organization_id: string;
  model_id: string;
  test_id: string;
  timestamp: string;
  questions: TestResultQuestionAnswer[];
  total_questions: number;
  correct_answers: number;
  score_percentage: number;
  duration_seconds: number;
  used_cot: boolean;
  used_rag: boolean;
  temperature: number;
  token_usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
    [k: string]: unknown;
  };
  pool_name: string;
  pool_id: string;
  [k: string]: unknown;
}
export interface TestResultQuestionAnswer {
  question_id: string;
  model_answer: string;
  correct_answer: string;
  is_correct: boolean;
  has_image: boolean;
  image_path?: string | null;
  rag_context?: string[] | null;
  token_usage: {
    input_tokens: number;
    output_tokens: number;
    total_tokens: number;
    input_token_details: {
      audio?: number;
      cache_read?: number;
      [k: string]: unknown;
    };
    output_token_details: {
      audio?: number;
      reasoning?: number;
      [k: string]: unknown;
    };
    [k: string]: unknown;
  };
  [k: string]: unknown;
}
