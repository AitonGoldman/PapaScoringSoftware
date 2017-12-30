import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { CreateEditEntityComponent } from '../../components/create-edit-entity/create-edit-entity'


/**
 * Generated class for the CreateTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'CreateTournament/:targetEventId/:entityType/:actionType'
})
@Component({
  selector: 'page-create-tournament',
    templateUrl: '../../components/create-edit-entity/create-edit-entity.html'
})
export class CreateTournamentPage extends CreateEditEntityComponent {
    entityType:string='tournament';

    ionViewDidLoad() {
        console.log('ionViewDidLoad CreateTournamentPage');
    }

}
