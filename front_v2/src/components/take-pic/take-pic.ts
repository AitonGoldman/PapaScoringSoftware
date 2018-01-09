import { NavParams, ViewController } from 'ionic-angular';
import { Component } from '@angular/core';

/**
 * Generated class for the TakePicComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
@Component({
  selector: 'take-pic',
  templateUrl: 'take-pic.html'
})
export class TakePicComponent {
    img_file:string=null;
    text: string;
    customStyle:any=null;
    constructor(public navParam: NavParams, public viewCtrl: ViewController) {
        console.log('Hello TakePicComponent Component');
        this.text = 'Hello World';
    }
    onUploadFinished(event){
        //this.selectedPlayer.has_pic=true;        
        //console.log(event.serverResponse._body);
        this.img_file=JSON.parse(event.serverResponse._body).data;        
        
    }
    onClose(){
        this.viewCtrl.dismiss(this.img_file);
    }
    onRemoved(file) {
        this.img_file=null;
    }    
}
