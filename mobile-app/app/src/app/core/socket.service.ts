import { Injectable } from '@angular/core';
import { Socket, SocketIoConfig } from 'ngx-socket-io';

@Injectable({
  providedIn: 'root'
})
export class SocketService {
  config: SocketIoConfig = { url: 'http://localhost:4444', options: {} };
  public deviceId: string = 'e0db0991-5c15-4a98-bd05-7ed14cefbca5'
  public messages: [];

  constructor(
    private socket: Socket
  ) {
  }

  login() {
    this.socket.emit('login', {deviceId: this.deviceId})
  }

  updateDeviceVentilation(data) {
    this.socket.emit('device:ventilation:put', data)
  }

  updateDeviceLight(data) {
    this.socket.emit('device:light:put', data)
  }

  event() {
    return this.socket.fromEvent('event')
  }
}
