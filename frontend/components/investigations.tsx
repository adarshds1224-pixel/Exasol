'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { Square, AlertTriangle, Check, Pencil, X, Loader2 } from 'lucide-react'
import { Card, SectionTitle, SeverityBadge } from '@/components/civic-ui'
import { getInvestigation, submitReview, type Investigation } from '@/lib/api'

function ConfidenceBar({ value }: { value: number }) {
  return (
    <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
      <div className="h-full rounded-full bg-primary" style={{ width: `${value}%` }} />
    </div>
  )
}

export function Investigations() {
  const searchParams = useSearchParams()
  const department = searchParams.get('department')
  const [investigation, setInvestigation] = useState<Investigation | null>(null)
  const [decision, setDecision] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadInvestigation() {
      if (!department) {
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError(null)
        setInvestigation(await getInvestigation(department))
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unable to load investigation')
      } finally {
        setLoading(false)
      }
    }

    loadInvestigation()
  }, [department])

  function retryLoadInvestigation() {
    if (!department) return

    setLoading(true)
    setError(null)
    getInvestigation(department)
      .then(setInvestigation)
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Unable to load investigation')
      })
      .finally(() => setLoading(false))
  }

  async function submitDecision(nextDecision: 'accept' | 'modify' | 'reject') {
    if (!department) return
    try {
      const response = await submitReview(department, nextDecision)
      setDecision(response.message)
    } catch (err) {
      setDecision(err instanceof Error ? err.message : 'Decision failed')
    }
  }

  if (!department) {
    return (
      <Card>
        <p className="text-sm text-foreground">Select a blind spot from the Blind Spots page to view its investigation</p>
      </Card>
    )
  }

  if (loading) {
    return (
      <Card className="flex items-center gap-3">
        <Loader2 className="size-5 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">Loading investigation...</p>
      </Card>
    )
  }

  if (error || !investigation) {
    return (
      <Card className="border-status-red/30 bg-status-red-bg">
        <p className="font-semibold text-status-red">Investigation unavailable</p>
        <p className="mt-1 text-sm text-foreground">{error ?? 'No investigation data returned.'}</p>
        <button
          type="button"
          onClick={retryLoadInvestigation}
          className="mt-4 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
        >
          Retry
        </button>
      </Card>
    )
  }

  const briefFields = [
    { label: 'Problem', value: investigation.investigation_brief.problem },
    { label: 'Observed Contradiction', value: investigation.investigation_brief.observed_contradiction },
    { label: 'Evidence', value: investigation.investigation_brief.evidence },
    { label: 'Hypotheses', value: investigation.hypotheses.map((hypothesis) => hypothesis.text).join(' ') },
    { label: 'Uncertainty', value: investigation.investigation_brief.uncertainty },
    { label: 'Affected Groups', value: investigation.investigation_brief.affected_groups },
    { label: 'Additional Evidence Required', value: investigation.investigation_brief.additional_evidence_required },
    { label: 'Recommended Investigation Steps', value: investigation.investigation_brief.recommended_steps },
  ]

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div className="flex items-center gap-3">
        <SeverityBadge severity={investigation.severity} />
        <h2 className="text-lg font-semibold text-foreground">{investigation.department}</h2>
      </div>

      <Card className="space-y-4">
        <SectionTitle>Root-Cause Hypotheses</SectionTitle>
        <div className="space-y-4">
          {investigation.hypotheses.map((hypothesis, index) => (
            <div key={`${hypothesis.label}-${index}`} className="space-y-1.5">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-foreground">{hypothesis.text}</p>
                <span className="text-sm font-semibold text-foreground">{hypothesis.confidence_pct}%</span>
              </div>
              <ConfidenceBar value={hypothesis.confidence_pct} />
              <p className="text-[11px] font-medium uppercase tracking-wide text-muted-foreground">{hypothesis.label}</p>
            </div>
          ))}
        </div>
      </Card>

      <Card className="border-status-amber/30 bg-status-amber-bg">
        <SectionTitle className="text-foreground">Insufficient evidence to determine root cause with certainty</SectionTitle>
        <p className="mt-2 text-sm font-medium text-muted-foreground">Additional evidence required:</p>
        <ul className="mt-3 space-y-2">
          {investigation.evidence_gaps.map((item) => (
            <li key={item} className="flex items-center gap-2 text-sm text-foreground">
              <Square className="size-4 text-muted-foreground" />
              {item}
            </li>
          ))}
        </ul>
      </Card>

      <Card className="space-y-5">
        <SectionTitle>Investigation Brief</SectionTitle>
        <div className="divide-y divide-border">
          {briefFields.map((field) => (
            <div key={field.label} className="grid gap-1 py-3 sm:grid-cols-[200px_1fr] sm:gap-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">{field.label}</p>
              <p className="text-sm text-foreground">{field.value}</p>
            </div>
          ))}
        </div>
      </Card>

      <Card className="space-y-4">
        <SectionTitle>Human Review Required</SectionTitle>
        <div className="flex items-start gap-3 rounded-lg border border-status-amber/30 bg-status-amber-bg p-4">
          <AlertTriangle className="mt-0.5 size-5 shrink-0 text-status-amber" />
          <p className="text-sm text-foreground">This is an AI-generated investigation brief. It does not constitute a final decision.</p>
        </div>

        <div className="flex flex-wrap gap-3">
          <button onClick={() => submitDecision('accept')} className="inline-flex items-center gap-2 rounded-md bg-status-green px-4 py-2 text-sm font-medium text-white transition-opacity hover:opacity-90">
            <Check className="size-4" />
            Accept Investigation
          </button>
          <button onClick={() => submitDecision('modify')} className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-muted">
            <Pencil className="size-4" />
            Modify
          </button>
          <button onClick={() => submitDecision('reject')} className="inline-flex items-center gap-2 rounded-md border border-status-red/40 bg-card px-4 py-2 text-sm font-medium text-status-red transition-colors hover:bg-status-red-bg">
            <X className="size-4" />
            Reject
          </button>
        </div>

        {decision && (
          <p className="rounded-md border border-border bg-muted px-4 py-2.5 text-sm text-foreground">{decision}</p>
        )}
      </Card>
    </div>
  )
}
