import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ScorekeeperStartPlayerPage } from './scorekeeper-start-player';
import { AutoCompleteModule } from 'ionic2-auto-complete';

@NgModule({
  declarations: [
    ScorekeeperStartPlayerPage,
  ],
  imports: [
      IonicPageModule.forChild(ScorekeeperStartPlayerPage),
      AutoCompleteModule      
  ],
})
export class ScorekeeperStartPlayerPageModule {}
