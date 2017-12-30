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
        };
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
