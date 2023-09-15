import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({ providedIn: 'root'})
export class HistoryService {

    url = 'http://localhost:8000/'
    constructor(private http: HttpClient) {}

    get_clustering_history() {
        return this.http.get(`${this.url}cluster-images`)
    }

    get_logistic_history() {
        return this.http.get(`${this.url}logistic-images`)
    }

    get_one_clustering(id) {
        return this.http.get(`${this.url}cluster-images/${id}`)
    }    
    get_one_lositic(id) {
        return this.http.get(`${this.url}logistic-images/${id}`)
    }
}