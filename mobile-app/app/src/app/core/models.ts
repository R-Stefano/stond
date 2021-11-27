export class Sensor {
    Id: string
    isWorking: boolean
    currentValue: number
    name: string
    updatedAt: Date
}

export interface SensorReading {
    Id: string
    isWorking: boolean
    sensorId: string
    timestamp: Date
    value: number
}