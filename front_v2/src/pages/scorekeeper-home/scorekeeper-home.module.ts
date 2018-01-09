import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperHomePage } from './scorekeeper-home';

@NgModule({
  declarations: [
    ScorekeeperHomePage,
  ],
  imports: [
    IonicPageModule.forChild(ScorekeeperHomePage),
  ],
})
export class ScorekeeperHomePageModule {}
