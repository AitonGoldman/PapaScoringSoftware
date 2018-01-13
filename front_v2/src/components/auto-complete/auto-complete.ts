import { Component } from '@angular/core';
import { PssPageComponent } from '../../components/pss-page/pss-page'

import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { ModalController, Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';
import { AlertController } from 'ionic-angular';

import { ActionSheetController } from 'ionic-angular'
import { NotificationsService } from 'angular2-notifications';

//import { IonicPage } from 'ionic-angular';

/**
 * Generated class for the AutoCompleteComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'auto-complete',
  templateUrl: 'auto-complete.html'
})
export class AutoCompleteComponent extends PssPageComponent {

  text: string;

    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                public actionSheetCtrl: ActionSheetController,
                public notificationsService: NotificationsService,
                public alertCtrl: AlertController,
                public modalCtrl: ModalController){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              notificationsService);

    }
}
