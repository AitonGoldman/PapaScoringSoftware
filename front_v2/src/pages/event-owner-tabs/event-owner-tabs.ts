import { ViewChild, Component } from '@angular/core';
import { Tabs, IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the EventOwnerTabsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-owner-tabs',
  templateUrl: 'event-owner-tabs.html',
})
export class EventOwnerTabsPage extends PssPageComponent{
    @ViewChild('myTabs') tabRef: Tabs;

    ionViewDidLoad() {
        console.log('ionViewDidLoad EventOwnerTabsPage');
    }
    onTabSelect(){
        console.log('selected a tab!');
    }
    onTabChange(event){        
        console.log('changed a tab!');
        if (this.tabRef.getByIndex(event.index).canGoBack()){
            this.tabRef.getByIndex(event.index).popToRoot({animate:false});
        }
        let previousTab = this.tabRef.previousTab(false);
        if (previousTab && previousTab.canGoBack()){
            this.tabRef.previousTab().popToRoot({animate:false});
        }
    }    
}
