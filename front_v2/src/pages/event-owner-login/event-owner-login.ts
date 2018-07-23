import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { LoginPage } from '../login/login'
/**
 * Generated class for the EventOwnerLoginPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-owner-login',
  templateUrl: 'event-owner-login.html',
})
export class EventOwnerLoginPage extends LoginPage {

  ionViewDidLoad() {
    console.log('ionViewDidLoad EventOwnerLoginPage');
  }

}
