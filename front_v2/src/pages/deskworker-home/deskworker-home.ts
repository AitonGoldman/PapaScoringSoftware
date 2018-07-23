import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the DeskworkerHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-deskworker-home',
  templateUrl: 'deskworker-home.html',
})
export class DeskworkerHomePage extends PssPageComponent {

  ionViewDidLoad() {
      if(this.eventId==null){
          this.pushRootPage('EventSelectPage')
          return;
      }      
  }
}
