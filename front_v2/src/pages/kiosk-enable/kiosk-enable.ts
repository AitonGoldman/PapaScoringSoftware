import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the KioskEnablePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-kiosk-enable',
  templateUrl: 'kiosk-enable.html',
})
export class KioskEnablePage  extends PssPageComponent {

  ionViewWillLoad() {
      this.tournamentSettings.setKioskMode();
      console.log('ionViewDidLoad KioskEnablePage');
  }

}
