/**
 * Generated class for the CustomHeaderComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
import { Component, Input } from '@angular/core';
import { Platform } from 'ionic-angular';

@Component({
  selector: 'custom-headers',
  templateUrl: 'custom-header.html'
})
export class CustomHeaderComponent {
    goGoCustomHeader(){
        
    }
    @Input() homePage;
    @Input() eventId;
        
    // @Input() eventName;

    // @Input() title;
    
    
}
