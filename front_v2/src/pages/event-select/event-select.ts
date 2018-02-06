import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the EventSelectPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-select',
  templateUrl: 'event-select.html',
})
export class EventSelectPage extends PssPageComponent {
    nextPage:string = null;
    events = [];

    generateGetAllEventsProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            this.events=result.data;
            this.tournamentSettings.setEvents(this.events);
        };
    }

    gotoEvent(eventId,eventName){
        this.eventAuth.logoutEventOwner();
        let nextPage = '';
        let tabIndex=null;
        if(this.platform.is('mobile') == true){
            nextPage = 'TabsPage';
            tabIndex = 0;
        } else {
            nextPage = this.getHomePageString(eventId);
        }          
        
        this.pushRootPage(nextPage,{'eventId':eventId,'eventName':eventName});

    }
    
    
    ionViewWillLoad() {                
        
        this.pssApi.getAllEvents({})
            .subscribe(this.generateGetAllEventsProcessor())    
        
        if(this.platform.is('mobile') == true){          
            this.nextPage='TabsPage';    
        } else {          
            this.nextPage=this.getHomePageString();         
        }                                
        console.log('ionViewDidLoad EventSelectPage');
        
    }

}
