import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { Observable } from 'rxjs/Observable';
import { of }         from 'rxjs/observable/of';
import { LoadingController } from 'ionic-angular';

/*
  Generated class for the PssApiProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class PssApiProvider {
    basePssUrl='http://localhost:8000'
    loading_instance = null;
    constructor(public http: HttpClient,public loadingCtrl: LoadingController) {
        console.log('Hello PssApiProvider Provider');
    }
    loginUser(eventId, user_info):Observable {
        this.loading = this.loadingCtrl.create({
            content: 'Please wait...'
        });

        this.loading.present();        
        let result_observable = this.http.post(this.basePssUrl+"/auth/pss_event_user/login/"+eventId,
                                           user_info)
            .pipe(                
                catchError(this.handleError('loginUser', null))
            );
        result_observable.subscribe(()=>{this.loading.dismiss()});
        return result_observable;
    }
    private handleError<T> (operation = 'operation', result?: T) {
        //this.loading.dismiss();
        return (error: any): Observable<T> => {
 
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead
  
            // Let the app keep running by returning an empty result.
            return of(result as T);
            //throw Observable.throw(result);  
        };        
    }    
}
