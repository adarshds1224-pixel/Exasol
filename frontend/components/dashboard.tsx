'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import {
  AlertTriangle,
  EyeOff,
  Flame,
  FileText,
  Activity,
  ArrowRight,
  Loader2,
} from 'lucide-react'
import {
  Line,
  LineChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import { Card } from '@/components/civic-ui'
import { getDashboard, type DashboardData } from '@/lib/api'

const iconMap = {
  EyeOff,
  Flame,
  FileText,
  Activity,
}

const statTone: Record<string, string> = {
  blue: 'bg-accent text-primary',
  red: 'bg-status-red-bg text-status-red',
  amber: 'bg-status-amber-bg text-status-amber',
}

export function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true)
        setData(await getDashboard())
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unable to load dashboard data')
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [])

  function retryLoadDashboard() {
    setLoading(true)
    setError(null)
    getDashboard()
      .then(setData)
      .catch((err) => {
        setError(err instanceof Error ? err.message : 'Unable to load dashboard data')
      })
      .finally(() => setLoading(false))
  }

  if (loading) {
    return (
      <Card className="flex items-center gap-3">
        <Loader2 className="size-5 animate-spin text-primary" />
        <p className="text-sm text-muted-foreground">Loading dashboard...</p>
      </Card>
    )
  }

  if (error || !data) {
    return (
      <Card className="border-status-red/30 bg-status-red-bg">
        <p className="font-semibold text-status-red">Dashboard unavailable</p>
        <p className="mt-1 text-sm text-foreground">{error ?? 'No data returned by the backend.'}</p>
        <button
          type="button"
          onClick={retryLoadDashboard}
          className="mt-4 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
        >
          Retry
        </button>
      </Card>
    )
  }

  const stats = [
    { label: 'Active Blind Spots', value: data.active_blind_spots, tone: 'blue', icon: 'EyeOff' },
    { label: 'High Severity', value: data.high_severity_count, tone: 'red', icon: 'Flame' },
    { label: 'Cases Analyzed', value: data.cases_analyzed, tone: 'amber', icon: 'FileText' },
  ]

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => {
          const Icon = iconMap[(stat.icon as keyof typeof iconMap) ?? 'EyeOff'] ?? EyeOff
          return (
            <Card key={stat.label} className="flex items-center gap-4">
              <div className={`flex size-11 items-center justify-center rounded-lg ${statTone[stat.tone] ?? statTone.blue}`}>
                <Icon className="size-5" />
              </div>
              <div>
                <p className="text-2xl font-semibold text-foreground">{stat.value}</p>
                <p className="text-sm text-muted-foreground">{stat.label}</p>
              </div>
            </Card>
          )
        })}
      </div>

      <Card>
        <div className="mb-1 flex items-center justify-between">
          <div>
            <h2 className="text-base font-semibold text-foreground">National Yearly Trend</h2>
            <p className="text-sm text-muted-foreground">Received, disposed, and resolution rate</p>
          </div>
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <span className="size-2.5 rounded-full bg-chart-1" /> Received
            </span>
            <span className="flex items-center gap-1.5">
              <span className="size-2.5 rounded-full bg-chart-2" /> Disposed
            </span>
          </div>
        </div>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data.yearly_trend} margin={{ top: 16, right: 12, left: -8, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
              <XAxis dataKey="year" stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip
                contentStyle={{
                  borderRadius: 8,
                  border: '1px solid var(--border)',
                  fontSize: 12,
                }}
              />
              <Legend wrapperStyle={{ display: 'none' }} />
              <Line type="monotone" dataKey="received" name="Received" stroke="var(--chart-1)" strokeWidth={2.5} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="disposed" name="Disposed" stroke="var(--chart-2)" strokeWidth={2.5} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-6 border-t border-border pt-5">
          <div className="mb-1">
            <h2 className="text-base font-semibold text-foreground">Monthly Prediction vs Actual</h2>
            <p className="text-sm text-muted-foreground">Prediction performance across 2025</p>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.monthly_prediction} margin={{ top: 16, right: 12, left: -8, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                <XAxis dataKey="month" stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                <Tooltip contentStyle={{ borderRadius: 8, border: '1px solid var(--border)', fontSize: 12 }} />
                <Legend wrapperStyle={{ display: 'none' }} />
                <Line type="monotone" dataKey="predicted" name="Predicted" stroke="var(--chart-1)" strokeWidth={2.5} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="actual" name="Actual" stroke="var(--chart-2)" strokeWidth={2.5} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </Card>

      {data.top_blind_spots.length > 0 && (
        <div className="flex flex-col items-start justify-between gap-4 rounded-xl border border-status-amber/30 bg-status-amber-bg p-5 sm:flex-row sm:items-center">
          <div className="flex items-start gap-3">
            <AlertTriangle className="mt-0.5 size-5 shrink-0 text-status-amber" />
            <div>
              <p className="font-semibold text-foreground">Potential blind spot detected</p>
              <p className="text-sm text-muted-foreground">{data.top_blind_spots[0].indicator_summary}</p>
            </div>
          </div>
          <Link href="/blind-spots" className="inline-flex shrink-0 items-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90">
            View Details
            <ArrowRight className="size-4" />
          </Link>
        </div>
      )}
    </div>
  )
}
