import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { TournamentComponent } from '../../components/tournament/tournament'

/**
 * Generated class for the EventOwnerCreateTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EventOwnerCreateTournament/:eventId/:actionType/:wizardMode'
})
@Component({
    selector: 'page-event-owner-create-tournament',
    templateUrl: '../../components/create-edit-entity/create-edit-entity.html'
})
export class EventOwnerCreateTournamentPage extends TournamentComponent{
    destPageAfterSuccess:string="EventOwnerHomePage";
    wizardModeNextPage:string="EventOwnerTournamentMachinesPage";        
    ionViewDidLoad() {
        console.log('ionViewDidLoad EventOwnerCreateTournamentPage');
    }
}
