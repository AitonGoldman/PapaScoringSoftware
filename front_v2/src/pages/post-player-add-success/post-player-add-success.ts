import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { SuccessPage } from '../success/success'
/**
 * Generated class for the PostPlayerAddSuccessPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-post-player-add-success',
  templateUrl: '../success/success.html',
})
export class PostPlayerAddSuccessPage extends SuccessPage {
    postAddPlayerSuccess:boolean=true;
    playerId:number=null;
    picTaken:boolean=false;
    requirePic:boolean=false;
    generateGetAllEventPlayersWithNoPicsProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
            console.log('in check pic..')
            console.log(result.data)
            let player = result.data.filter((player)=>{
                if(player.player_id==this.playerId){
                    return true;
                } else {
                    return false;
                }
            });
            if(player.length==0){
                this.picTaken=true;
            }
            
        }
    }
    checkPicTaken(){
        this.pssApi.getEventPlayers(this.eventId,'no_pics')
            .subscribe(this.generateGetAllEventPlayersWithNoPicsProcessor())            

    }
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

        super.ionViewWillLoad();
        this.playerId = this.navParams.get('playerId');
        this.requirePic = this.navParams.get('requirePic');
        console.log('ionViewDidLoad PostPlayerAddSuccessPage');
    }    
}
