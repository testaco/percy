/* eslint-disable */
/**
 * This file was automatically generated by json-schema-to-typescript.
 * DO NOT MODIFY IT BY HAND. Instead, modify the source JSONSchema file,
 * and run json-schema-to-typescript to regenerate this file.
 */

/**
 * Schema for the LLM testing leaderboard data
 */
export interface BoardData {
  /**
   * Timestamp of when the leaderboard was last updated
   */
  last_updated?: string;
  /**
   * Array of individual test results from LLM evaluations
   */
  test_results: {
    /**
     * Unique identifier for the test attempt
     */
    test_id: string;
    /**
     * Filename of the test result without path or extension
     */
    test_result_id: string;
    /**
     * When the test was conducted
     */
    timestamp: string;
    /**
     * The LLM model used
     */
    model_id: string;
    /**
     * Service provider of the LLM (e.g., openai, anthropic)
     */
    provider_id: string;
    /**
     * Amateur radio license class being tested (Technician, General, Extra)
     */
    license_class: string;
    /**
     * Model configuration and capabilities
     */
    parameters: {
      /**
       * Sampling temperature used for generation
       */
      temperature?: number;
      /**
       * Whether Chain-of-Thought reasoning was enabled
       */
      used_cot?: boolean;
      /**
       * Whether Retrieval Augmented Generation was used
       */
      used_rag?: boolean;
      /**
       * Maximum input context length in tokens
       */
      context_window?: number | null;
      /**
       * Number of parameters in the model (billions)
       */
      param_count?: number | null;
      [k: string]: unknown;
    };
    /**
     * Test performance metrics
     */
    results: {
      /**
       * Total number of questions in the test
       */
      total_questions: number;
      /**
       * Number of questions answered correctly
       */
      correct_answers: number;
      /**
       * Percentage of correct answers
       */
      score_percentage: number;
      /**
       * Whether the score met passing threshold
       */
      passed: boolean;
      /**
       * Difference between score and passing threshold
       */
      margin_to_pass: number;
      [k: string]: unknown;
    };
    /**
     * Runtime performance metrics
     */
    performance: {
      /**
       * Total time taken to complete the test
       */
      duration_seconds: number;
      /**
       * Average token processing speed
       */
      tokens_per_second: number;
      /**
       * Total tokens used across all questions
       */
      total_tokens: number;
      /**
       * Tokens used in input prompts
       */
      prompt_tokens: number;
      /**
       * Tokens generated in responses
       */
      completion_tokens: number;
      [k: string]: unknown;
    };
    /**
     * Cost analysis in USD
     */
    costs: {
      /**
       * Total cost for the entire test
       */
      total_cost: number;
      /**
       * Cost of input tokens
       */
      prompt_cost: number;
      /**
       * Cost of output tokens
       */
      completion_cost: number;
      /**
       * Average cost per question
       */
      cost_per_question: number;
      [k: string]: unknown;
    };
    [k: string]: unknown;
  }[];
  [k: string]: unknown;
}
