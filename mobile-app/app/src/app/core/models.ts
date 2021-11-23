export class Sensor {
    Id: string
    isWorking: boolean
    currentValue: number
    name: string
    readings: SensorReading[]
}

export interface SensorReading {
    Id: string
    isWorking: boolean
    sensorId: string
    timestamp: Date
    value: number
}