import type { LogEntry } from '../types'

interface Props {
  logs: LogEntry[]
}

export default function LogPanel({ logs }: Props) {
  return (
    <div className="log-list">
      {logs.map((log, index) => (
        <div key={`${log.timestamp}-${index}`} className="log-row">
          <strong>{log.timestamp} — {log.level}</strong>
          <div>{log.source}</div>
          <div>{log.message}</div>
        </div>
      ))}
    </div>
  )
}
