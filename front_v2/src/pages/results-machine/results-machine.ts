import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ResultsMachinePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment : "MachineResults/:eventId/:eventName/:tournamentId/:tournamentName/:tournamentMachineId/:tournamentMachineName"
})
@Component({
  selector: 'page-results-machine',
  templateUrl: 'results-machine.html',
})
export class ResultsMachinePage  extends PssPageComponent {
    tournamentId:number = null;
    tournamentName:string = null;
    tournamentMachineId:number = null;
    tournamentMachineName:string=null;
    results:any=null;
    width:string="100%";
    maxScore=0;
    bigMaxScore=999999999;
    smallMaxScore=99999;
    generateGetTournamentMachineResultsProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            this.results=result.data.map((result)=>{
                if(result.score > this.maxScore){
                    this.maxScore=result.score;
                }
                return result;
            });
            console.log(this.maxScore);
        }
    }
 
    onReload(){
        this.pssApi.getTournamentMachineResults(this.eventId,this.tournamentId,this.tournamentMachineId)            
            .subscribe(this.generateGetTournamentMachineResultsProcessor())        
    }

    ionViewWillLoad() {
      console.log('ionViewDidLoad ResultsMachinePage');
        if(this.platform.is('mobile')==false){
            this.width='75%';
        }
        this.tournamentId=this.navParams.get('tournamentId');
        this.tournamentName=this.navParams.get('tournamentName');
        this.tournamentMachineId=this.navParams.get('tournamentMachineId');
        this.tournamentMachineName=this.navParams.get('tournamentMachineName');
        console.log(this.tournamentMachineName);
        this.pssApi.getTournamentMachineResults(this.eventId,this.tournamentId,this.tournamentMachineId)            
            .subscribe(this.generateGetTournamentMachineResultsProcessor())        
    }


}
