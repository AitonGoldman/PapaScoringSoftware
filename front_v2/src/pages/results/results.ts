import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

/**
 * Generated class for the ResultsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-results',
  templateUrl: 'results.html',
})
export class ResultsPage extends PssPageComponent {

    constructor(public navCtrl: NavController,
                public navParams: NavParams,
                public eventAuth: EventAuthProvider) {
              super(eventAuth,navParams);            
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ResultsPage');
  }

}
