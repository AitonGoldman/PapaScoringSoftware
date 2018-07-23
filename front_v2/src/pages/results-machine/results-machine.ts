import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'

/**
 * Generated class for the ResultsMachinePage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-results-machine',
  templateUrl: 'results-machine.html',
})
export class ResultsMachinePage  extends PssPageComponent {
    displayFavoriteMachine:boolean = false;
    tournamentId:number = null;
    tournamentName:string = null;
    tournamentMachineId:number = null;
    tournamentMachineName:string=null;
    results:any=null;
    width:string="100%";
    maxScore=0;
    bigMaxScore=999999999;
    smallMaxScore=99999;
    loaded:boolean=false;

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
    markAsFavorite(){
        this.listOrderStorage.addFavoriteTournamentMachine(this.eventId,
                                                           this.tournamentMachineId,
                                                           this.tournamentMachineName,
                                                           this.tournamentId,
                                                           this.tournamentName)
        this.displayFavoriteMachine=false;
    }
    ionViewWillEnter(){
        
        if(this.loaded==false){
        if(this.eventId==null){
            this.pushRootPage('EventSelectPage')
            return;
        }

            console.log('results machine on enter...')
            let tournamentMachineId = this.navParams.get('tournamentMachineId');
            let favoriteMachines = this.listOrderStorage.getFavoriteTournamentMachines(this.eventId)
            this.displayFavoriteMachine=favoriteMachines==null || favoriteMachines[tournamentMachineId]==null
            if(this.platform.is('mobile')==false){
                this.width='75%';
            }
            this.tournamentMachineId=this.navParams.get('tournamentMachineId');
            this.tournamentId=this.navParams.get('tournamentId');
            this.tournamentName=this.navParams.get('tournamentName');
            this.tournamentMachineName=this.navParams.get('tournamentMachineName');
            console.log(this.tournamentMachineName);
            this.pssApi.getTournamentMachineResults(this.eventId,this.tournamentId,this.tournamentMachineId)            
                .subscribe(this.generateGetTournamentMachineResultsProcessor())                    
        }
        this.loaded=true;
    }
    ionViewWillLoad() {
      console.log('ionViewDidLoad ResultsMachinePage');
    }


}
