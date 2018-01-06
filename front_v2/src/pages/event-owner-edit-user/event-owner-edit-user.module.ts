import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { EventOwnerEditUserPage } from './event-owner-edit-user';

@NgModule({
  declarations: [
    EventOwnerEditUserPage,
  ],
  imports: [
    IonicPageModule.forChild(EventOwnerEditUserPage),
      AutoCompleteModule
  ],
})
export class EventOwnerEditUserPageModule {}
