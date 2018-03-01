import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { SrPage } from '../sr/sr'
import { trigger, style, transition, animate  } from '@angular/animations'

/**
 * Generated class for the ArPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage({
    segment: 'ar/:sliceDelta/:pause/:tournamentIndexToDisplay'
})
@Component({
    selector: 'page-ar',
    templateUrl: 'ar.html',
    animations: [
        trigger('scrollOut', [
            transition(':leave', [
                style({transform: 'translateY(0)', opacity: 1}),
                animate('1500ms', style({transform: 'translateY(-100%)', opacity: 0}))
            ])                        
        ])
    ]    
})
export class ArPage extends SrPage {
    sliceDelta:number=20;
    pause:number=8000;
        
}
