import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DetailsComponent } from './details/details.component';
import { SensorComponent } from './sensor/sensor.component';
import { Tab1Page } from './tab1.page';

const routes: Routes = [
  {path: '', component: Tab1Page},
  {path: ':seasonID/details', component: DetailsComponent},
  {path: 'sensors/:sensorId', component: SensorComponent},
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class Tab1PageRoutingModule {}
