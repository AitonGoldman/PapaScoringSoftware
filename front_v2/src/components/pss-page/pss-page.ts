import { Component } from '@angular/core';
import { NavParams } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

/**
 * Generated class for the TopNavComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'pss-page',
  templateUrl: 'pss-page.html'
})
export class PssPageComponent {
    eventId:number = null;
    eventName:string = null;
    hideBackButton:boolean = false;
  constructor(public eventAuth: EventAuthProvider,
              public navParams: NavParams,
              public title?:string) {
      this.eventId = navParams.get('eventId');
      this.eventName = navParams.get('eventName');
      console.log('Hello PssPageComponent Component');
  }
  buildNavParams(params){
   params['eventId'] = this.eventId;
   params['eventName'] = this.eventName;
   return params;
  }
    hideTheBackButton(){
        this.hideBackButton=true;
    }
}
