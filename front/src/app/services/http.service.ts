import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({ providedIn: 'root' })
export class HttpService {

    url = "http://localhost:8000/api"

    constructor(private http: HttpClient) {}

    train_clustering(form: FormData) {
        return this.http.post(`${this.url}/clustering/`, form)
    }

    train_logostic(form: FormData) {
        return this.http.post(`${this.url}/churn/train`, form)
    }

    test_logositic(form: FormData) {
        return this.http.post(`${this.url}/churn/test`, form)
    }

    predict_logositic(form: FormData) {
        return this.http.post(`${this.url}/churn/`, form)
    }
}