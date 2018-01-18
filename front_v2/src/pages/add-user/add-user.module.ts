import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddUserPage } from './add-user';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { SimpleNotificationsModule } from 'angular2-notifications';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    AddUserPage,
  ],
  imports: [
      IonicPageModule.forChild(AddUserPage),
      AutoCompleteModule,
      SimpleNotificationsModule.forRoot(),
      CustomComponentsModule                 
  ],
})
export class AddUserPageModule {}
