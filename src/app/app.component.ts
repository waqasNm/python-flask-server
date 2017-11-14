import { Component } from '@angular/core';
import { Http } from '@angular/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  todos;
  task;
  edit;
  isTrue = -1;
  constructor(private http: Http){
    this.getTasks()
  }

  getTasks(){
    this.http.get('http://127.0.0.1:5000/todos').subscribe(data => {
      console.log(data.json())
      this.todos = data.json()
    })
  }

  addTask(){
    let task = {task:this.task}
    this.http.post('http://127.0.0.1:5000/add-todo',task).subscribe(data => {
      console.log(data.json())
      this.todos = data.json()
    })
    this.task = "";
  }

  delTask(id){
    console.log(id);
    let data = {_id: id}
    this.http.delete(`http://127.0.0.1:5000/delete-todo/${id}`).subscribe(data => {
      console.log(data.json())
      this.todos = data.json()      
    })
  }
  editTrue = true
  editTask(index){
    this.isTrue = index;
    this.editTrue = false;
  }
  closeTask(){
    this.editTrue = true;
    this.isTrue = -1;
    
  }
  
  saveTask(data){
    data.task = this.edit;
    this.isTrue = -1;
    this.http.put(`http://127.0.0.1:5000/update-todo`,data).subscribe(data => {
      console.log(data.json())
    })
    this.edit = "";
    this.editTrue = true;
    

  }
}
