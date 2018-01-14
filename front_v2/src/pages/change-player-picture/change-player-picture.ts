import { Component } from '@angular/core';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { TakePicComponent } from '../../components/take-pic/take-pic'

import { AutoCompleteProvider } from '../../providers/auto-complete/auto-complete';
import { ModalController, Platform, App, NavParams, NavController } from 'ionic-angular';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { PssApiProvider } from '../../providers/pss-api/pss-api';

import { ActionSheetController } from 'ionic-angular'
import { NotificationsService } from 'angular2-notifications';
import { IonicPage } from 'ionic-angular';

/**
 * Generated class for the ChangePlayerPicturePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-change-player-picture',
  templateUrl: 'change-player-picture.html',
})
export class ChangePlayerPicturePage extends PssPageComponent {
    players:any = [];
    selectedPlayer:any = null;
    constructor(public autoCompleteProvider:AutoCompleteProvider,
                public eventAuth: EventAuthProvider,
                public navParams: NavParams,
                public navCtrl: NavController,
                public appCtrl: App,
                public pssApi: PssApiProvider,
                public platform: Platform,                
                public actionSheetCtrl: ActionSheetController,
                public notificationsService: NotificationsService,                
                public modalCtrl: ModalController){
        super(eventAuth,navParams,
              navCtrl,appCtrl,
              pssApi,platform,
              notificationsService,
              actionSheetCtrl);
    }
    
    generateGetAllEventPlayersWithNoPicsProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
            this.players = result.data;
        }
    }
    
    ionViewWillLoad() {
        this.pssApi.getEventPlayers(this.eventId,'no_pics')
            .subscribe(this.generateGetAllEventPlayersWithNoPicsProcessor())            

        console.log('ionViewDidLoad ChangePlayerPicturePage');
    }
    generateEditPlayerProcessor(){
        return (result)=>{
            if(result==null){
                return
            }
            console.log('in generatedEditPlayerProcessor')
            this.pssApi.getEventPlayers(this.eventId,'no_pics')
                .subscribe(this.generateGetAllEventPlayersWithNoPicsProcessor())                                    
        }
    }
    takePicture(player){
        this.selectedPlayer=player;
        let profileModal = this.modalCtrl.create(TakePicComponent, { userId: 8675309 });
        profileModal.onDidDismiss(data => {
            console.log('in modal...');
            console.log(data);
            if(data==null){
                return
            }            
            this.selectedPlayer.has_pic=true;
            this.selectedPlayer.img_file=data;
            this.pssApi.editPlayer(this.selectedPlayer,this.eventId)
                .subscribe(this.generateEditPlayerProcessor())                    
            
        });
        profileModal.present();
    }

}
