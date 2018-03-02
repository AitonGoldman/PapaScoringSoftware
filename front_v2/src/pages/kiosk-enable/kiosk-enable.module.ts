import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { KioskEnablePage } from './kiosk-enable';

@NgModule({
  declarations: [
    KioskEnablePage,
  ],
  imports: [
    IonicPageModule.forChild(KioskEnablePage),
  ],
})
export class KioskEnablePageModule {}
