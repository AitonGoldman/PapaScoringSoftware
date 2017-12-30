import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
/**
 * Generated class for the EventOwnerHomePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-owner-home',
  templateUrl: 'event-owner-home.html',
})
export class EventOwnerHomePage extends PssPageComponent {
    eventsAndTournaments:any;
    generateGetAllEventsAndTournamentsProcessor(){
        return (result) => {            
            if(result == null){
                return;
            }
            console.log('got back tournaments and events...');            
            this.eventsAndTournaments=result.data;
            console.log(this.eventsAndTournaments);
        };
    }

    ionViewWillLoad() {
        this.pssApi.getAllEventsAndTournaments()
            .subscribe(this.generateGetAllEventsAndTournamentsProcessor())    
        console.log('ionViewDidLoad EventOwnerHomePage');
    }

}
