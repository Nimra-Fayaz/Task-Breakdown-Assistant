export interface GuideStep {
  id: number
  task_id: number
  step_number: number
  title: string
  description: string
  detailed_instructions: string | null
  estimated_time: number | null
  dependencies: number[] | null
  resources: string[] | null
  code_snippets: string[] | null
  tips: string | null
  warnings: string | null
  verification_steps: string | null
  created_at: string
}

export interface TaskWithGuide {
  id: number
  title: string | null
  description: string
  complexity_score: number
  estimated_total_time: number | null
  created_at: string
  updated_at: string | null
  guide_steps: GuideStep[]
}

export interface Rating {
  id: number
  task_id: number
  rating: number
  comment: string | null
  created_at: string
}

export interface RatingStats {
  task_id: number
  average_rating: number
  total_ratings: number
  ratings: Rating[]
}

