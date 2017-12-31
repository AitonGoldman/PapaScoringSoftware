import { Component } from '@angular/core';
import { IonicPage} from 'ionic-angular';
import { TournamentComponent } from '../../components/tournament/tournament'

/**
 * Generated class for the EditTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EditTournament/:eventId/:tournamentId/:actionType'
})
@Component({
  selector: 'page-edit-tournament',
  templateUrl: '../../components/create-edit-entity/create-edit-entity.html',    
})
export class EditTournamentPage extends TournamentComponent {
    destPageAfterSuccess:string="TournamentDirectorHomePage";
    entityType:string = "tournament"
  ionViewDidLoad() {
    console.log('ionViewDidLoad EditTournamentPage');
  }

}
