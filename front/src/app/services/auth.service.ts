import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({ providedIn: 'root' })
export class AuthService {
    
    private token = ''
    private refresh = ''

    constructor(private http: HttpClient) {}
    
    setToken(token) {
        this.token = token
    }

    setRefreshToken(token) {
        this.token = token
    }

    public get auth() {
        return this.token
    }
    
    public get refresh_token() {
        return this.refresh
    }
    
    login(form: FormData) {
        return this.http.post('http://localhost:8000/api/login/', form)
    }

    newUser(form: FormData) {
        return this.http.post('http://localhost:8000/auth/users/', form)
    }
    
    refershToken() {
        return this.http.post('http://localhost:8000/api/login/', {'refresh': this.refresh})
    }

}