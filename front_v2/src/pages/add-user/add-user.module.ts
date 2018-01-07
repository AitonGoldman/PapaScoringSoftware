import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddUserPage } from './add-user';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
    AddUserPage,
  ],
  imports: [
      IonicPageModule.forChild(AddUserPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot()            
  ],
})
export class AddUserPageModule {}
