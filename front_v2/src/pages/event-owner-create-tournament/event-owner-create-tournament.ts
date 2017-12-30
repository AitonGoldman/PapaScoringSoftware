import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { CreateEditEntityComponent } from '../../components/create-edit-entity/create-edit-entity'

/**
 * Generated class for the EventOwnerCreateTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EventOwnerCreateTournament/:eventId/:entityType/:actionType'
})
@Component({
    selector: 'page-event-owner-create-tournament',
    templateUrl: '../../components/create-edit-entity/create-edit-entity.html'
})
export class EventOwnerCreateTournamentPage extends CreateEditEntityComponent{
    entityType:string='tournament';
    destPageAfterSuccess:string = "EventOwnerHomePage";
    ionViewDidLoad() {
        console.log('ionViewDidLoad EventOwnerCreateTournamentPage');
    }
}
