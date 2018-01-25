import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { TopThreePopoverComponent } from '../../components/top-three-popover/top-three-popover'

/**
 * Generated class for the ResultsTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment : "Results/:eventId/:eventName/:tournamentId/:tournamentName"
})

@Component({
  selector: 'page-results-tournament',
  templateUrl: 'results-tournament.html',
})

export class ResultsTournamentPage extends PssPageComponent {
    tournamentId:number = null;
    tournamentName:string = null;
    results:any = null;
    width:any = '100%';
    maxResultsToDisplay:number=0;

    onBump(){
        if(this.maxResultsToDisplay<this.results.length){
            this.maxResultsToDisplay=this.maxResultsToDisplay+50;
        }
    }
    onReload(){
        this.maxResultsToDisplay=50;
        this.pssApi.getTournamentResults(this.eventId,this.tournamentId)            
            .subscribe(this.generateGetTournamentResultsProcessor())        
    }
    generateGetTournamentResultsProcessor(){
        return (result) => {
            if(result == null){
                return;
            }
            this.results=result.data;
            this.maxResultsToDisplay=50;
            this.results.map((result)=>{
                
                if(result.top_machines!=null){
                    result.topMachineStrings=[];
                    result.top_machines.forEach((top_machine,index)=>{
                        result.topMachineStrings.push(top_machine.abbreviation)
                    })
                    result.topMachineString=result.topMachineStrings.join('/');
                }
                
                return result;
            })
        }
    }
 
    ionViewDidLoad() {
        console.log('done loading and now publishing...')
        this.eventsService.publish('results-tournaments:done-loading');
    }
    
    ionViewWillLoad() {
        console.log('ionViewDidLoad ResultsTournamentPage');
        if(this.platform.is('mobile')==false){            
            this.width='75%';
        }
        this.tournamentId=this.navParams.get('tournamentId');
        this.tournamentName=this.navParams.get('tournamentName');

        this.pssApi.getTournamentResults(this.eventId,this.tournamentId)            
            .subscribe(this.generateGetTournamentResultsProcessor())        
    }
    showTopThreeMachines(event,machines){
        let linkParams = this.buildNavParams({tournamentId:this.tournamentId,tournamentName:this.tournamentName})        
        let popover = this.popoverCtrl.create(TopThreePopoverComponent,
                                              {'machines':machines,
                                               'linkParams': linkParams,
                                               'tabNavCtrl': this.navCtrl});
        popover.present({
            ev: event
        });
    }
}

