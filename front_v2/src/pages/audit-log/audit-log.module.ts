import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AuditLogPage } from './audit-log';
import { AutoCompleteModule } from 'ionic2-auto-complete';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    AuditLogPage,
  ],
  imports: [
    IonicPageModule.forChild(AuditLogPage),
      AutoCompleteModule,      
      CustomComponentsModule                   
  ],
})
export class AuditLogPageModule {}
