import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth'
import { PssPageComponent } from '../../components/pss-page/pss-page'
/**
 * Generated class for the KioskHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:"/kiosk-home/:eventId/:eventName"
})
@Component({
  selector: 'page-kiosk-home',
  templateUrl: 'kiosk-home.html',
})
export class KioskHomePage extends PssPageComponent{    

  ionViewDidLoad() {
    console.log('ionViewDidLoad KioskHomePage');
  }

}
