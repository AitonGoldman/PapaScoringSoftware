import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { TopThreePopoverComponent } from '../../components/top-three-popover/top-three-popover'

/**
 * Generated class for the ResultsTournamentPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()

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
    loaded:boolean=false;
    tournamentSettings:any=null;
    setRowColor(e,result){
        let rankRestriction=false;
        console.log(this.tournamentSettings);
        if(this.tournamentSettings.finals_style=="PAPA"){
            rankRestriction=this.tournamentSettings.number_of_qualifiers;
        } else {
            rankRestriction=this.tournamentSettings.number_of_qualifiers_for_a_when_finals_style_is_ppo;
        }
        console.log('rankrestriction is..');
        console.log(rankRestriction);
        if(result.ifpa_ranking_restricted==true && result.rank > rankRestriction){
            return '#FF6347';
        }                
        if(e==true){
            return '#EEEEEE'
        }
        if(e!=true){
            return null
        };
    }
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
            this.tournamentSettings=result.tournament;
                
            this.maxResultsToDisplay=50;
            this.results.map((result)=>{                
                if(result.top_machines!=null){
                    result.topMachineStrings=[];
                    console.log('poop');                    
                    result.top_machines.forEach((top_machine,index)=>{
                        console.log(top_machine)
                        result.topMachineStrings.push("#"+top_machine.rank+" on "+top_machine.abbreviation)
                    })
                    if(this.platform.is("mobile")){
                        result.topMachineString="top 3";
                    } else {
                        result.topMachineString=result.topMachineStrings.join(' / ');
                    }

                    
                }
                
                return result;
            })
        }
    }
 
    ionViewDidLoad() {
        console.log('done loading and now publishing...')
        this.eventsService.publish('results-tournaments:done-loading');
        if(this.platform.is('core')==true || this.platform.is('tablet')==true){
            this.contentWidth='90%'
        }
        
    }
    
    ionViewWillEnter() {
        console.log('ionViewDidLoad ResultsTournamentPage');
        if(this.loaded==false){
            if(this.eventId==null){
                this.pushRootPage('EventSelectPage')
                return;
            }
            if(this.platform.is('mobile')==false){            
                this.width='100%';
            }
            this.tournamentId=this.navParams.get('tournamentId');
            this.tournamentName=this.navParams.get('tournamentName');

            this.pssApi.getTournamentResults(this.eventId,this.tournamentId)            
                .subscribe(this.generateGetTournamentResultsProcessor())        
        }
        this.loaded=true;
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

