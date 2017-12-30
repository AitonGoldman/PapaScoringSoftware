import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { TournamentMachinesComponent } from '../../components/tournament-machines/tournament-machines'

/**
 * Generated class for the TournamentMachinesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'TournamentMachines/:eventId/:tournamentId'
})
@Component({
    selector: 'page-tournament-machines',
    templateUrl: '../../components/tournament-machines/tournament-machines.html',
})

export class TournamentMachinesPage extends TournamentMachinesComponent {
    destPageAfterSuccess:string = 'TournamentDirectorHomePage';    
}
