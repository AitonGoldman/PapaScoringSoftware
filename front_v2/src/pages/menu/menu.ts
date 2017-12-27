import { Component } from '@angular/core';
import { Platform, IonicPage, NavController, NavParams } from 'ionic-angular';
import { TitleServiceProvider } from '../../providers/title-service/title-service';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

/**
 * Generated class for the MenuPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-menu',
  templateUrl: 'menu.html',
})
export class MenuPage extends PssPageComponent {    
    rootPage:string = null;
    
        
  constructor(public navCtrl: NavController,
              public navParams: NavParams,
              public plt: Platform,
              public titleService: TitleServiceProvider,
              public eventAuth: EventAuthProvider) {
      super(eventAuth,navParams);      
      if(this.plt.is('mobile') == true){          
          this.rootPage='TabsPage';    
      } else {          
          this.rootPage='HomePage';         
      }
      
  }    
    ionViewDidLoad() {
        console.log('ionViewDidLoad MenuPage');
    }
    menuNav(targetPage){
        this.navCtrl.getAllChildNavs()[0].push(targetPage,this.buildNavParams({}));
    }
  
}
