import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AdminVoidTokensPage } from './admin-void-tokens';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    AdminVoidTokensPage,
  ],
  imports: [
      IonicPageModule.forChild(AdminVoidTokensPage),
      AutoCompleteModule,      
      CustomComponentsModule                   
  ],
})
export class AdminVoidTokensPageModule {}
