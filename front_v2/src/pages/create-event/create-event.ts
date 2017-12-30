import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { CreateEditEntityComponent } from '../../components/create-edit-entity/create-edit-entity'

/**
 * Generated class for the CreateEventPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'CreateEventPage/:eventId/:actionType'    
})
@Component({
  selector: 'page-create-event',
  templateUrl: '../../components/create-edit-entity/create-edit-entity.html',
})
export class CreateEventPage extends CreateEditEntityComponent{    
    entityType:string='event';
    ionViewDidLoad() {
        console.log('ionViewDidLoad CreateEventPage');
    }

}
