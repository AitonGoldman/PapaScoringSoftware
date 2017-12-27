import { ViewChild, Component } from '@angular/core';
import { IonicPage, NavController, NavParams, Tabs } from 'ionic-angular';
import { TitleServiceProvider } from '../../providers/title-service/title-service';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

/**
 * Generated class for the HomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-home',
  templateUrl: 'home.html',
})
export class HomePage extends PssPageComponent{
  @ViewChild('myTabs') tabRef: Tabs;  
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public titleService:TitleServiceProvider,
              public eventAuth: EventAuthProvider) {
       super(eventAuth,navParams);      
       this.titleService.setTitle("Home");
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad HomePage');
  }
}
