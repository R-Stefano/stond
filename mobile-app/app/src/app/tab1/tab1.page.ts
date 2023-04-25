import { Component, HostListener, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { ApiService } from '../core/api.service';
import { Device } from '../core/models';
import { SocketService } from '../core/socket.service';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page {
  @ViewChild('pageHeader') pageHeader;
  public displayPageHeaderInToolbar: boolean = false;
  
  private _subscriptions = [];
  public device: Device;
  public currentSeasonID: number = 1

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

  constructor(
    private _router: Router,
    //private _socketMng: SocketService,
    private _api: ApiService
  ) {
    //this._socketMng.login()
    //this._socketMng.event().subscribe(evt => console.log(evt))
    
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
    this._router.navigate([`tabs/season/${this.currentSeasonID}/details`])
  }

  onScroll(evt) {
    this.displayPageHeaderInToolbar = this.pageHeader.nativeElement.getBoundingClientRect().top < 30;
  }

  onComponentButtonClick() {

  }

  onOpenSensorDetails(sensorId: string) {
    this._router.navigate([`tabs/season/sensors/${sensorId}`])

  }

  onRefresh() {
    this._api.getDevice().subscribe((device: Device) => {
      console.log(device)
      this.device = device
    })
  }

}
