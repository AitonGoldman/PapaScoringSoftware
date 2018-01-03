import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { AddUserComponent } from '../../components/add-user/add-user'
/**
 * Generated class for the EventOwnerAddUserPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EventOwnerAddUser/:eventId'
})
@Component({
  selector: 'page-event-owner-add-user',
  templateUrl: '../../components/add-user/add-user.html',
})
export class EventOwnerAddUserPage extends AddUserComponent {
    destPageAfterSuccess:string = 'EventOwnerHomePage';    
}
