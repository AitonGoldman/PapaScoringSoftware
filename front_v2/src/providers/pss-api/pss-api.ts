import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { Observable} from 'rxjs/Observable';
import { Subject} from 'rxjs/Subject';
import { of }         from 'rxjs/observable/of';
import { LoadingController } from 'ionic-angular';
import { PssToastProvider } from '../pss-toast/pss-toast';


/*
  Generated class for the PssApiProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class PssApiProvider {
    timeoutInMs:number=10000;    
    httpPrefix=null;
    pssUrlPort=null;
    pssHost=null;
     // pssHostUrl='http://192.168.1.178:8100';
    //pssHostUrl='https://results.papa.org';
    //basePssUrl='http://192.168.1.178:8000/api';
    //basePssUrl='https://results.papa.org:8000/api';
    basePssUrl='http://0.0.0.0:8000/api';
    pssHostUrl='http://0.0.0.0:8100';    
//   pssHostUrl='http://9.75.197.88:8100';
//   basePssUrl='http://9.75.197.88:8000';
    backendVersion=3;
    
    loading_instance = null;   
    constructor(public http: HttpClient,public loadingCtrl: LoadingController,
                //private toastCtrl: ToastController,
                private pssToast:PssToastProvider
               ){
        console.log('Hello PssApiProvider Provider');
        //this.httpPrefix='https'
        //this.pssUrlPort='8100'
        //this.pssHost='192.168.1.178'
        //pssHostUrl=this.httpPrefix+'://'+this.pssHost+":"+this.pssUrlPort;
        //basePssUrl=this.httpPrefix+'://'+this.pssHost+':8000';
        
    }
    getBackendHost(){
        return this.basePssUrl;
    }
    getBackendHostUrl(){
        return this.pssHostUrl;
    }
    
    makeHot(cold) {
        const subject = new Subject();
        cold.subscribe(subject);
        return new Observable((observer) => subject.subscribe(observer));
    }
    
    generate_api_call(apiName,url,method,hideLoading?){
        return (...restOfArgs: any[]) => {
            
            let localUrl=url;            
            let postObject=null;            
            if(method=="post" || method=="put" || method=="delete") {
                postObject=restOfArgs.shift();
            }
            let localMatches = localUrl.match(/\:arg/g);
            if (restOfArgs!=null && localMatches!=null && localMatches.length!=restOfArgs.length){
                throw new Error("Oops - number of args in url and args given do not match");
            }
            if(hideLoading==null||hideLoading==false){
                this.loading_instance = this.loadingCtrl.create({
                    content: 'Please wait...'                
                });
                this.loading_instance.present();        
            }
            
            while (localUrl.indexOf(':arg')>=0) {
                let newUrl=localUrl.replace(":arg",restOfArgs.shift())
                localUrl = newUrl;
            }
            localUrl=localUrl+'?version='+this.backendVersion;
            let result_observable = this.makeHot(this.http.request(method,localUrl,            
                                                                   {withCredentials:true,                                                                    
                                                                    body:postObject}
                                                                  )['timeout'](this.timeoutInMs))
                .pipe(                
                    catchError(this.handleError(apiName,null))
                );

            result_observable.subscribe(()=>{if(hideLoading==null){this.loading_instance.dismiss()}});
            return result_observable;            
        }
    }    
    adminVoidTicket = this.generate_api_call('adminVoidTicket',this.basePssUrl+"/:arg/admin/token/:arg/:arg/:arg",'delete');
    adminAddScore = this.generate_api_call('adminAddScore',this.basePssUrl+"/:arg/admin/entry/:arg/:arg/:arg",'put');
    adminEditScore = this.generate_api_call('editScore',this.basePssUrl+"/:arg/admin/entry/:arg/:arg",'put');
    
    addTournamentMachine = this.generate_api_call('addTournamentMachine',this.basePssUrl+"/:arg/tournament_machine",'post');
    addEventUsers = this.generate_api_call('addEventUsers',this.basePssUrl+"/:arg/event_user",'post');
    addEventPlayers = this.generate_api_call('addEventPlayers',this.basePssUrl+"/:arg/player",'post');
    addEventPlayerToQueue = this.generate_api_call('addPlayerToQueue',this.basePssUrl+"/:arg/queue",'post');
    kioskAddEventPlayerToQueue = this.generate_api_call('kioskAddPlayerToQueue',this.basePssUrl+"/:arg/queue/authless",'post');

    bumpPlayerDownQueue = this.generate_api_call('bumpPlayerDownQueue',this.basePssUrl+"/:arg/queue",'put')
    completeTicketPurchase = this.generate_api_call('completeTicketPurchase',this.basePssUrl+"/:arg/token/:arg",'put');
    completeRound = this.generate_api_call('completeRound',this.basePssUrl+"/:arg/final/:arg/:arg",'put');

    createEvent = this.generate_api_call('createEvent',this.basePssUrl+"/event",'post');
    createWizardEvent = this.generate_api_call('createWizardEvent',this.basePssUrl+"/wizard/event/tournament/tournament_machines",'post');
    createWizardTournament = this.generate_api_call('createWizardTournament',this.basePssUrl+"/wizard/tournament/tournament_machines",'post');        
    createTournament = this.generate_api_call('createTournament',this.basePssUrl+"/:arg/tournament",'post');

    editTournamentMachine = this.generate_api_call('editTournamentMachine',this.basePssUrl+"/:arg/tournament_machine",'put');
    editTournament = this.generate_api_call('editTournament',this.basePssUrl+"/:arg/tournament",'put');
    editEvent = this.generate_api_call('editEvent',this.basePssUrl+"/event",'put');
    editPlayer = this.generate_api_call('editEvent',this.basePssUrl+"/:arg/player",'put');
    
    editEventUserRole = this.generate_api_call('editEventUser',this.basePssUrl+"/:arg/event_role_mapping",'put');    
    editEventUserPassword = this.generate_api_call('editEventUserPassword',this.basePssUrl+"/:arg/password",'put');    
    editFinalsMatch = this.generate_api_call('editFinalsMatch',this.basePssUrl+"/:arg/finals_match/:arg",'put');    
    
    eventOwnerCreateRequest = this.generate_api_call('eventOwnerCreateRequest',this.basePssUrl+"/pss_user_request",'post');
    eventOwnerCreateConfirm = this.generate_api_call('eventOwnerCreateConfirm',this.basePssUrl+"/pss_user_request_confirm/:arg",'post');
    generateFinalsBracket = this.generate_api_call('generateFinalsBracket',this.basePssUrl+"/:arg/brackets/:arg/:arg",'post');
    
    
    getAllEvents = this.generate_api_call('getAllEvents',this.basePssUrl+"/events",'get');
    getAllPlayers = this.generate_api_call('getAllPlayers',this.basePssUrl+"/players",'get');    
    getEventPlayer = this.generate_api_call('getEventPlayer',this.basePssUrl+"/:arg/event_player/:arg",'get');
    getEventPlayerResultsHidden = this.generate_api_call('getEventPlayerResults',this.basePssUrl+"/:arg/test_player_results/:arg",'get',true);
    getEventPlayerResults = this.generate_api_call('getEventPlayerResults',this.basePssUrl+"/:arg/test_player_results/:arg",'get');
    getEventPlayerResultsByPlayerId = this.generate_api_call('getEventPlayerResults',this.basePssUrl+"/:arg/test_player_results_by_player_id/:arg",'get');
    
    getEventPlayerHidden = this.generate_api_call('getEventPlayer',this.basePssUrl+"/:arg/event_player/:arg",'get',true);

    getEventPlayers = this.generate_api_call('getEventPlayers',this.basePssUrl+"/:arg/event_players/:arg",'get');
    getEvent = this.generate_api_call('getEvent',this.basePssUrl+"/event/:arg",'get');
    getFinal = this.generate_api_call('getFinal',this.basePssUrl+"/:arg/final/:arg",'get')
    getFinalsTiebreakersRollCall = this.generate_api_call('getFinalsTiebreakersRollCall',this.basePssUrl+"/:arg/tiebreakers/:arg/:arg",'get')
    saveFinalsBootstrapTiebreakersScore = this.generate_api_call('saveFinalsBootstrapTiebreakersScore',this.basePssUrl+"/:arg/tiebreaker/:arg",'put')
    saveFinalsMatchTiebreakersScore = this.generate_api_call('saveFinalsMatchTiebreakersScore',this.basePssUrl+"/:arg/tiebreaker/:arg/match/:arg",'put')

    getIfpaRanking = this.generate_api_call('getIfpaRanking',this.basePssUrl+"/ifpa/:arg",'get');
    
    getTournament = this.generate_api_call('getTournament',this.basePssUrl+"/:arg/tournament/:arg",'get');
    
    getAllTournamentMachines = this.generate_api_call('getAllTournamentMachines',this.basePssUrl+"/:arg/:arg/tournament_machines/machines",'get');
    getTournamentMachines = this.generate_api_call('getAllTournamentMachines',this.basePssUrl+"/:arg/:arg/tournament_machines",'get');
    getTournamentMachine = this.generate_api_call('getAllTournamentMachines',this.basePssUrl+"/:arg/:arg/tournament_machine/:arg",'get');
    getTournamentResults = this.generate_api_call('getTournamentResults',this.basePssUrl+"/:arg/test_tournament_results/:arg",'get');
    getTournamentResultsHidden = this.generate_api_call('getTournamentResults',this.basePssUrl+"/:arg/test_tournament_results/:arg",'get',true);

    getTournamentMachineResults = this.generate_api_call('getTournamentMachineResults',this.basePssUrl+"/:arg/test_tournament_machine_results/:arg/:arg",'get');
    getTournamentMachineResultsHidden = this.generate_api_call('getTournamentMachineResults',this.basePssUrl+"/:arg/test_tournament_machine_results/:arg/:arg",'get',true);

    getAllMachines = this.generate_api_call('getAllMachines',this.basePssUrl+"/machines",'get');
    getAuditLogs = this.generate_api_call('getAuditLogs',this.basePssUrl+"/:arg/audit_log/:arg",'get');
    
    getAllUsers = this.generate_api_call('getAllUsers',this.basePssUrl+"/pss_users",'get');
    getScores = this.generate_api_call('getScores',this.basePssUrl+"/:arg/scores/:arg",'get');        
    
    getAllTournaments = this.generate_api_call('getAllTournaments',this.basePssUrl+"/:arg/tournaments",'get');

    //fixme : can probably replace earlier calls with this call
    getAllTournamentsAndMachines = this.generate_api_call('getAllTournamentsAndMachines',this.basePssUrl+"/:arg/tournaments/tournament_machines",'get');
    getAllTournamentsAndMachinesHidden = this.generate_api_call('getAllTournamentsAndMachines',this.basePssUrl+"/:arg/tournaments/tournament_machines",'get',true);
    
    getAllTournamentsAndMachinesAndEventPlayer = this.generate_api_call('getAllTournamentsAndMachines',this.basePssUrl+"/:arg/tournaments/tournament_machines/event_player/:arg",'get');

    getAllEventsAndTournaments = this.generate_api_call('getAllEventsAndTournaments',this.basePssUrl+"/events/tournaments",'get');
    
    loginEventOwner = this.generate_api_call('loginEventOwner',this.basePssUrl+"/auth/pss_user/login",'post');
    loginUser = this.generate_api_call('loginUser',this.basePssUrl+"/auth/pss_event_user/login/:arg",'post');
    loginPlayer = this.generate_api_call('loginPlayer',this.basePssUrl+"/auth/player/login/:arg",'post');
    removePlayerFromQueue = this.generate_api_call('removePlayerFromQueue',this.basePssUrl+"/:arg/queue",'delete');
    recordTokens = this.generate_api_call('recordTokens',this.basePssUrl+"/fcm_tokens/:arg",'get',true);
    searchPlayers = this.generate_api_call('searchPlayers',this.basePssUrl+"/players/:arg",'get');        
    searchPlayersHidden = this.generate_api_call('searchPlayers',this.basePssUrl+"/players/:arg",'get',true);        

    searchEventPlayers = this.generate_api_call('searchPlayers',this.basePssUrl+"/:arg/event_players/:arg",'get');           searchEventPlayersHidden = this.generate_api_call('searchPlayers',this.basePssUrl+"/:arg/event_players/:arg",'get',true);        

    startPlayerOnMachine = this.generate_api_call('startPlayerOnMachine',this.basePssUrl+"/:arg/entry",'post');    

    submitScore = this.generate_api_call('submitScore',this.basePssUrl+"/:arg/entry",'put');

    purchaseTicket = this.generate_api_call('purchaseTicket',this.basePssUrl+"/:arg/token",'post');
    voidTicket = this.generate_api_call('purchaseTicket',this.basePssUrl+"/:arg/entry",'delete');
    voidTicketAndReaddOrQueue = this.generate_api_call('deleteTicketAndReaddOrQueue',this.basePssUrl+"/:arg/entry/player",'delete');

    private handleError<T> (operation = 'operation', result?: T) {
    //private handleError<T> (operation = 'operation') {            
        let debouncer=false;
        
        return (error: any): Observable<T> => {                        
            if (debouncer == false){
                debouncer=true;
                
                if(error.constructor.name=="TimeoutError"){
                    console.log('TIMEOUT IS HAPPENING...');
                    //console.log(error)
                    error.status=-1;
                    error.error={message:"Operation Timed Out.  Please Try Again. "}
                }
                console.error(error); // log to console instead                
                if(error.status!=404){                    
                    let error_message = "";
                    if(error.status==0){
                        error_message="Internal server error.  Please try again."
                    } else {
                        error_message=error.error.message;
                    }
                    this.pssToast.showToast(error_message,7000,"dangerToast");                    
                }
                if (error.status==404){
                    console.log('found 404...')
                    result = {data:null} as any
                }   
            } 
            // Let the app keep running by returning an empty result.
            //return Observable.empty();
            return of(result as T);
        };        
    }    
}
