import { ViewChild, Component } from '@angular/core';
import { IonicPage, Tabs } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the HomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({    
    segment: 'HomePage/:eventId/:eventName'
})
@Component({
  selector: 'page-home',
  templateUrl: 'home.html',
})
export class HomePage extends PssPageComponent{
    @ViewChild('myTabs') tabRef: Tabs;    
    numberCols:number=3;
    numberMachines:number=16;
    round:any=Math.round;
    homeHelpExtra:any={expanded:false};
    
    ionViewDidLoad() {
        console.log('ionViewDidLoad HomePage');        
    }
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }
        console.log('ionViewDidLoad HomePage');        
    }
    
    testClick(){
        alert('hi there');
    }
}
