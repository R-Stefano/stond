import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private _http: HttpClient,
  ) { }

  getDeviceStatus() {
    return this._http.get<any>(environment.apiUrl + `api/devices/${environment.deviceId}/status`)
  }

  getSensorData(sensorId, scaleSelected: string | null) {
    return this._http.get<any>(environment.apiUrl + `api/devices/${environment.deviceId}/sensors/${sensorId}`, {params: {scale: scaleSelected}})
  }
}
