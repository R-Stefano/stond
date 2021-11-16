import { Component, HostListener, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { ApiService } from '../core/api.service';
import { SocketService } from '../core/socket.service';

export class DeviceStatus {
  sensors: {
    env_temperature: {
      isWorking: boolean,
      value: number
    },
    water_ph: {
      isWorking: boolean,
      value: number
    }
  }
  actuators: {
    ventilation: {
      isWorking: boolean,
      status: string
    },
    LED: {
      isWorking: boolean,
      status: string
    }
  }
  constructor(data) {
    Object.assign(this, data);
  }

  get temperature_status(): string {
    if (this.sensors.env_temperature.value > 23 && this.sensors.env_temperature.value < 26) {
      return 'ok'
    }
    else if (this.sensors.env_temperature.value > 20 && this.sensors.env_temperature.value < 29) {
      return 'warning'
    } else {
      return 'error'
    }
  }

  get ph_status(): string {
    if (this.sensors.water_ph.value > 5.5 && this.sensors.water_ph.value < 6.5) {
      return 'ok'
    }
    else if (this.sensors.water_ph.value > 4.5 && this.sensors.water_ph.value < 7.5) {
      return 'warning'
    } else {
      return 'error'
    }
  }

}

export class AnalyticsOverview {
  currentSeasonID: number
  fan: string
  temperature: number
  ph: number
  water_level: number
  water_temperature: number
  humidity: number
  nutrients: Date

  constructor(data) {
    Object.assign(this, data);
  }





  get humidity_status(): string {
    if (this.humidity > 40 && this.humidity < 60) {
      return 'ok'
    }
    else if (this.temperature > 30 && this.temperature < 70) {
      return 'warning'
    } else {
      return 'error'
    }
  }

  get water_temp_status(): string {
    if (this.water_temperature < 20) {
      return 'ok'
    }
    else if (this.water_temperature < 24) {
      return 'warning'
    } else {
      return 'error'
    }
  }
}

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {
  @ViewChild('pageHeader') pageHeader;
  public displayPageHeaderInToolbar: boolean = false;
  
  private _subscriptions = [];
  public deviceStatus: DeviceStatus;

  public strain = {
    refImage: 'https://images.hytiva.com/Black-Widow.jpg?mw420-mh420',
    name: 'black widow',
    alias: 'test alias',
    description: 'Black Widow is a balanced hybrid marijuana strain made by crossing South American with South Indian Sativa..',
    thc: 18,
    growing_period_weeks: 12,
    yield: 100,
    type: 'hybrid'
  }

  public analytics: AnalyticsOverview = new AnalyticsOverview({
    currentSeasonID: 1,
    fan: 'on',
    ventilation: 'on',
    temperature: 28.5,
    ph: 6.5,
    water_level: 1,
    water_temperature: 21.5,
    humidity: 68,
    nutrients: new Date(),
  })

  constructor(
    private _router: Router,
    private _socketMng: SocketService,
    private _api: ApiService
  ) {
    this._socketMng.login()

    this._socketMng.event().subscribe(evt => console.log(evt))
    
    this.onRefresh()

    this._subscriptions.push(setInterval(() => {
      const timestamp = new Date()

      if (timestamp.getSeconds() == 5) {
        this.onRefresh()
      }
    }, 1000))
  }

  ngOnDestroy() {
    this._subscriptions.map((_sub): Subscription => _sub.unsubscribe())
  }

  onDetailsClick() {
    this._router.navigate([`tabs/season/${this.analytics.currentSeasonID}/details`])
  }

  onScroll(evt) {
    this.displayPageHeaderInToolbar = this.pageHeader.nativeElement.getBoundingClientRect().top < 30;
  }

  onVentilationButtonClick() {
    this._socketMng.updateDeviceVentilation({status: 'on'})
  }

  onLightButtonClick() {
    this._socketMng.updateDeviceLight({status: 'on'})
  }

  onRefresh() {
    this._api.getDeviceStatus().subscribe((deviceStatus: DeviceStatus) => {
      this.deviceStatus = new DeviceStatus(deviceStatus)
      console.log(this.deviceStatus)
    })
  }

}
