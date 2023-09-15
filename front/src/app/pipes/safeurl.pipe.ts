import { Pipe } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Pipe({name: 'safeurl'})
export class SafeUrl {
  constructor(private sanitizer:DomSanitizer){}

  transform(html) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(html);
  }
}