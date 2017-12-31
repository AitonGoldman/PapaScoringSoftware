import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { TournamentComponent } from '../../components/tournament/tournament'

/**
 * Generated class for the EventOwnerEditTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EventOwnerEditTournament/:eventId/:tournamentId/:actionType'
})
@Component({
  selector: 'page-event-owner-edit-tournament',
  templateUrl: '../../components/create-edit-entity/create-edit-entity.html',    
})
export class EventOwnerEditTournamentPage extends TournamentComponent {
    destPageAfterSuccess:string="EventOwnerHomePage";
    entityType:string = "tournament"

  ionViewDidLoad() {
    console.log('ionViewDidLoad EventOwnerEditTournamentPage');
  }

}
