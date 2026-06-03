export interface ChartData {
  date: string
  value: number
}

export interface TableRow {
  date: string | null
  category: string
  region: string
  value: number | null
  latitude: number | null
  longitude: number | null
  note: string
}

export interface TableResponse {
  rows: TableRow[]
  count: number
}

export interface LocationPoint {
  region: string
  category: string
  value: number | null
  latitude: number
  longitude: number
  note: string
}

export interface LogEntry {
  timestamp: string
  level: string
  source: string
  message: string
}
