import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AdminEditScoresPage } from './admin-edit-scores';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    AdminEditScoresPage,
  ],
  imports: [
    IonicPageModule.forChild(AdminEditScoresPage),
      AutoCompleteModule,      
      CustomComponentsModule                   
  ],
})
export class AdminEditScoresPageModule {}
