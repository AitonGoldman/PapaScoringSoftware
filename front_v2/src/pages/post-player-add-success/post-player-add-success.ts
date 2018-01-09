import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { SuccessPage } from '../success/success'
/**
 * Generated class for the PostPlayerAddSuccessPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-post-player-add-success',
  templateUrl: '../success/success.html',
})
export class PostPlayerAddSuccessPage extends SuccessPage {
    postAddPlayerSuccess:boolean=true;
    ionViewWillLoad() {
        super.ionViewWillLoad();
        console.log('ionViewDidLoad PostPlayerAddSuccessPage');
    }    
}
