import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie';
import { ToastController } from 'ionic-angular';

/*
  Generated class for the ListOrderStorageProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class ListOrderStorageProvider {

    constructor(public http: HttpClient, public _cookieService:CookieService, private toastCtrl: ToastController) {
        console.log('Hello ListOrderStorageProvider Provider');
    }
    
    getList(pageName,listName){
        let listStorage = this._cookieService.getObject("listStorage_"+pageName);
        if(listStorage==null){
            listStorage={};            
        }
        if(listStorage[pageName]==null){
            listStorage[pageName]={};
        }
        return listStorage[pageName][listName];
    }

    storeQuickLinksMachineLists(tournaments){
        let tournamentMachines=[];
        tournaments.forEach((tournament)=>{
            tournament.tournament_machines.forEach((machine)=>{                
                machine.tournament_name=tournament.tournament_name;
                tournamentMachines.push(machine);
            })
        })
        tournamentMachines=tournamentMachines.sort((n1,n2)=>{
            if(n1.tournament_machine_name>n2.tournament_machine_name){
                return 1;
            } else {
                return -1;
            }
        })
        let tournamentMachinesListToStore = []
        tournamentMachines.forEach((machine,index)=>{                        
            tournamentMachinesListToStore.push({index:index+1,tournamentMachineId:machine.tournament_machine_id,tournamentMachineName:machine.tournament_machine_name,tournamentId:machine.tournament_id,tournamentName:machine.tournament_name});
            
        })
        this.updateList('QuickLinksPage','tournament_machines',tournamentMachinesListToStore)        
    }
    
    updateList(pageName,listName, list){
        let listStorage = this._cookieService.getObject("listStorage_"+pageName);
        if(listStorage==null){
            listStorage={};            
        }
        if(listStorage[pageName]==null){
            listStorage[pageName]={};
        }
        listStorage[pageName][listName]=list;
        this._cookieService.putObject("listStorage_"+pageName,listStorage);
    }
    //FIXME : this should be in it's own service
    addFavoriteTournamentMachine(eventId,tournamentMachineId,tournamentMachineName,tournamentId,tournamentName,index?){
        console.log('recording new favorite...');
        let favoriteMachines = this._cookieService.getObject("favoriteMachines");
        if(favoriteMachines==null){
            favoriteMachines={};            
        }
        if(favoriteMachines[eventId]==null){
            favoriteMachines[eventId]={};
        }
        if(favoriteMachines[eventId][tournamentMachineId]==null){
            favoriteMachines[eventId][tournamentMachineId]={tournamentMachineId:tournamentMachineId,tournamentMachineName:tournamentMachineName,tournamentId:tournamentId,tournamentName:tournamentName};
            if(index!=null){
                favoriteMachines[eventId][tournamentMachineId].index=index;
            }
            
            // let toast = this.toastCtrl.create({
            //     message: 'Machine added to favorites',
            //     duration: 99000,
            //     position: 'top',
            //     showCloseButton: true,
            //     closeButtonText: " ",
            //     cssClass: "successToast"
            // });
            // toast.present();
        }  
        this._cookieService.putObject("favoriteMachines",favoriteMachines);
        
        
    }
    getFavoriteTournamentMachines(eventId){        
        let favoriteMachines = this._cookieService.getObject("favoriteMachines");
        if(favoriteMachines==null){
            return null;
        }
        return favoriteMachines[eventId];
    }
    
    
}
