import { ViewChild, Component } from '@angular/core';
import { Tabs, PopoverController, IonicPage, NavController, NavParams } from 'ionic-angular';
import { TitleServiceProvider } from '../../providers/title-service/title-service';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the TabsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-tabs',
  templateUrl: 'tabs.html',
})
export class TabsPage extends PssPageComponent {
    @ViewChild('myTabs') tabRef: Tabs;
    roleName:string = "blah";    
    constructor(public navCtrl: NavController,
                public navParams: NavParams,
                public titleService: TitleServiceProvider,
                public popoverCtrl: PopoverController,                
                public eventAuth: EventAuthProvider) {
        super(eventAuth,navParams);
        console.log('in tabs, event id is ... '+this.eventId);
        let roleName = this.eventAuth.getRoleName(this.eventId);
        this.roleName = roleName ? roleName : 'Home'
    }
    ionViewDidLoad() {
        console.log('ionViewDidLoad TabsPage');
    }
    // presentPopover(myEvent) {
    //     let popover = this.popoverCtrl.create(QuicklinksComponent);
    //     popover.present({
    //         ev: myEvent     
    //     });
    // }
    
    onTabChange(event){        
        if (this.tabRef.getByIndex(event.index).canGoBack()){
            this.tabRef.getByIndex(event.index).first();
        }                
    }

}
