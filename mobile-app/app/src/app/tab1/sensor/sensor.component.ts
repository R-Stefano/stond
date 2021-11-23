import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/core/api.service';
import { Sensor, SensorReading } from 'src/app/core/models';
import * as moment from 'moment';
import 'chartjs-adapter-moment'
import { Chart, BarController, LineController, BarElement, LineElement, PointElement,CategoryScale, LinearScale, TimeScale} from 'chart.js';
Chart.register( BarController, LineController, BarElement, LineElement, PointElement, CategoryScale, LinearScale, TimeScale);

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss'],
})
export class SensorComponent implements OnInit {
  @ViewChild('pageHeader') pageHeader;
  public displayPageHeaderInToolbar: boolean = false;
  
  @ViewChild('lineChart') lineChart;
  lines: any;
  private _scales = {
    1: '1H',
    6: '6H',
    24: '1D',
    720: '30D'
  }
  public scaleSelected = '1H'
  public sensor: Sensor;
  public sensorName: string = ""

  private sensorsNames = {
    'env_temperature': 'environment temperature',
    'env_humidity': 'environment humidity',
    'water_temperature': 'water temperature',
    'water_ph': 'water ph',
    'water_level': 'water level',
  }
  
  
  constructor(
    private _route: ActivatedRoute,
    private _api: ApiService
  ) { }

  ngOnInit() {
    let sensorId = this._route.snapshot.paramMap.get('sensorId')
    this._api.getSensorData(sensorId, this.scaleSelected).subscribe((sensor: Sensor) => {
      this.sensor = sensor
      this.sensorName = this.sensorsNames[sensor.name]
      this.lines = new Chart(this.lineChart.nativeElement, {
        type: 'line',
        data: {
          //labels: sensor.readings.map((reading: SensorReading) => reading.timestamp),
          datasets: [{
            data: sensor.readings.map((reading: SensorReading) => {return {x: moment(reading.timestamp), y: reading.value}}),
            fill: {
              target: 'origin',
              above: 'rgb(255, 0, 0)',
              below: 'rgb(0, 0, 255)'
            },
            tension: 0.1, // Bezier curve tension of the line. Set to 0 to draw straightlines. This option is ignored if monotone cubic interpolation is used.
            backgroundColor: getComputedStyle(document.body).getPropertyValue('--ion-color-secondary'),
            borderColor: getComputedStyle(document.body).getPropertyValue('--ion-color-secondary'),
            borderWidth: 1, //The line width (in pixels).
            pointRadius: 0,
          }]
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                  unit: 'hour',
                  displayFormats: {
                    quarter: 'MMM YYYY'
                }
              },
              ticks: {
                  source: 'data'
              },
              grid: {
                display: false
              }
            },
            y: {
              //beginAtZero: true,
              grid: {
                display: false,
              }
            }
          }
        }
      });
    }) 
  }

  onScroll(evt) {
    this.displayPageHeaderInToolbar = this.pageHeader.nativeElement.getBoundingClientRect().top < 30;
  }

  onChangeXScale(hours: number) {
    this.scaleSelected = this._scales[hours]
    this._fetchData(this.scaleSelected)
  }

  private _fetchData(scaleSelected) {
    this._api.getSensorData(this.sensor.Id, scaleSelected).subscribe((sensor: Sensor) => {
      this.lines.data.datasets[0].data  = sensor.readings.map((reading: SensorReading) => {return {x: moment(reading.timestamp), y: reading.value}});
      this.lines.update();
    })
  }
}
