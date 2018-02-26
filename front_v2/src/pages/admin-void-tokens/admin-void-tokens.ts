import { Component } from '@angular/core';
import { AutoCompleteComponent } from '../../components/auto-complete/auto-complete'
import { IonicPage } from 'ionic-angular';

/**
 * Generated class for the AdminVoidTokensPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-admin-void-tokens',
  templateUrl: 'admin-void-tokens.html',
})
export class AdminVoidTokensPage extends AutoCompleteComponent {
    tokenCount:number = 0;
    selectedTournamentId:any = null;
    ionViewWillLoad() {
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }
        
        this.autoCompleteProvider.initializeAutoComplete(null,
                                                         null,
                                                         null,
                                                         this.eventId);      
        
        console.log('ionViewDidLoad AdminVoidTokensPage');
    }
    onFocus(){
        console.log('in onFocus..')
        this.selectedPlayer=null;                
    }
    generateAdminVoidTokenProcessor(){
        return ((result)=>{
            if(result == null){
                return
            }
            // let toast = this.toastCtrl.create({
            //     message:  this.tokenCount+" unused tokens have been voided",
            //     duration: 99000,
            //     position: 'top',
            //     showCloseButton: true,
            //     closeButtonText: " ",
            //     cssClass: "successToast"
            // });
            // toast.present();                    
            this.pssToast.showToast(this.tokenCount+" unused tokens have been voided",4000,"successToast")
            
        })
    }    
    onSubmit(){
        this.pssApi.adminVoidTicket({},this.eventId,this.selectedPlayer.player_id,this.selectedTournamentId,this.tokenCount)
            .subscribe(this.generateAdminVoidTokenProcessor())                                                  

    }
    
}