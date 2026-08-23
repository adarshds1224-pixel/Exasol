'use client'

import { useEffect, useState } from 'react'
import { Gauge, MessageSquare, Cog, Archive, BadgeCheck, Loader2 } from 'lucide-react'
import { Card } from '@/components/civic-ui'
import { getEvidence, type EvidenceSource } from '@/lib/api'

const iconMap = {
  kpi: Gauge,
  citizen: MessageSquare,
  operational: Cog,
  historical: Archive,
}

export function Evidence() {
  const [items, setItems] = useState<EvidenceSource[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadEvidence() {
      try {
        setLoading(true)
        setError(null)
        const data = await getEvidence()
        setItems(data.evidence_sources)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unable to load evidence chain')
      } finally {
        setLoading(false)
      }
    }

    loadEvidence()
  }, [])

  function retryLoadEvidence() {
    setLoading(true)
    setError(null)
    getEvidence()
      .then((data) => setItems(data.evidence_sources))
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Unable to load evidence chain')
      })
      .finally(() => setLoading(false))
  }

  if (loading) {
    return (
      <Card className="flex items-center gap-3">
        <Loader2 className="size-5 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">Loading evidence chain...</p>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="border-status-red/30 bg-status-red-bg">
        <p className="font-semibold text-status-red">Evidence chain unavailable</p>
        <p className="mt-1 text-sm text-foreground">{error}</p>
        <button
          type="button"
          onClick={retryLoadEvidence}
          className="mt-4 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
        >
          Retry
        </button>
      </Card>
    )
  }

  return (
    <div className="mx-auto max-w-3xl">
      <ol className="relative space-y-4 border-l border-border pl-6">
        {items.map((item) => {
          const iconKey = item.type === 'KPI Data'
            ? 'kpi'
            : item.type === 'Severity Signal'
              ? 'citizen'
              : item.type === 'Operational Signal'
                ? 'operational'
                : 'historical'
          const Icon = iconMap[iconKey]
          return (
            <li key={item.source_name} className="relative">
              <span className="absolute -left-[35px] flex size-6 items-center justify-center rounded-full border border-border bg-card">
                <span className="size-2.5 rounded-full bg-primary" />
              </span>
              <Card className="flex items-start gap-4">
                <div className="flex size-11 shrink-0 items-center justify-center rounded-lg bg-accent text-primary">
                  <Icon className="size-5" />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-semibold text-foreground">{item.source_name}</p>
                  <p className="text-sm text-muted-foreground">{item.type}</p>
                  <p className="mt-1 text-sm text-foreground">
                    <span className="text-muted-foreground">Source:</span> {item.origin}
                  </p>
                  <span className={`mt-3 inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${item.verified ? 'border-status-green/30 bg-status-green-bg text-status-green' : 'border-status-amber/30 bg-status-amber-bg text-status-amber'}`}>
                    <BadgeCheck className="size-3.5" />
                    {item.verified ? 'Data verified' : 'Prototype-generated, not independently verified'}
                  </span>
                </div>
              </Card>
            </li>
          )
        })}
      </ol>
    </div>
  )
}
