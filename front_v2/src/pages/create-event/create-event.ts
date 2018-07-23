import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { EventComponent } from '../../components/event/event'

/**
 * Generated class for the CreateEventPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-create-event',
  templateUrl: '../../components/create-edit-entity/create-edit-entity.html',
})
export class CreateEventPage extends EventComponent{    
    destPageAfterSuccess:string="EventOwnerHomePage";
    wizardModeNextPage:string="TournamentPage";
    
    ionViewDidLoad() {
        console.log('ionViewDidLoad CreateEventPage');
    }

}
