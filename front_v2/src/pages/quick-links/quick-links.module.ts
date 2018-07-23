import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { QuickLinksPage } from './quick-links';

@NgModule({
  declarations: [
    QuickLinksPage,
  ],
  imports: [
    IonicPageModule.forChild(QuickLinksPage),
  ],
})
export class QuickLinksPageModule {}
