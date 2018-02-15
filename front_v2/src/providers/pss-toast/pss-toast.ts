import { Injectable } from '@angular/core';
import { ToastController, Toast } from 'ionic-angular';

/*
  Generated class for the PssToastProvider provider.

  See https://angular.io/guide/dependency-injection for more info on providers
  and Angular DI.
*/
@Injectable()
export class PssToastProvider {
    currentToast:Toast=null;
    constructor(private toastCtrl: ToastController) {
        console.log('Hello PssToastProvider Provider');
    }
    showToast(message,duration, type){
        if(this.currentToast!=null){
            this.currentToast.dismiss();
            // do something
        }
        
        let toastOptions = {
            message:  message,
            duration: duration,
            position: 'top',
            showCloseButton: true,
            closeButtonText: " ",
            cssClass: type,
            dismissOnPageChange: true	
        }
        this.currentToast = this.toastCtrl.create(toastOptions)
        this.currentToast.present()
    }
}
