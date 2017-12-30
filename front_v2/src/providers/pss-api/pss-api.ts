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
    basePssUrl='http://0.0.0.0:8000'
    //basePssUrl='http://0.0.0.0'
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
            let postObject={};
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
            //let result_observable = this.http[method](localUrl,
            let result_observable = this.makeHot(this.http[method](localUrl,            
                                                                   postObject,{withCredentials:true}))
                 .pipe(                
                     catchError(this.handleError(apiName, null))
                 );
            
            result_observable.subscribe(()=>{this.loading_instance.dismiss()});
            return result_observable;            
        }
    }
    loginUser = this.generate_api_call('loginUser',this.basePssUrl+"/auth/pss_event_user/login/:arg",'post');
    loginEventOwner = this.generate_api_call('loginEventOwner',this.basePssUrl+"/auth/pss_user/login",'post');
    
    createEvent = this.generate_api_call('createEvent',this.basePssUrl+"/event",'post');
    createTournament = this.generate_api_call('createTournament',this.basePssUrl+"/:arg/tournament",'post');
    addTournamentMachine = this.generate_api_call('addTournamentMachine',this.basePssUrl+"/:arg/tournament_machine",'post');
    editTournamentMachine = this.generate_api_call('editTournamentMachine',this.basePssUrl+"/:arg/tournament_machine",'put');
    
    getAllEvents = this.generate_api_call('getAllEvents',this.basePssUrl+"/events",'get');
    getAllMachines = this.generate_api_call('getAllMachines',this.basePssUrl+"/:arg/:arg/tournament_machines/machines",'get');
    getAllTournaments = this.generate_api_call('getAllTournaments',this.basePssUrl+"/:arg/tournaments",'get');
    
    getAllEventsAndTournaments = this.generate_api_call('getAllEventsAndTournaments',this.basePssUrl+"/events/tournaments",'get');
    
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
