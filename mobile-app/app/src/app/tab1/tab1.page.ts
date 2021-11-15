import { Component, HostListener, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { SocketService } from '../core/socket.service';

export class AnalyticsOverview {
  currentSeasonID: number
  fan: string
  ventilation: string
  temperature: number
  ph: number
  water_level: number
  water_temperature: number
  humidity: number
  nutrients: Date

  constructor(data) {
    Object.assign(this, data);
  }

  get temperature_status(): string {
    if (this.temperature > 23 && this.temperature < 26) {
      return 'ok'
    }
    else if (this.temperature > 20 && this.temperature < 29) {
      return 'warning'
    } else {
      return 'error'
    }
  }

  get ph_status(): string {
    if (this.ph > 5.5 && this.temperature < 6.5) {
      return 'ok'
    }
    else if (this.temperature > 4.5 && this.temperature < 7.5) {
      return 'warning'
    } else {
      return 'error'
    }
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
    private _socketMng: SocketService
  ) {
    this._socketMng.login()

    this._socketMng.event().subscribe(evt => console.log(evt))
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

}
