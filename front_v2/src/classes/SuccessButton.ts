export class SuccessButton  {    
    constructor(public title:string,
                public targetPage:string,
                public params,
                public targetTabIndex?:number) {
    }
    getTitle():string {
        return this.title;
    }
    getTargetPage():string {
        return this.targetPage;
    }
    getTargetTabIndex():number {
        return this.targetTabIndex;
    }    
    getParams() {
        return this.params;
    }    
}
