/**
 * Generated class for the CustomHeaderComponent component.
 *
 * See https://angular.io/api/core/Component for more info on Angular
 * Components.
 */
import { Component, Input } from '@angular/core';
import { EventAuthProvider } from '../../providers/event-auth/event-auth';
import { Platform } from 'ionic-angular';

@Component({
  selector: 'custom-headers',
  templateUrl: 'custom-header.html'
})
export class CustomHeaderComponent {
    text: string;  

    constructor(public eventAuth: EventAuthProvider,public platform: Platform) {
        console.log('Hello CustomHeaderComponent Component');
        this.text = 'Hello World';
    }
    
    @Input() eventId;
        
    @Input() eventName;

    @Input() title;
    
    
}
