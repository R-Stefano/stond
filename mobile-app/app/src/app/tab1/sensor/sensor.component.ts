import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from 'src/app/core/api.service';
import { Sensor, SensorReading } from 'src/app/core/models';
import * as moment from 'moment';
import 'chartjs-adapter-moment'
import { Chart, BarController, LineController, BarElement, LineElement, PointElement,CategoryScale, LinearScale, TimeScale, ChartConfiguration} from 'chart.js';
Chart.register( BarController, LineController, BarElement, LineElement, PointElement, CategoryScale, LinearScale, TimeScale);

@Component({
  selector: 'app-sensor',
  templateUrl: './sensor.component.html',
  styleUrls: ['./sensor.component.scss'],
})
export class SensorComponent implements OnInit {
  @ViewChild('pageHeader') pageHeader;
  public displayPageHeaderInToolbar: boolean = false;
  
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
      measurementUnit: '° C'
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
    this._api.getSensor(this._route.snapshot.paramMap.get('sensorId')).subscribe((sensor: Sensor) => {
      this.sensor = sensor
    })

    this.getHistoryData()
  }
  
  ngAfterViewInit() {
    // setup graph
    this.lineChartObj = new Chart(this.lineChartElRef.nativeElement, this._chartConfigs);
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
    const timeNow = moment()
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
      case '30D':
        params['timestamp'] = `${timeNow.subtract({days: 30}).format()}`
        break;
    }
    console.log(params)

    this._api.getSensorHistory(this._route.snapshot.paramMap.get('sensorId'), params).subscribe((sensorReadings: SensorReading[]) => {
      console.log(sensorReadings)
      // Process values for the graph
      const dataSeries = []
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
        case '30D':
          binSize = 60 * 12 // 12 H
          break;
      }
      for (var record of sensorReadings) {
        const minutesDiff = Math.round(moment(record.timestamp).diff(timeNow) / 60000) // difference in minutes
        const binIdx = Math.round(minutesDiff / binSize)

        const datapoint = {
          x: record.value,
          y: moment(record.timestamp).toISOString()
        }

        if (dataSeries.length == binIdx) { // add new bin
          dataSeries.push(datapoint)
        } else { // update existing bin
          dataSeries[binIdx] = datapoint
        }
      }

      console.log(dataSeries)
      // display current value
      this.currentDataPoint = dataSeries[dataSeries.length - 1]

      // refresh chart
      this._chartConfigs.data.datasets[0].data = dataSeries
      this.lineChartObj.destroy()
      this.lineChartObj = new Chart(this.lineChartElRef.nativeElement, this._chartConfigs);

    })
  }

  // DEPRECATED
  private _fetchDataOld() {
    this._api.getSensorHistory(this._route.snapshot.paramMap.get('sensorId'), {scale: this.scaleSelected}).subscribe((sensorReadings: SensorReading[]) => {
      //Format date - group by: 1m, 5m, 20m, 10h
      const newData = sensorReadings.reduce((group, reading) => {
        let dateFormatted = moment(reading.timestamp).set({second:0, millisecond:0})
        let remainder = 0
        switch (this.scaleSelected) {
          case '1H':
            break;
          case '6H':
            remainder = 5 - (dateFormatted.minute() % 5);
            dateFormatted.add(remainder, "minutes")
            break;
          case '1D':
            remainder = 20 - (dateFormatted.minute() % 20);
            dateFormatted.add(remainder, "minutes")
            break;
          case '30D':
            remainder = 10 - (dateFormatted.hours() % 10);
            dateFormatted.add(remainder, "hours")
            break;
        }

        const groupRecord = group[dateFormatted.format()] || {y: dateFormatted, data: []}
        groupRecord.data.push(reading.value)
        group[dateFormatted.format()] = groupRecord
        return group
      }, {} )
      
      // average values
      const dataSeries = []
      for (var key in newData) {
        dataSeries.push({x: newData[key].y, y: newData[key].data.reduce((prev, curr) => prev += parseFloat(curr), 0) / newData[key].data.length})
      }

      // display current value
      this.currentDataPoint = dataSeries[dataSeries.length - 1]

      // refresh chart
      this._chartConfigs.data.datasets[0].data = dataSeries
      this.lineChartObj.destroy()
      this.lineChartObj = new Chart(this.lineChartElRef.nativeElement, this._chartConfigs);
    })
  }
}
