import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { Observable} from 'rxjs/Observable';
import { Subject} from 'rxjs/Subject';
import { of }         from 'rxjs/observable/of';
import { LoadingController } from 'ionic-angular';
import { ToastController } from 'ionic-angular';


/*
  Generated class for the PssApiProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class PssApiProvider {
    basePssUrl='http://192.168.1.178:8000'
    //basePssUrl='http://0.0.0.0:8000'
    loading_instance = null;   
    constructor(public http: HttpClient,public loadingCtrl: LoadingController,
                private toastCtrl: ToastController) {
        console.log('Hello PssApiProvider Provider');
    }

    makeHot(cold) {
        const subject = new Subject();
        cold.subscribe(subject);
        return new Observable((observer) => subject.subscribe(observer));
    }
    
    generate_api_call(apiName,url,method){
        return (...restOfArgs: any[]) => {
            console.log('trying a network op 1 ...')
            let localUrl=url;            
            let postObject=null;            
            if(method=="post" || method=="put"){
                postObject=restOfArgs.shift();
            }
            let localMatches = localUrl.match(/\:arg/g);
            if (restOfArgs!=null && localMatches!=null && localMatches.length!=restOfArgs.length){
                throw new Error("Oops - number of args in url and args given do not match");
            }            
            this.loading_instance = this.loadingCtrl.create({
                content: 'Please wait...'
            });
            this.loading_instance.present();        
            
            while (localUrl.indexOf(':arg')>=0) {
                let newUrl=localUrl.replace(":arg",restOfArgs.shift())
                localUrl = newUrl;
            }
            console.log('trying a network op 2...')
            
            let result_observable = this.makeHot(this.http.request(method,localUrl,            
                                                                   {withCredentials:true,
                                                                    body:postObject}))
                .pipe(                
                    catchError(this.handleError(apiName, null))
                );

            result_observable.subscribe(()=>{this.loading_instance.dismiss()});
            return result_observable;            
        }
    }    
    addTournamentMachine = this.generate_api_call('addTournamentMachine',this.basePssUrl+"/:arg/tournament_machine",'post');
    addEventUsers = this.generate_api_call('addEventUsers',this.basePssUrl+"/:arg/event_user",'post');
    addEventPlayers = this.generate_api_call('addEventPlayers',this.basePssUrl+"/:arg/player",'post');    
    createEvent = this.generate_api_call('createEvent',this.basePssUrl+"/event",'post');
    createWizardEvent = this.generate_api_call('createWizardEvent',this.basePssUrl+"/wizard/event/tournament/tournament_machines",'post');
    createWizardTournament = this.generate_api_call('createWizardTournament',this.basePssUrl+"/wizard/tournament/tournament_machines",'post');        
    createTournament = this.generate_api_call('createTournament',this.basePssUrl+"/:arg/tournament",'post');

    editTournamentMachine = this.generate_api_call('editTournamentMachine',this.basePssUrl+"/:arg/tournament_machine",'put');
    editTournament = this.generate_api_call('editTournament',this.basePssUrl+"/:arg/tournament",'put');
    editEvent = this.generate_api_call('editEvent',this.basePssUrl+"/event",'put');
    editEventUserRole = this.generate_api_call('editEventUser',this.basePssUrl+"/:arg/event_role_mapping",'put');    
    
    eventOwnerCreateRequest = this.generate_api_call('eventOwnerCreateRequest',this.basePssUrl+"/pss_user_request",'post');
    eventOwnerCreateConfirm = this.generate_api_call('eventOwnerCreateConfirm',this.basePssUrl+"/pss_user_request_confirm/:arg",'post');
    
    getAllEvents = this.generate_api_call('getAllEvents',this.basePssUrl+"/events",'get');
    getAllPlayers = this.generate_api_call('getAllPlayers',this.basePssUrl+"/players",'get');    
    getEvent = this.generate_api_call('getEvent',this.basePssUrl+"/event/:arg",'get');
    getIfpaRanking = this.generate_api_call('getIfpaRanking',this.basePssUrl+"/ifpa/:arg",'get');
    
    getTournament = this.generate_api_call('getTournament',this.basePssUrl+"/:arg/tournament/:arg",'get');
    
    getAllTournamentMachines = this.generate_api_call('getAllTournamentMachines',this.basePssUrl+"/:arg/:arg/tournament_machines/machines",'get');
    getAllMachines = this.generate_api_call('getAllMachines',this.basePssUrl+"/machines",'get');
    getAllUsers = this.generate_api_call('getAllUsers',this.basePssUrl+"/pss_users",'get');        
    getAllTournaments = this.generate_api_call('getAllTournaments',this.basePssUrl+"/:arg/tournaments",'get');
    
    getAllEventsAndTournaments = this.generate_api_call('getAllEventsAndTournaments',this.basePssUrl+"/events/tournaments",'get');
    
    loginEventOwner = this.generate_api_call('loginEventOwner',this.basePssUrl+"/auth/pss_user/login",'post');
    loginUser = this.generate_api_call('loginUser',this.basePssUrl+"/auth/pss_event_user/login/:arg",'post');
    searchPlayers = this.generate_api_call('searchPlayers',this.basePssUrl+"/players/:arg",'get');        
    
    private handleError<T> (operation = 'operation', result?: T) {        
        let debouncer=false;        
        return (error: any): Observable<T> => {
            console.log('trying a network op 3...')
            if (debouncer == false){
                debouncer=true;
                console.log('error handling in progress...');
                console.error(error); // log to console instead
                let toast = this.toastCtrl.create({
                    message: error.error.message,
                    duration: 99000,
                    position: 'top',
                    showCloseButton: true,
                    cssClass: "dangerToast"
                });
                toast.present();                
            } 
            // Let the app keep running by returning an empty result.
            return of(result as T);            
        };        
    }    
}
