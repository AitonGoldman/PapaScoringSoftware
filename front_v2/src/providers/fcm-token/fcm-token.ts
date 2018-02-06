import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

/*
  Generated class for the FcmTokenProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class FcmTokenProvider {
    fcmToken:any=null;
    constructor(public http: HttpClient) {
        console.log('Hello FcmTokenProvider Provider');
    }
    getFcmToken(){
        return this.fcmToken;
    }
    setFcmToken(token){
        this.fcmToken=token;
    }

}
