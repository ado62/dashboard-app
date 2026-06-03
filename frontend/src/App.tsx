import { useEffect, useState } from 'react'
import { ChartData, LocationPoint, LogEntry, TableResponse } from './types'
import LineChartView from './components/LineChart'
import DataTable from './components/DataTable'
import MapView from './components/MapView'
import LogPanel from './components/LogPanel'

const API_BASE =
  import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function App() {
  const [chartData, setChartData] = useState<ChartData[]>([])
  const [tableData, setTableData] = useState<TableResponse | null>(null)
  const [locations, setLocations] = useState<LocationPoint[]>([])
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function load() {
      try {
	const [chartRes, tableRes, locationRes, logRes] = await Promise.all([
	  fetch(`${API_BASE}/api/data/chart`),
	  fetch(`${API_BASE}/api/data/table`),
	  fetch(`${API_BASE}/api/data/locations`),
	  fetch(`${API_BASE}/api/logs`),
	])
        if (!chartRes.ok || !tableRes.ok || !locationRes.ok || !logRes.ok) {
          throw new Error('Unable to load backend data')
        }
        const chartJson = await chartRes.json()
        const tableJson = await tableRes.json()
        const locationJson = await locationRes.json()
        const logJson = await logRes.json()

        setChartData(chartJson.series)
        setTableData(tableJson)
        setLocations(locationJson.points)
        setLogs(logJson.logs)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    load()
  }, [])

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>CSV Dashboard</h1>
          <p>Python backend + CSV source data with charts, tables, map, and logs.</p>
        </div>
      </header>

      <main>
        {error ? (
          <section className="alert-panel">{error}</section>
        ) : loading ? (
          <section className="alert-panel">Loading dashboard data…</section>
        ) : (
          <>
            <section className="grid-row">
              <article className="card card-large">
                <h2>Trend by date</h2>
                <LineChartView data={chartData} />
              </article>
              <article className="card card-small">
                <h2>Recent logs</h2>
                <LogPanel logs={logs} />
              </article>
            </section>

            <section className="grid-row">
              <article className="card card-table">
                <h2>Data table preview</h2>
                {tableData ? <DataTable rows={tableData.rows} /> : <p>No row data</p>}
              </article>
              <article className="card card-map">
                <h2>Regional locations</h2>
                <MapView points={locations} />
              </article>
            </section>
          </>
        )}
      </main>
    </div>
  )
}

export default App
