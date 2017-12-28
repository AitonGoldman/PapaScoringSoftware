import { ViewChild, Component } from '@angular/core';
import { IonicPage, NavController, ViewController, NavParams, Tabs } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

/**
 * Generated class for the HomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({    
    segment: 'HomePage/:eventId'
})
@Component({
  selector: 'page-home',
  templateUrl: 'home.html',
})
export class HomePage extends PssPageComponent{
    @ViewChild('myTabs') tabRef: Tabs;    
    constructor(public navCtrl: NavController,
                public navParams: NavParams,              
                public eventAuth: EventAuthProvider,
                public viewCtrl: ViewController) {       
        super(eventAuth,navParams,'Home');
        //this.hideBackButton=true;
    }

    ionViewDidLoad() {
        console.log('ionViewDidLoad HomePage');        
    }
}
