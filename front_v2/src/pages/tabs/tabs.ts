import { ViewChild, Component } from '@angular/core';
import { Tabs, IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { TopThreePopoverComponent } from '../../components/top-three-popover/top-three-popover'

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
    ionViewWillLoad() {
        let roleName = this.eventAuth.getRoleName(this.eventId);
        this.roleName = roleName ? roleName : 'Home'

        console.log('ionViewDidLoad TabsPage');
    }
    // presentPopover(myEvent) {
    //     let popover = this.popoverCtrl.create(QuicklinksComponent);
    //     popover.present({
    //         ev: myEvent     
    //     });
    // }
    onTabSelect(){
        console.log('selected a tab!');
    }
    onQuickLinksSelect(){
        this.eventsService.publish('quickLinks:reload');
    }
    showTopThreeMachines(event){
        let popover = this.popoverCtrl.create(TopThreePopoverComponent);
        popover.present({
            ev: event
        });
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
    onHelp(){        
        console.log(this.tabRef.getSelected());        
    }
}
