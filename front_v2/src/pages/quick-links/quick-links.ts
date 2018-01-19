import { Component } from '@angular/core';
import { IonicPage } from 'ionic-angular';
import { PssPageComponent } from '../../components/pss-page/pss-page'
import { reorderArray } from 'ionic-angular';

/**
 * Generated class for the QuickLinksPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-quick-links',
  templateUrl: 'quick-links.html',
})
export class QuickLinksPage extends PssPageComponent {  
    reorderEnabled:boolean = false;
    items=[{'title':'Results - Classics I',
            'icon':'md-clipboard'},
           {'title':'Results - Main A',
            'icon':'md-clipboard'},
           {'title':'Queues - Classics I',
            'icon':'git-branch'},
           {'title':'Queues - Classics I',
            'icon':'git-branch'},           
          ];

  ionViewWillLoad() {
    console.log('ionViewDidLoad QuickLinksPage');
  }
    reorderItems(indexes) {
        this.items = reorderArray(this.items, indexes);
    }    
}
