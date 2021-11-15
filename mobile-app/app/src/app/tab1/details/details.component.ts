import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NavController } from '@ionic/angular';

@Component({
  selector: 'app-details',
  templateUrl: './details.component.html',
  styleUrls: ['./details.component.scss'],
})
export class DetailsComponent implements OnInit {
  @ViewChild('pageHeader') pageHeader;
  public displayPageHeaderInToolbar: boolean = false;
  public seasonName: string = "hellooo "

  constructor(
    private _route: ActivatedRoute,
  ) { }

  ngOnInit() {
    let seasonID = this._route.snapshot.paramMap.get('seasonID')
    console.log(seasonID)
  }

  onScroll(evt) {
    this.displayPageHeaderInToolbar = this.pageHeader.nativeElement.getBoundingClientRect().top < 30;
  }
}
