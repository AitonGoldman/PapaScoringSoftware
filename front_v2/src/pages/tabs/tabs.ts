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
    ionViewDidLoad(){
        //this.tabRef.getByIndex(1).setRoot('ResultsPage',this.buildNavParams({}));
    }
    ionViewWillLoad() {        
        let roleName = this.eventAuth.getRoleName(this.eventId);
        this.roleName = roleName ? roleName : 'Home';
        console.log('ionViewDidLoad TabsPage');
        this.eventsService.subscribe('quicklinks:player:results-push',(pageName,args)=>{            
            console.log('QUICKLINKS RECIEVED FOR '+pageName)
            this.tabRef.getByIndex(1).push(pageName,args,{animate:false}).then((data)=>{                
                this.tabRef.getByIndex(1).last().showBackButton(false);                
                this.tabRef.select(1);                
            });
            
        });                
        
    }
    ionViewWillUnload() {
        console.log('unloading tabs...')
    }

    // presentPopover(myEvent) {
    //     let popover = this.popoverCtrl.create(QuicklinksComponent);
    //     popover.present({
    //         ev: myEvent     
    //     });
    // }
    showTopThreeMachines(event){
        let popover = this.popoverCtrl.create(TopThreePopoverComponent);
        popover.present({
            ev: event
        });
    }
    onTabClick(){
        //let previousTab = this.tabRef.previousTab(true);
        
        console.log('click...')
        //this.tabRef.getByIndex(event.index).push('ResultsPage',{eventId:this.eventId,eventName:this.eventName}).then((data)=>{
        //    this.tabRef.select(event.index);
        //})        
        
    }
    onTabChange(event){                
        console.log('changed a tab!');        
        let previousTab = this.tabRef.previousTab(false);
        console.log(previousTab);
        // if(previousTab!=null && previousTab.index!=3){
        //     //console.log('poop!');
        //     this.tabRef.getByIndex(event.index).popToRoot({})
        // }
                
        
        if (this.tabRef.getByIndex(event.index).canGoBack()==true){            
            //console.log('popping...')            
            //this.tabRef.getByIndex(event.index).popToRoot({}).then((data)=>{
        //let rootPage = this.tabRef.getByIndex(event.index).root;
        //this.eventsService.publish('tab:reload:'+rootPage);            
            if(previousTab.index!=3){
                console.log('poop!');
                //this.tabRef.select(event.index);
            }
            
            //});
        }
        //Let rootPage = this.tabRef.getByIndex(event.index).root;
        //let rootParams = this.tabRef.getByIndex(event.index).rootParams;       
        //this.tabRef.getByIndex(event.index).push('ResultsPage',rootParams);
        //this.tabRef.getByIndex(event.index).popToRoot({animate:false});
        
//        let previousTab = this.tabRef.previousTab(true);        
        if (previousTab && previousTab.canGoBack()){
            console.log('popping previous...')
            //let previousView = previousTab.getViews()[0];
            //previousTab.push('TournamentDirectorHomePage')
        }
    }
    onHelp(){        
        console.log(this.tabRef.getSelected());        
    }
}
