import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ScorekeeperHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-scorekeeper-home',
  templateUrl: 'scorekeeper-home.html',
})
export class ScorekeeperHomePage extends PssPageComponent{

  ionViewDidLoad() {
    console.log('ionViewDidLoad ScorekeeperHomePage');
  }

}
