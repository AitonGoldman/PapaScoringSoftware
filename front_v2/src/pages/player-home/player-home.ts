import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the PlayerHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'PlayerHomePage/:eventId'
})
@Component({
  selector: 'page-player-home',
  templateUrl: 'player-home.html',
})
export class PlayerHomePage extends PssPageComponent {

  ionViewDidLoad() {
    console.log('ionViewDidLoad PlayerHomePage');
  }

}
