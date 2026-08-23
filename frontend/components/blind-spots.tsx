'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { ChevronDown, ChevronUp, ArrowRight, Loader2 } from 'lucide-react'
import {
  Card,
  SeverityBadge,
  IndicatorChip,
} from '@/components/civic-ui'
import { getBlindSpots, type BlindSpot as ApiBlindSpot } from '@/lib/api'

type BlindSpot = {
  department: string
  severity: 'HIGH' | 'MEDIUM' | 'LOW'
  indicators: { label: string; value: string; tone: 'up' | 'down' | 'neutral' }[]
  defaultExpanded: boolean
}

function BlindSpotCard({ spot }: { spot: BlindSpot }) {
  const [expanded, setExpanded] = useState(spot.defaultExpanded)

  return (
    <Card className="p-0">
      <button onClick={() => setExpanded((v) => !v)} className="flex w-full items-start justify-between gap-4 p-5 text-left">
        <div className="flex items-start gap-3">
          <SeverityBadge severity={spot.severity} />
          <div>
            <p className="font-semibold text-foreground">{spot.department}</p>
          </div>
        </div>
        {expanded ? (
          <ChevronUp className="size-5 shrink-0 text-muted-foreground" />
        ) : (
          <ChevronDown className="size-5 shrink-0 text-muted-foreground" />
        )}
      </button>

      {expanded && (
        <div className="space-y-4 border-t border-border p-5">
          <div className="flex flex-wrap gap-2">
            {spot.indicators.map((ind) => (
              <IndicatorChip key={ind.label} label={ind.label} value={ind.value} tone={ind.tone as 'up' | 'down' | 'neutral'} />
            ))}
          </div>

          <Link href={`/investigations?department=${encodeURIComponent(spot.department)}`} className="inline-flex items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">
            View Investigation
            <ArrowRight className="size-4" />
          </Link>
        </div>
      )}
    </Card>
  )
}

export function BlindSpots() {
  const [spots, setSpots] = useState<BlindSpot[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadSpots() {
      try {
        setLoading(true)
        setError(null)
        const response = await getBlindSpots()
        setSpots(
          response.blind_spots.map((spot: ApiBlindSpot) => ({
            department: spot.department,
            severity: spot.severity as 'HIGH' | 'MEDIUM' | 'LOW',
            indicators: [
              { label: 'Resolution rate', value: `${spot.resolution_rate}%`, tone: 'up' },
              { label: 'Pending >3 years', value: `${spot.pending_gt_3yr}`, tone: 'down' },
              { label: 'Pending >1 year', value: `${spot.pending_gt_1yr_pct}%`, tone: 'down' },
            ],
            defaultExpanded: spot.severity === 'HIGH',
          })),
        )
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unable to load blind spots')
      } finally {
        setLoading(false)
      }
    }

    loadSpots()
  }, [])

  function retryLoadSpots() {
    setLoading(true)
    setError(null)
    getBlindSpots()
      .then((response) => {
        setSpots(
          response.blind_spots.map((spot) => ({
            department: spot.department,
            severity: spot.severity as 'HIGH' | 'MEDIUM' | 'LOW',
            indicators: [
              { label: 'Resolution rate', value: `${spot.resolution_rate}%`, tone: 'up' },
              { label: 'Pending >3 years', value: `${spot.pending_gt_3yr}`, tone: 'down' },
              { label: 'Pending >1 year', value: `${spot.pending_gt_1yr_pct}%`, tone: 'down' },
            ],
            defaultExpanded: spot.severity === 'HIGH',
          })),
        )
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Unable to load blind spots')
      })
      .finally(() => setLoading(false))
  }

  if (loading) {
    return (
      <Card className="flex items-center gap-3">
        <Loader2 className="size-5 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">Loading blind spots...</p>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="border-status-red/30 bg-status-red-bg">
        <p className="font-semibold text-status-red">Unable to load blind spots</p>
        <p className="mt-1 text-sm text-foreground">{error}</p>
        <button
          type="button"
          onClick={retryLoadSpots}
          className="mt-4 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
        >
          Retry
        </button>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {spots.map((spot) => (
        <BlindSpotCard key={spot.department} spot={spot} />
      ))}
    </div>
  )
}
