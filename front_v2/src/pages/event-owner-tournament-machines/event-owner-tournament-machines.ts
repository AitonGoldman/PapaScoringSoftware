import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { TournamentMachinesComponent } from '../../components/tournament-machines/tournament-machines'

/**
 * Generated class for the EventOwnerTournamentMachinesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EventOwnerTournamentMachines/:eventId/:tournamentId'
})
@Component({
    selector: 'page-event-owner-tournament-machines',
    templateUrl: '../../components/tournament-machines/tournament-machines.html'
})
export class EventOwnerTournamentMachinesPage extends TournamentMachinesComponent{
    destPageAfterSuccess:string = 'EventOwnerHomePage';

}
