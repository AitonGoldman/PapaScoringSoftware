export class SuccessButton  {    
    constructor(public title:string,
                public targetPage:string,
                public params) {
    }
    getTitle():string {
        return this.title;
    }
    getTargetPage():string {
        return this.targetPage;
    }
    getParams() {
        return this.params;
    }    
}
