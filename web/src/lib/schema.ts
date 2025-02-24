import { z } from "zod";

export const BoardSchema = z.object({
  batch_name: z.string(),
  model_providers: z.array(z.string()),
  parameters: z.object({
    temperature: z.array(z.number()),
    use_cot: z.array(z.boolean()),
    use_rag: z.array(z.boolean())
  }),
  last_updated: z.string().datetime()
});
