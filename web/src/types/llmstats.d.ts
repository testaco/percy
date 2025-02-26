export interface LLMStats {
  [modelId: string]: {
    canonical_model_id: string | null;
    fine_tuned_from_model_id: string | null;
    name: string;
    description: string;
    release_date: string;
    input_context_size: number;
    output_context_size: number;
    license: string;
    multimodal: boolean;
    web_hydrated: boolean;
    knowledge_cutoff: string | null;
    api_ref_link: string;
    playground_link: string | null;
    paper_link: string | null;
    scorecard_blog_link: string | null;
    repo_link: string | null;
    weights_link: string | null;
    param_count: number | null;
    training_tokens: number | null;
    qualitative_metrics?: Array<{
      dataset_name: string;
      score: number;
      is_self_reported: boolean;
      analysis_method: string;
      date_recorded: string;
      source_link: string;
    }>;
    providers: Array<{
      provider_name: string;
      provider_website: string;
      price_per_input_token: number;
      price_per_output_token: number;
      throughput: number;
      latency: number;
      updated_at: string;
    }>;
  };
}
