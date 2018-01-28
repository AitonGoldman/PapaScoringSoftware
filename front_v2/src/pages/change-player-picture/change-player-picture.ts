import { Component } from '@angular/core';
import { TakePicComponent } from '../../components/take-pic/take-pic'
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete';
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
export class ChangePlayerPicturePage extends AutoCompleteComponent {
    players:any = [];
    selectedPlayer:any = null;
    
    generateGetAllEventPlayersWithNoPicsProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
            this.players = result.data;
        }
    }
    onReload(){
        this.pssApi.getEventPlayers(this.eventId,'no_pics')
            .subscribe(this.generateGetAllEventPlayersWithNoPicsProcessor())            

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
