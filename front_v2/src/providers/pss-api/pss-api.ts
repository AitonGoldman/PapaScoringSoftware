import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { Observable } from 'rxjs/Observable';
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
    basePssUrl='http://localhost:8000'
    loading_instance = null;   
    constructor(public http: HttpClient,public loadingCtrl: LoadingController,
                private toastCtrl: ToastController) {
        console.log('Hello PssApiProvider Provider');
    }
    
    generate_api_call(apiName,url,method){
        return (...restOfArgs: any[]) => {
            let localUrl=url;            
            let postObject=null;
            if(method=="post" || method=="put"){
                postObject=restOfArgs.shift();
            }
            if (localUrl.match(/\:arg/g).length!=restOfArgs.length){
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
            let result_observable = this.http[method](localUrl,            
                                                      postObject)
                .pipe(                
                    catchError(this.handleError(apiName, null))
                );
            result_observable.subscribe(()=>{this.loading_instance.dismiss()});
            return result_observable;            
        }
    }
    loginUser = this.generate_api_call('loginUser',this.basePssUrl+"/auth/pss_event_user/login/:arg",'post');
    // loginUser(eventId, user_info) {
    //     this.loading_instance = this.loadingCtrl.create({
    //         content: 'Please wait...'
    //     });

    //     this.loading_instance.present();        
    //     let result_observable = this.http.post(this.basePssUrl+"/auth/pss_event_user/login/"+eventId,
    //                                        user_info)
    //         .pipe(                
    //             catchError(this.handleError('loginUser', null))
    //         );
    //     result_observable.subscribe(()=>{this.loading_instance.dismiss()});
    //     return result_observable;
    // }
    private handleError<T> (operation = 'operation', result?: T) {
        //this.loading.dismiss();
        let debouncer=false;        
        return (error: any): Observable<T> => {
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
            //throw Observable.throw(result);  
        };        
    }    
}
