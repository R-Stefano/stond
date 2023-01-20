import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/core/api.service';
import { Sensor, SensorReading } from 'src/app/core/models';
import * as moment from 'moment';
import 'chartjs-adapter-moment'
import { Chart, BarController, LineController, BarElement, LineElement, PointElement,CategoryScale, LinearScale, TimeScale, ChartConfiguration} from 'chart.js';
import { Subscription } from 'rxjs';
Chart.register( BarController, LineController, BarElement, LineElement, PointElement, CategoryScale, LinearScale, TimeScale);

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss'],
})
export class SensorComponent implements OnInit {
  @ViewChild('pageHeader') pageHeader;
  public displayPageHeaderInToolbar: boolean = false;
  private _subscriptions = [];
  
  @ViewChild('lineChart') lineChartElRef;
  lineChartObj: any;

  public scaleSelected = '1H'
  public sensor: Sensor;
  public sensorName: string = ""
  public currentDataPoint;

  public sensorsConfigs = {
    'env_temperature': {
      name: 'environment temperature',
      measurementUnit: '° C'
    },
    'env_humidity': {
      name: 'environment humidity',
      measurementUnit: '%'
    },
    'water_temperature': {
      name: 'water temperature',
      //measurementUnit: '° C'
      measurementUnit: 'cm'
    },
    'water_ph': {
      name: 'water ph',
      measurementUnit: ''
    },
    'water_level': {
      name: 'water level',
      measurementUnit: ''
    },
  }
  
  private _chartConfigs: ChartConfiguration = {
    type: 'line',
    data: {
      datasets: [{
        data: [],
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
      responsive: true, // Resizes the chart canvas when its container does
      scales: {
        x: {
          type: 'time',
          time: {
              unit: 'day',
          },
          ticks: {
              source: 'data'
          },
          grid: {
            display: false
          }
        },
        y: {
          grid: {
            display: false,
          }
        }
      },
      hover: {
        mode: 'index',
        intersect: false
      },
      onHover: (evt, el, chart) => {
        // set the new current value
        this.currentDataPoint = this._chartConfigs.data.datasets[0].data[el[0].index]

        // draw line
        chart.ctx.beginPath();
        chart.ctx.setLineDash([5, 10]);
        chart.ctx.moveTo(el[0].element.x, chart.scales['y'].top);
        chart.ctx.lineTo(el[0].element.x, chart.scales['y'].bottom);
        chart.ctx.lineWidth = 1;
        chart.ctx.strokeStyle = '#757575';
        chart.ctx.stroke();
      }
    }
  }

  constructor(
    private _route: ActivatedRoute,
    private _api: ApiService
  ) { }

  ngOnInit() {
    //fetch sensor info
    this._api.getSensor(this._route.snapshot.paramMap.get('sensorId')).subscribe((sensor: Sensor) => this.sensor = sensor)

    this.getHistoryData()
  }
  
  ngAfterViewInit() {
    // setup graph
    this.lineChartObj = new Chart(this.lineChartElRef.nativeElement, this._chartConfigs);
  }

  ngOnDestroy() {
    //this._subscriptions.map((_sub): Subscription => _sub.unsubscribe())
  }

  onScroll(evt) {
    this.displayPageHeaderInToolbar = this.pageHeader.nativeElement.getBoundingClientRect().top < 30;
  }

  onChangeXScale(scale: string) {
    this.scaleSelected = scale
    this.getHistoryData()
  }

  getHistoryData() {
    const params = {}
    const time = '2022-01-17 06:00:00'
    const timeNow = moment(time)//moment().utc()
    switch (this.scaleSelected) {
      case '1H':
        params['timestamp'] = `${timeNow.subtract({hours: 1}).format()}`
        break;
      case '6H':
        params['timestamp'] = `${timeNow.subtract({hours: 6}).format()}`
        break;
      case '1D':
        params['timestamp'] = `${timeNow.subtract({days: 1}).format()}`
        break;
      case '7D':
        params['timestamp'] = `${timeNow.subtract({days: 7}).format()}`
        break;
      case '30D':
        params['timestamp'] = `${timeNow.subtract({days: 30}).format()}`
        break;
    }

    this._api.getSensorHistory(this._route.snapshot.paramMap.get('sensorId'), params).subscribe((sensorReadings: SensorReading[]) => {
      // Process values for the graph
      let dataSeries = []
      let binSize = 1 //minutes bin size
      switch (this.scaleSelected) {
        case '1H':
          binSize = 1
          break;
        case '6H':
          binSize = 5
          break;
        case '1D':
          binSize = 15
          break;
        case '7D':
          binSize = 120
          break;
        case '30D':
          binSize = 60 * 12 // 12 H
          break;
      }

      sensorReadings = []
      let initialValue = 0
      // pant growht contorl
      for (var i=0; i<168;i++) {
        let randomness = Math.random() * 0.2

        if (i < 48) {
          randomness = randomness / 4
        }
        initialValue += randomness

        sensorReadings.push({
          Id: '',
          sensorId: '',
          isWorking: true,
          timestamp: new Date(moment('2022-07-17 12:00:00').add({hours: i}).valueOf()),
          value: initialValue
        })
      }

      // Temp and humidity contorl
      /*
      const maxTemp = 80
      let initialValue = 50
      let humOn = true
      let tempIncreaseI = 10
      for (var i=0; i<360;i++) {
        let randomness = Math.random() * 0.1
        if (!humOn) {
          const prevLog = Math.log2(1+tempIncreaseI)
          tempIncreaseI += 6
          const newLog = Math.log2(1+tempIncreaseI)
          // temp increase
          const step = (newLog - prevLog) + randomness
          initialValue = initialValue - step
        }

        if (humOn) {
          tempIncreaseI = 10
          const step = Math.random()
          initialValue = initialValue + step
        }

        if (initialValue > 81) {
          humOn = false
        }

        if (initialValue < 79) {
          humOn = true
        }

        sensorReadings.push({
          Id: '',
          sensorId: '',
          isWorking: true,
          timestamp: new Date(moment().add({minutes: i}).valueOf()),
          value: initialValue
        })
      }
      */

      for (var record of sensorReadings) {
        const minutesDiff = Math.round(moment(record.timestamp).diff(timeNow) / 60000) // difference in minutes
        const binIdx = Math.round(minutesDiff / binSize)

        const datapoint = {
          y: record.value,
          x: moment(record.timestamp).format("YYYY-MM-DD HH:mm:ss")
        }

        if (dataSeries.length == binIdx) { // add new bin
          dataSeries.push(datapoint)
        } else { // update existing bin
          dataSeries[binIdx] = datapoint
        }
      }

      // remove the empty 
      dataSeries = dataSeries.filter(record => record)
      // display current value
      this.currentDataPoint = dataSeries[dataSeries.length - 1]
      
      // refresh chart
      this._chartConfigs.data.datasets[0].data = dataSeries
      this.lineChartObj.destroy()
      this.lineChartObj = new Chart(this.lineChartElRef.nativeElement, this._chartConfigs);

    })
  }
}
