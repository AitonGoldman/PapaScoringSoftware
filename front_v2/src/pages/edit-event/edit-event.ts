import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { EventComponent } from '../../components/event/event'

/**
 * Generated class for the EditEventPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EditEventPage/:actionType/:eventId'    
})
@Component({
  selector: 'page-edit-event',
  templateUrl: '../../components/create-edit-entity/create-edit-entity.html',  
})
export class EditEventPage extends EventComponent{
    destPageAfterSuccess:string="EventOwnerHomePage";

    ionViewDidLoad() {
        console.log('ionViewDidLoad EditEventPage');
    }
}
