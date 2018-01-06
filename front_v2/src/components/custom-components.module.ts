import { NgModule } from '@angular/core';
import { CustomHeaderComponent } from './custom-header/custom-header';
import {IonicModule} from 'ionic-angular';

@NgModule({
    declarations: [CustomHeaderComponent],
    imports: [IonicModule],
    exports: [CustomHeaderComponent]
})
export class CustomComponentsModule {}
