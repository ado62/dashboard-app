import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import L from 'leaflet'
import type { LocationPoint } from '../types'
import 'leaflet/dist/leaflet.css'

interface Props {
  points: LocationPoint[]
}

export default function MapView({ points }: Props) {
  const center = points.length
    ? [points[0].latitude, points[0].longitude] as [number, number]
    : [39.5, -98.35] as [number, number]

  // Fix for react-leaflet default icon issue
  delete (L.Icon.Default.prototype as any)._getIconUrl
  L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
  })

  return (
    <MapContainer center={center} zoom={4} scrollWheelZoom={false} className="leaflet-container">
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {points.map((point, index) => (
        <CircleMarker
          key={`${point.latitude}-${point.longitude}-${index}`}
          center={[point.latitude, point.longitude]}
          radius={8}
          pathOptions={{ color: '#2563eb', fillColor: '#93c5fd', fillOpacity: 0.8 }}
        >
          <Popup>
            <strong>{point.region}</strong>
            <div>{point.category}</div>
            <div>value: {point.value ?? 'n/a'}</div>
            <div>{point.note}</div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  )
}
