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
        this.tournamentItems=this.tournamentSettings.getTournaments(this.eventId);
        //console.log(this.tournamentItems)
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

        if(this.tournamentsOrderList!=null){
             this.tournamentItems=this.tournamentItems.sort((n1,n2)=>{
                 if(this.tournamentsOrderList[n1.tournament_id]!=null && this.tournamentsOrderList[n2.tournament_id]!=null){
                     return this.tournamentsOrderList[n1.tournament_id].index - this.tournamentsOrderList[n2.tournament_id].index;
                 } else {
                     return 1;
                 }
                 
             })            
        }                        
        
        // on set Tournaments, we also set favorite tournament machines with a alphabetical sorted list of tournament machines - if not already set
        // remove favoriting options for machine results
        // 
        //
        //this.tournamentMachines = this.listOrderStorage.getFavoriteTournamentMachines(this.eventId);        
        console.log('almost almost sorting...');
        this.tournamentMachines = this.listOrderStorage.getList('QuickLinksPage','tournament_machines');
        console.log(this.tournamentMachines);
        if(this.tournamentMachines!=null){
            
            //this.tournamentMachinesOrderList = this.listOrderStorage.getList('QuickLinksPage','tournament_machines');            
            //this.tournamentMachines = this.generateListFromObj(this.tournamentMachines);
            //console.log('almost sorting...');s            
            this.tournamentMachines=this.tournamentMachines.sort((n1,n2)=>{                    
                if(n1.index>n2.index){
                    return 1
                } else {
                    return -1;
                }                   
            })                

            // if(this.tournamentMachinesOrderList!=null){
            //     console.log('sorting...');
            //     this.tournamentMachines=this.tournamentMachines.sort((n1,n2)=>{                    
            //         if(this.tournamentMachinesOrderList[n1.tournamentMachineId]!=null && this.tournamentMachinesOrderList[n2.tournamentMachineId]!=null){
            //             return this.tournamentMachinesOrderList[n1.tournamentMachineId].index - this.tournamentMachinesOrderList[n2.tournamentMachineId].index;
            //         } else {
            //             return -1;
            //         }                   
            //     })                
            // }
            console.log(this.tournamentMachines);
        }
        
        
        
    }
    getCsallback(pageName,args){        
        return ()=>{
            console.log("**************")                            
            // let toast = this.toastCtrl.create({
            //     message:  "Something went wrong.  Please try the quicklink again.",
            //     duration: 99000,
            //     position: 'top',
            //     showCloseButton: true,
            //     closeButtonText: " ",
            //     cssClass: "dangerToast"
            // });
            // toast.present();                                                                                    
        }            
    }
    getTournamentsAndSetLists(){
        this.listOrderStorage.wipeList('ScorekeeperMachineSelect')        
        this.pssApi.getAllTournamentsAndMachines(this.eventId)            
            .subscribe((result)=>{                    
                //this.tournamentItems==result.data;
                this.tournamentSettings.setTournaments(result.data);
                this.getAndOrderTournaments();
                this.listOrderStorage.storeQuickLinksMachineLists(result.data);
                this.getAndOrderTournaments();                
            })
    }
    publishQuickLinksPlayerPush(pageName,args){
        //this.tabRef.getByIndex(1).push(pageName,args,{animate:false});
        let tabs = this.navCtrl.parent;
        console.log('about to jump to warp speed')
        if(tabs.getByIndex(1)._views.length!=0){
            console.log("were okay....")
            this.navCtrl.parent.getByIndex(1).push(pageName,args,{animate:false}).then(()=>{
                tabs.getByIndex(1).last().showBackButton(false);
                tabs.select(1)
            })
            
            return
        }
        if(tabs.getByIndex(1)._views.length==0){
            // console.log("were moving right along")
            //  tabs.select(1).then(()=>{            
            //      this.navCtrl.parent.getByIndex(1).push(pageName,args,{animate:false}).then(()=>{
            //          tabs.getByIndex(1).last().showBackButton(false);                    
            //      })                            
            //  })
            console.log("were moving right along")                        
            tabs.select(1).then(()=>{
                //tabs.getByIndex(1).setPages([{page:"ResultsPage",params:args},{page:pageName,params:args}])
                this.showLoading("Please Wait");
                setTimeout(()=>{
                    tabs.getByIndex(1).setPages([{page:"ResultsPage",params:args},{page:pageName,params:args}]).then(()=>{
                        this.hideLoading();
                    })
                },2000);
            })            

            return
        }
        
        //let whatever_one = this.navCtrl.parent.getByIndex(1)._views;
        //console.log('---------------')
        //console.log(this.navCtrl.parent.getByIndex(1)._zone.isStable);
        //tabs.select(1).then(()=>{            
        //    setTimeout(this.getCallback(pageName,args),0)
            
        //})
        
        // this.navCtrl.parent.getByIndex(1).push(pageName,args,{animate:false}).then((data)=>{
        //     setTimeout(()=>{                
        //         setTimeout(()=>{
        //             tabs.getByIndex(1).push(pageName,args,{animate:false})
        //         },1000)
        //     },3000);
        // });
        
        //this.eventsService.publish('quicklinks:player:results-push',pageName, args);
    }
    //ionViewDidLoad(){
    //  this.tournamentItems=this.tournamentSettings.getTournaments(this.eventId);
    //}
    ionViewWillEnter() {        
            if(this.eventId==null){
                this.pushRootPage('EventSelectPage')
                return;
            }
        this.reorderEnabled=false;
        console.log('ionViewDidLoad QuickLinksPage');
        
        this.getAndOrderTournaments();
        if(this.tournamentItems==null){
            this.getTournamentsAndSetLists();
        }
        console.log('tournament itemss3');
        console.log(this.tournamentItems);
        // this.eventsService.subscribe('quickLinks:reload', (event)=>{
        //     //this.getAndOrderTournaments();
        //     console.log('got the message');
        // });

        // this.eventsService.subscribe('tab:reload', (event)=>{            
        //     console.log('got the message about the tab');
        // });               
        
        //this.getAndOrderTournaments()
        
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
        console.log(this.tournamentMachines);
        console.log(indexes)
        this.tournamentMachines = reorderArray(this.tournamentMachines, indexes);
        this.tournamentMachines.forEach((item,index)=>{
            item.index=index;
        }) 
        
        let tournamentMachinesListToStore = {}
        // this.tournamentMachines.forEach((item,index)=>{
        //     tournamentMachinesListToStore[item.tournamentMachineId]={index:index+1,tournamentMachineId:item.tournamentMachineId};
        // }) 
        //this.listOrderStorage.updateList('QuickLinksPage','tournament_machines',tournamentMachinesListToStore)
        this.listOrderStorage.updateList('QuickLinksPage','tournament_machines',this.tournamentMachines)
    }    
    
}
