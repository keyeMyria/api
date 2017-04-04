student_click = function(e){
	e.preventDefault();
	let id = parseInt(this.getAttribute("data-id"));
	// console.log('get: ', id);
	console.log(students);
	students.get(id).edit();
	// alert('a');
};

class DaySchedule{
	constructor(lessons=[]) {
		this.is_today = true;
		this.element = document.querySelector('#today');
		this.date = moment(this.element.querySelector('span.hide.date').innerHTML);

		let x = this;

		this.element.querySelector('.prev').addEventListener("click", function(e) {
			e.preventDefault();
			x.prev();
		});
		this.element.querySelector('.next').addEventListener("click", function(e) {
			e.preventDefault();
			x.next();
		});
	}

	api_link(){return '/api/schedule/' + this.date.format('YYYY-MM-DD');}

	next(){
		this.date = this.date.add(1, 'days');
		this.check_today();
		this.update();
		console.log(this.date);
	}
	prev(){
		this.date = this.date.subtract(1, 'days');
		this.check_today();
		this.update();
		console.log(this.date.format('l'));
	}
	check_today(){
		if (this.date.format('l')==moment().format('l'))
			this.is_today=true;
		else
			this.is_today=false;
	}
	update_today_string(){
		this.element.querySelector('.current').innerHTML = this.date.format('dddd, Do MMMM');
	}

	update_lesson(i, data){
		// let div = document.createElement('div');
		// div.innerHTML = 'asd';
		// this.element.querySelector('.lessons').appendChild(div);
		// console.log('.lessons > div.lesson:nth-child('+i+')');
		let lessons = this.element.querySelector('div.lessons');
		let lesson = lessons.querySelector('.lesson'+i);

		// add
		if (!lesson){
			alert('no lesson '+i);
		}

		let student = lesson.querySelector('.student');
		let s = moment(data['start']); // start
		let e = moment(data['end']);  // end
		let start = lesson.querySelector('.start');
		let end = lesson.querySelector('.end');
		start.innerHTML = s.format('HH:mm');
		start.setAttribute('title', s);
		end.innerHTML = e.format('HH:mm');
		end.setAttribute('title', e);
		if (data['student']) {
			lesson.classList.add('busy');
			student.innerHTML = data['student']['first_name'];
		}
		// let div = this.element.querySelector('div');
		// console.log(lesson);
		// div.innerHTML = 'asd';
		// this.element.querySelector('.lessons').appendChild(div);
	}

	// Update day schedule (all data inside)
	update(){
		console.log(this.api_link());
		this.update_today_string();
		fetch(this.api_link(), {
			method: 'GET',
			credentials: 'include',
			headers: {
				"X-CSRFToken": getCookie('csrftoken'),
				"Accept": "application/json",
				"Content-type": "application/x-www-form-urlencoded"
			}
		})
			.then(r => r.json())
			.then(data => {
				this.update_schdeule(data['schedule']);
				// this.update_today_string();
				// this.add_students(data);
			})
			.catch(function(reason) {
				alert('failed api schedule: '+reason);
			});
	}

	clear(){
		// this.element.querySelector('.lessons').innerHTML='';
	}

	update_schdeule(lessons){
		this.clear();
		let i=1;
		for (let lesson of lessons) {
			this.update_lesson(i, lesson);
			i+=1;
		}
	}
}

class Students{
	constructor() {
		this.students = {'a':'b'};


		fetch('/api/students', {
			method: 'GET',
			credentials: 'include',
			headers: {
				"X-CSRFToken": getCookie('csrftoken'),
				"Accept": "application/json",
				"Content-type": "application/x-www-form-urlencoded"
			}
		})
			.then(r => r.json())
			.then(data => {
				console.log(data);
				this.add_students(data);
			})
			.catch(function(reason) {
				alert('failed api students'+reason);
			});


		// fetch('/students', {
		// 	method: 'POST',
		// 	credentials: 'include',
		// 	headers: {
		// 		"X-CSRFToken": getCookie('csrftoken'),
		// 		"Accept": "application/json",
		// 		"Content-type": "application/x-www-form-urlencoded"
		// 	},
		// 	body: serialize({})
		// })
		// 	.then(r => r.json())
		// 	.then(data => {
		// 		console.log(data);
		// 		// this.add_students(data);
		// 		if ("errors" in data){
		// 			// showFormErrors(data["errors"], document.getElementById("login"));
		// 		}else{
		// 			// window.location.href = getURLParameter('next');
		// 		}
		// 	})
		// 	.catch(function(reason) {
		// 		alert('failed students creation');
		// 	});

		for (let element of document.getElementsByClassName("student")) {
		// 	let id = parseInt(element.getAttribute("data-id"));
		// 	// console.log(id);
		// 	this.add_students(id);

			element.addEventListener("click", student_click);
		// 	// element.addEventListener("click", function(e) {
		// 	// 	// e.preventDefault();
		// 	// 	let L = new Lesson(this);
		// 	// 	L.edit();
		// 	// 	L.mark();
		// 	// 	// document.getElementById("week").classList.toggle("hide");
		// 	// 	// document.getElementById("new_student").classList.toggle("hide");
		// 	// });
		};
	}

