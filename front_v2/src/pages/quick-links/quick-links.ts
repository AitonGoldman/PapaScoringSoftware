import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { reorderArray } from 'ionic-angular';

/**
 * Generated class for the QuickLinksPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-quick-links',
  templateUrl: 'quick-links.html',
})
export class QuickLinksPage extends PssPageComponent {  
    reorderEnabled:boolean = false;
    

    // items=[{'title':'Results - Classics I',
    //         'icon':'md-clipboard'},
    //        {'title':'Results - Main A',
    //         'icon':'md-clipboard'},
    //        {'title':'Queues - Classics I',
    //         'icon':'git-branch'},
    //        {'title':'Queues - Classics I',
    //         'icon':'git-branch'},           
    //       ];
    tournamentItems:any=[];
    tournamentsOrderList:any=null;
    tournamentMachinesOrderList:any=null;
  
    tournamentMachines:any=[];
    tournamentsMachinesList:any=null;
    
    getAndOrderTournaments(){
        this.tournamentItems=this.tournamentSettings.getTournaments();
        if(this.tournamentItems==null){            
            return;
        }
        
        this.tournamentItems.map((item)=>{            
            item.icon='clipboard';            
            item.title=item.tournament_name;
            item.type='tournament';
            item.uid=item.tournament_id;
        })        
        this.tournamentsOrderList = this.listOrderStorage.getList('QuickLinksPage','tournaments');
        if(this.tournamentsOrderList==null){
            return;
        }                        
        
        this.tournamentItems=this.tournamentItems.sort((n1,n2)=>{
            return this.tournamentsOrderList[n1.tournament_id].index - this.tournamentsOrderList[n2.tournament_id].index;
        })

        this.tournamentMachines = this.listOrderStorage.getFavoriteTournamentMachines(this.eventId);
        console.log(this.tournamentMachines);
        if(this.tournamentMachines==null){
            return;
        }
        this.tournamentMachines = this.generateListFromObj(this.tournamentMachines);
        this.tournamentMachinesOrderList = this.listOrderStorage.getList('QuickLinksPage','tournament_machines');
        if(this.tournamentMachinesOrderList==null){
            return;
        }                        
        
        this.tournamentMachines=this.tournamentMachines.sort((n1,n2)=>{
            return this.tournamentMachinesOrderList[n1.tournamentMachineId].index - this.tournamentsOrderList[n2.tournamentMachineId].index;
        })
        
        
    }
    ionViewWillLoad() {        
        console.log('ionViewDidLoad QuickLinksPage');
        this.eventsService.subscribe('quickLinks:reload', (event)=>{
            this.getAndOrderTournaments();
            console.log('got the message');
        });               
        this.getAndOrderTournaments()
        
    }
    reorderTournamentItems(indexes) {
        
        this.tournamentItems = reorderArray(this.tournamentItems, indexes);
        
        let tournamentsListToStore = {}
        this.tournamentItems.forEach((item,index)=>{
            tournamentsListToStore[item.tournament_id]={index:index+1,tournamentId:item.tournament_id};
        }) 
        this.listOrderStorage.updateList('QuickLinksPage','tournaments',tournamentsListToStore)
    }
    reorderMachineItems(indexes) {
        
        this.tournamentMachines = reorderArray(this.tournamentMachines, indexes);
        
        let tournamentMachinesListToStore = {}
        this.tournamentMachines.forEach((item,index)=>{
            tournamentMachinesListToStore[item.tournamentMachineId]={index:index+1,tournamentMachineId:item.tournamentMachineId};
        }) 
        this.listOrderStorage.updateList('QuickLinksPage','tournament_machines',tournamentMachinesListToStore)
    }    
    
}
