import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Device } from './models';
import { map, catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private _http: HttpClient,
  ) { }

  getDevice(): Observable<Device> {
    return this._http.get<any>(environment.apiUrl + `api/devices/${environment.deviceId}`).pipe(
      map(device => new Device(device))
    )
  }

  getSensor(sensorId: string) {
    return this._http.get<any>(environment.apiUrl + `api/sensors/${sensorId}`)
  }

  getSensorHistory(sensorId: string, params) {
    return this._http.get<any>(environment.apiUrl + `api/sensors/${sensorId}/history`, {params: params})
  }
}
