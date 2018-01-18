/**
 * Generated class for the CustomHeaderComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
import { Component, Input } from '@angular/core';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';

@Component({
  selector: 'custom-headers',
  templateUrl: 'custom-header.html'
})
export class CustomHeaderComponent {    
    constructor(public eventAuth: EventAuthProvider){        

    }
    goGoCustomHeader(){
        
    }
    
    @Input() homePage;
    @Input() homePageDisplayName;    
    @Input() eventId;
    @Input() eventName;
    @Input() title;
        
    // @Input() eventName;

    // @Input() title;
    
}
