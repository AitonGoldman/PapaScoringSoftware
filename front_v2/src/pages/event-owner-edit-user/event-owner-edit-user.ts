import { Component } from '@angular/core';
import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';

import { ActionSheetController } from 'ionic-angular'
import { NotificationsService } from 'angular2-notifications';
import { EditUserComponent } from '../../components/edit-user/edit-user'

import { IonicPage } from 'ionic-angular';

/**
 * Generated class for the EventOwnerEditUserPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment:'EventOwnerEditUser/:eventId'
})
@Component({
  selector: 'page-event-owner-edit-user',
  templateUrl: '../../components/edit-user/edit-user.html',
})
export class EventOwnerEditUserPage extends EditUserComponent {
    destPageAfterSuccess:any='EventOwnerHomePage';
    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                public actionSheetCtrl: ActionSheetController,
                public notificationsService: NotificationsService) {
        super( autoCompleteProvider,
               eventAuth,
               navParams,
               navCtrl,
               appCtrl,
               pssApi,
               platform,               
               actionSheetCtrl,
               notificationsService)
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad EventOwnerEditUserPage');
  }

}
