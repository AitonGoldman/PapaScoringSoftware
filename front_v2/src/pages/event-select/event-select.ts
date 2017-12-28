import { Component } from '@angular/core';
import { Platform, IonicPage, NavController, NavParams } from 'ionic-angular';

/**
 * Generated class for the EventSelectPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-select',
  templateUrl: 'event-select.html',
})
export class EventSelectPage {
    nextPage:string = null;
    constructor(public navCtrl: NavController, public navParams: NavParams,
                platform: Platform) {
            if(platform.is('mobile') == true){          
                this.nextPage='TabsPage';    
            } else {          
                this.nextPage='HomePage';         
            }                        
    }
    
    ionViewDidLoad() {
        console.log('ionViewDidLoad EventSelectPage');
    }

}
