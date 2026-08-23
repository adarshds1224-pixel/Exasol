// TODO: move API_BASE_URL to an environment variable.
export const API_BASE_URL = 'http://localhost:8000'

export interface BlindSpot {
  department: string
  severity: 'HIGH' | 'MEDIUM' | 'LOW'
  resolution_rate: number
  pending_gt_3yr: number
  pending_gt_1yr_pct: number
  indicator_summary: string
}

export interface BlindSpotsResponse {
  blind_spots: BlindSpot[]
}

export interface YearlyTrendItem {
  year: number
  received: number
  disposed: number
  resolution_rate: number
}

export interface MonthlyPredictionItem {
  month: string
  predicted: number
  actual: number
  pct_change: number
}

export interface DashboardData {
  active_blind_spots: number
  high_severity_count: number
  cases_analyzed: number
  top_blind_spots: BlindSpot[]
  yearly_trend: YearlyTrendItem[]
  monthly_prediction: MonthlyPredictionItem[]
}

export interface EvidenceSource {
  source_name: string
  type: string
  origin: string
  verified: boolean
}

export interface EvidenceResponse {
  evidence_sources: EvidenceSource[]
}

export interface ImpactYearData {
  received: number
  disposed: number
  resolution_rate: number
}

export interface ImpactTrackerData {
  before_year: number
  after_year: number
  before: ImpactYearData
  after: ImpactYearData
  note: string
}

export interface Hypothesis {
  text: string
  confidence_pct: number
  label: string
}

export interface InvestigationBrief {
  problem: string
  observed_contradiction: string
  evidence: string
  uncertainty: string
  affected_groups: string
  additional_evidence_required: string
  recommended_steps: string
}

export interface Investigation extends BlindSpot {
  hypotheses: Hypothesis[]
  evidence_gaps: string[]
  investigation_brief: InvestigationBrief
}

export interface ReviewResponse {
  department: string
  action: 'accept' | 'modify' | 'reject'
  status: string
  message: string
}

async function parseError(response: Response, context: string): Promise<never> {
  let detail = ''
  try {
    const data = await response.json()
    detail = data?.detail ?? data?.message ?? ''
  } catch {
    detail = ''
  }

  const suffix = detail ? `: ${detail}` : ''
  throw new Error(`${context} failed (${response.status} ${response.statusText})${suffix}`)
}

export async function getDashboard(): Promise<DashboardData> {
  const response = await fetch(`${API_BASE_URL}/api/dashboard`)
  if (!response.ok) {
    await parseError(response, 'Dashboard request')
  }
  return (await response.json()) as DashboardData
}

export async function getBlindSpots(): Promise<BlindSpotsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/blind-spots`)
  if (!response.ok) {
    await parseError(response, 'Blind spots request')
  }
  return (await response.json()) as BlindSpotsResponse
}

export async function getEvidence(): Promise<EvidenceResponse> {
  const response = await fetch(`${API_BASE_URL}/api/evidence`)
  if (!response.ok) {
    await parseError(response, 'Evidence request')
  }
  return (await response.json()) as EvidenceResponse
}

export async function getImpactTracker(): Promise<ImpactTrackerData> {
  const response = await fetch(`${API_BASE_URL}/api/impact-tracker`)
  if (!response.ok) {
    await parseError(response, 'Impact tracker request')
  }
  return (await response.json()) as ImpactTrackerData
}

export async function getInvestigation(department: string): Promise<Investigation> {
  const encodedDepartment = encodeURIComponent(department)
  const response = await fetch(`${API_BASE_URL}/api/investigations/${encodedDepartment}`)
  if (!response.ok) {
    await parseError(response, 'Investigation request')
  }
  return (await response.json()) as Investigation
}

export async function submitReview(
  department: string,
  action: 'accept' | 'modify' | 'reject',
): Promise<ReviewResponse> {
  const encodedDepartment = encodeURIComponent(department)
  const response = await fetch(`${API_BASE_URL}/api/investigations/${encodedDepartment}/review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ action }),
  })

  if (!response.ok) {
    await parseError(response, 'Review submission')
  }

  return (await response.json()) as ReviewResponse
}

async function apiRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers ?? {}),
    },
  })

  if (!response.ok) {
    await parseError(response, 'API request')
  }

  return (await response.json()) as T
}

export const api = {
  get: <T>(path: string) => apiRequest<T>(path),
  post: <T, B = unknown>(path: string, body: B) =>
    apiRequest<T>(path, {
      method: 'POST',
      body: JSON.stringify(body),
    }),
}
