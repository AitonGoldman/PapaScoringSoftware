import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the FinalsBootstrapResolveTiebreakerPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-finals-bootstrap-resolve-tiebreaker',
  templateUrl: 'finals-bootstrap-resolve-tiebreaker.html',
})
export class FinalsBootstrapResolveTiebreakerPage extends PssPageComponent {
    tiebreaker:any=null;    
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad FinalsBootstrapPage');
        this.tiebreaker=this.navParams.get('tiebreaker')
    }
    generateSaveFinalsBootstrapTiebreakersScoreProcessor(){
        return (result)=>{
            if(result==null){
                return;
            }
            //this.tiebreaker=result.data;
            console.log(result)
            let msg="Score Saved";
            if(result.data.completed){
                msg="Tiebreaker Completed";
            }
            let toast = this.toastCtrl.create({
                message:  msg,
                duration: 99000,
                position: 'top',
                showCloseButton: true,
                closeButtonText: " ",
                cssClass: "successToast"
            });            
            toast.present();                                                    
            
        }
    }

    
    saveScores(){
        this.pssApi.saveFinalsBootstrapTiebreakersScore(this.tiebreaker,this.eventId,this.tiebreaker.tiebreaker_id)
            .subscribe(this.generateSaveFinalsBootstrapTiebreakersScoreProcessor())                                                          

    }
}
