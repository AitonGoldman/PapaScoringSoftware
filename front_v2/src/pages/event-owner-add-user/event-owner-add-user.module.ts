import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EventOwnerAddUserPage } from './event-owner-add-user';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
    EventOwnerAddUserPage,
  ],
  imports: [
      IonicPageModule.forChild(EventOwnerAddUserPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot()      
  ],
})
export class EventOwnerAddUserPageModule {}