	get(id){
		console.log(id);
		console.log(this.students);
		return this.students[id];
	}

	add_students(data){
		// console.log('Students from: ', typeof data);
		if (Array.isArray(data)) {
			// console.log('Students from array');
			let first = data[0];
			if (typeof first == "number") {
				alert('students from array of numbers');
			}else{
				// alert('students from array of data');
				for (let student of data) {
					let id = student['id'];
					console.log(student);
					// console.log('set', id);
					this.students[id] = new Student(student);
				}
			}
		}else{
			this.students[data] = new Student(data);
		}
		// console.log(this.students);
	}
}

var students = new Students();
var myday = new DaySchedule();


class Student{
	constructor(data) {
		// console.log(data);
		this.in_db = false;
		this.name = 'Новый ученик';
		// console.log(typeof data);
		if (typeof data == "number") {
			// alert('a');
		}else{
			this.first_name = data['first_name'];
			this.schedule = data['schedule'];
		}
		this.days = [];
	}

	edit(){
		let editbox = document.getElementById("edit_student");
		// editbox.getElementsByTagName('h1')[0].innerHTML = this.first_name;
		editbox.querySelector('input[name=first_name]').value = this.first_name;
		console.log('schedule:', this.schedule);
		editbox.classList.remove("hide");
		// editbox.classList.remove("hide");
		this.select_schedule();
	}

	select_schedule(){
		let lessons = document.querySelectorAll('.lesson');
		for (let lesson of lessons) {
			lesson.classList.add("selected");
		}
	}

	html_element(){

	}
}

class Lesson {
	// constructor(height, width) {
	constructor(element, data={}) {
		this.element = element;
		this.student = 1;
		this.data = data;


		this.start_hour = element.querySelector('.start.hour');

		// student_id input
		this.busy = element.querySelector('form input[name="student_id"]') !== null;
		this.empty = !this.busy;
		if (this.busy) {
			// get lesson data
			let form = e.target;
			fetch(e.target.getAttribute("action"), {
				method: 'POST',
				credentials: 'include',
				headers: {
					"X-CSRFToken": getCookie('csrftoken'),
					"Accept": "application/json",
					"Content-type": "application/x-www-form-urlencoded"
				},
				body: serialize(formToJSON(form.elements))
			})
				.then(r => r.json())
				.then(data => {
					if ("errors" in data){
						showFormErrors(data["errors"], document.getElementById("login"));
					}else{
						window.location.href = getURLParameter('next');
					}
				});
		}


		// this.student = ;
		// console.log(this.student);
	}

	edit(){
		if (this.empty){
			document.getElementById("edit_lesson").classList.remove("hide");
		}else{

		}
	}

	mark(){
		this.element.classList.toggle("selected");
		console.log(document.getElementsByClassName("selected"));
	}

	time_start(){
		return this.start_hour+":"+this.start_hour;
	}

	get_data(){
		if (this.data!={}) ;
	}

}

class Week{
	constructor(){
		for (let lesson of document.getElementsByClassName("lesson")) {
			lesson.addEventListener("click", function(e) {
				// e.preventDefault();
				let L = new Lesson(this);
				L.edit();
				L.mark();
				// document.getElementById("week").classList.toggle("hide");
				// document.getElementById("new_student").classList.toggle("hide");
			});
		};
	}
}



{let ready=function(e){
	let week = new Week();
	// console.log(document.querySelector('#today span.hide.date'));
	// console.log('creating mystudents');
	// console.log(document.mystudents);
	// calendar drag - drop
	var drake = dragula({
		revertOnSpill: true,
		isContainer: function (el) {
			return el.classList.contains('day');
		},
		drop: function (el, target, source, sibling) {
			// return el.classList.contains('day');
		}
	});


	for (let time of document.getElementsByClassName("day-time")) {
		time.addEventListener("click", function(e) {
			e.preventDefault();
			console.log(e.target);
			// document.getElementById("week").classList.toggle("hide");
			// document.getElementById("new_student").classList.toggle("hide");
		});
	};


	// document.getElementById("new_student_btn").addEventListener("click", function(e) {
	// 	e.preventDefault();
	// 	document.getElementById("week").classList.toggle("hide");
	// 	document.getElementById("new_student").classList.toggle("hide");
	// });

	// "add student" form submit
	document.getElementById("new_student_form").addEventListener("submit", function(e) {
		e.preventDefault();
		let form = e.target;
		console.log(form.elements);
		console.log("a");
		console.log(serialize(formToJSON(form.elements)));
		console.log("b");
		fetch(e.target.getAttribute("action"), {
			method: 'POST',
			credentials: 'include',
			headers: {
				"X-CSRFToken": getCookie('csrftoken'),
				"Accept": "application/json",
				"Content-type": "application/x-www-form-urlencoded"
			},
			body: serialize(formToJSON(form.elements))
		})
			.then(r => r.json())
			.then(data => {
				if ("errors" in data){
					showFormErrors(data["errors"], document.getElementById("new_student_form"));
				}else{
					alert("Added!");
				}
			});
	});

};
 if (document.readyState === 'complete' || document.readyState !== 'loading') {
	 ready();
 } else {
	 document.addEventListener('DOMContentLoaded', ready);
 }
}
