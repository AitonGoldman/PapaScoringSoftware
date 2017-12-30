import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { TournamentComponent } from '../../components/tournament/tournament'


/**
 * Generated class for the CreateTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'CreateTournament/:eventId/:actionType'
})
@Component({
  selector: 'page-create-tournament',
    templateUrl: '../../components/create-edit-entity/create-edit-entity.html'
})
export class CreateTournamentPage extends TournamentComponent {
    destPageAfterSuccess:string="TournamentDirectorHomePage";
    wizardModeNextPage:string="TournamentMachinesPage";        

    ionViewDidLoad() {
        console.log('ionViewDidLoad CreateTournamentPage');
    }

}
