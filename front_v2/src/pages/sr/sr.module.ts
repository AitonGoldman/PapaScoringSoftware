import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { SrPage } from './sr';

@NgModule({
  declarations: [
    SrPage,
  ],
  imports: [
    IonicPageModule.forChild(SrPage),
  ],
})
export class SrPageModule {}
