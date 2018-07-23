import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { reorderArray } from 'ionic-angular';

/**
 * Generated class for the EventOwnerQuickLinksPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-event-owner-quick-links',
  templateUrl: 'event-owner-quick-links.html',
})
export class EventOwnerQuickLinksPage extends PssPageComponent {
    reorderEnabled:boolean = false;
    items=[];

  ionViewDidLoad() {
    console.log('ionViewDidLoad QuickLinksPage');
  }
    reorderItems(indexes) {
        this.items = reorderArray(this.items, indexes);
    }    

}
