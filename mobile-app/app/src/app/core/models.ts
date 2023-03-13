export class Device {
    id: string
    lastSnapshotReceivedAt: Date
    components: Component[]

    constructor(data) {
        data.components = data.components.map(component => new Component(component))
        return Object.assign(this, data)
    }

    getComponent(sensorName): Component {
        return this.components.find(c => c.name == sensorName)
    }
}

export class Component {
    id:       string
    deviceId: string
    type:     string
    name:     string
    isWorking; boolean
    status:   string
    value:    any
    valueType: string
    updatedAt: Date

    constructor(data) {
        if (data.valueType == 'number') {
            data.value = Number(data.value)
        } else if (data.valueType == 'boolean') {
            data.value = Boolean(data.value)
        }
        return Object.assign(this, data)
    }

    get valueScore() {
        switch(this.name) {
            case 'led':
                if (this.status == "ON") {
                    return 'success'
                } else {
                    return 'error'
                }
            case 'humidifier':
                if (this.status == "ON") {
                    return 'success'
                } else {
                    return 'error'
                }
            case 'hvac':
                if (this.status == "ON") {
                    return 'success'
                } else {
                    return 'error'
                }
            case 'fan_bottom':
                if (this.status == "ON") {
                    return 'success'
                } else {
                    return 'error'
                }
            case 'fan_top':
                if (this.status == "ON") {
                    return 'success'
                } else {
                    return 'error'
                }
            case 'env_temperature':
                if (this.value > 23 && this.value < 26) {
                    return 'success'
                } else if (this.value > 20 && this.value < 29) {
                    return 'warning'
                } else {
                    return 'error'
                }
            case 'water_ph':
                if (this.value > 5.5 && this.value < 6.5) {
                    return 'success'
                } else if (this.value > 5 && this.value < 7) {
                    return 'warning'
                } else {
                    return 'error'
                }
            case 'env_humidity':
                if (this.value > 55 && this.value < 80) {
                    return 'success'
                } else if (this.value > 40 && this.value < 90) {
                    return 'warning'
                } else {
                    return 'error'
                }
            case 'water_temperature':
                if (this.value < 20) {
                    return 'success'
                } else if (this.value < 22) {
                    return 'warning'
                } else {
                    return 'error'
                }
            case 'cpu_temperature':
                if (this.value < 45) {
                    return 'success'
                } else if (this.value < 65) {
                    return 'warning'
                } else {
                    return 'error'
                }
        }
    }
}

export interface SensorReading {
    Id: string
    isWorking: boolean
    sensorId: string
    timestamp: Date
    value: number
}