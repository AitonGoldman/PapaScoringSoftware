import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { EditUserPage } from './edit-user';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';

@NgModule({
  declarations: [
    EditUserPage,
  ],
  imports: [
      IonicPageModule.forChild(EditUserPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot()                  
  ],
})
export class EditUserPageModule {}
