import type { TableRow } from '../types'

interface Props {
  rows: TableRow[]
}

export default function DataTable({ rows }: Props) {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Category</th>
            <th>Region</th>
            <th>Value</th>
            <th>Note</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={`${row.date}-${index}`}>
              <td>{row.date ?? '—'}</td>
              <td>{row.category}</td>
              <td>{row.region}</td>
              <td>{row.value != null ? row.value : '—'}</td>
              <td>{row.note}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
