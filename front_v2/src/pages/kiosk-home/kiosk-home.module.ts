import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { KioskHomePage } from './kiosk-home';
import { CustomComponentsModule } from '../../components/custom-components.module';

@NgModule({
  declarations: [
    KioskHomePage,
  ],
  imports: [
      IonicPageModule.forChild(KioskHomePage),
      CustomComponentsModule,
      
  ],
})
export class KioskHomePageModule {}
