/* global moment, alert, fetch, getCookie, showFormErrors, serialize,
   formToJSON, dragula */

/** docs */
class DaySchedule {
  /**
   * Constuctor
   */
  constructor() {
    this.is_today = true;
    this.element = document.querySelector('#today');
    this.date = moment(this.element.querySelector('span.hide.date').innerHTML);

    const x = this;

    this.element.querySelector('.prev').addEventListener('click', (e) => {
      e.preventDefault();
      x.prev();
    });
    this.element.querySelector('.next').addEventListener('click', (e) => {
      e.preventDefault();
      x.next();
    });
  }

  /**
   *
   * @return {string} asd
   */
  apiLink() {
    return `/api/schedule/${this.date.format('YYYY-MM-DD')}`;
  }

  /**
   *
   */
  next() {
    this.date = this.date.add(1, 'days');
    this.checkToday();
    this.update();
    // console.log(this.date);
  }
  /**
   *
   */
  prev() {
    this.date = this.date.subtract(1, 'days');
    this.checkToday();
    this.update();
    // console.log(this.date.format('l'));
  }
  /**
   *
   */
  checkToday() {
    if (this.date.format('l') === moment().format('l')) {
      this.is_today = true;
    } else {
      this.is_today = false;
    }
  }
  /**
   *
   */
  updateTodayString() {
    this.element.querySelector('.current').innerHTML = this.date.format('dddd, Do MMMM');
  }

  /**
   *
   * @param {number} i
   * @param {dict} data
   */
  updateLesson(i, data) {
    // let div = document.createElement('div');
    // div.innerHTML = 'asd';
    // this.element.querySelector('.lessons').appendChild(div);
    // console.log('.lessons > div.lesson:nth-child('+i+')');
    const lessons = this.element.querySelector('div.lessons');
    const lesson = lessons.querySelector(`.lesson${i}`);

    // add
    if (!lesson) {
      alert(`no lesson ${i}`);
    }

    const student = lesson.querySelector('.student');
    const s = moment(data.start); // start
    const e = moment(data.end); // end
    const start = lesson.querySelector('.start');
    const end = lesson.querySelector('.end');
    start.innerHTML = s.format('HH:mm');
    start.setAttribute('title', s);
    end.innerHTML = e.format('HH:mm');
    end.setAttribute('title', e);
    if (data.student) {
      lesson.classList.add('busy');
      student.innerHTML = data.student.first_name;
    }
    // let div = this.element.querySelector('div');
    // console.log(lesson);
    // div.innerHTML = 'asd';
    // this.element.querySelector('.lessons').appendChild(div);
  }

  // Update day schedule (all data inside)
  update() {
    // console.log(this.apiLink());
    this.updateTodayString();
    fetch(this.apiLink(), {
      method: 'GET',
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        Accept: 'application/json',
        'Content-type': 'application/x-www-form-urlencoded',
      },
    })
      .then(r => r.json())
      .then((data) => {
        this.updateSchdeule(data.schedule);
        // this.updateTodayString();
        // this.addStudents(data);
      })
      .catch((reason) => {
        alert(`failed api schedule: ${reason}`);
      });
  }

  clear() {
    this.element.querySelector('.lessons').innerHTML = '';
  }

  updateSchdeule(lessons) {
    this.clear();
    let i = 1;
    Array.from(lessons).forEach((lesson) => {
      this.updateLesson(i, lesson);
      i += 1;
    });
    // for (const lesson of lessons) {
    //   this.updateLesson(i, lesson);
    //   i += 1;
    // }
  }
}

class Student {
  constructor(data) {
    // console.log(data);
    this.in_db = false;
    this.name = 'Новый ученик';
    // console.log(typeof data);
    if (typeof data === 'number') {
      // alert('a');
    } else {
      this.first_name = data.first_name;
      this.schedule = data.schedule;
    }
    this.days = [];
  }

  edit() {
    const editbox = document.getElementById('edit_student');
    // editbox.getElementsByTagName('h1')[0].innerHTML = this.first_name;
    editbox.querySelector('input[name=first_name]').value = this.first_name;
    // console.log('schedule:', this.schedule);
    editbox.classList.remove('hide');
    // editbox.classList.remove("hide");
    // this.selectSchedule();
    Array.from(document.querySelectorAll('.lesson')).forEach((lesson) => {
      lesson.classList.add('selected');
    });
  }

  // htmlElement() {
  // }
}

class Students {
  constructor() {
    this.students = { a: 'b' };

    fetch('/api/students', {
      method: 'GET',
      credentials: 'include',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        Accept: 'application/json',
        'Content-type': 'application/x-www-form-urlencoded',
      },
    })
      .then(r => r.json())
      .then((data) => {
        // console.log(data);
        this.addStudents(data);
      })
      .catch((reason) => {
        alert(`failed api students ${reason}`);
      });

    // fetch('/students', {
    // method: 'POST',
    // credentials: 'include',
    // headers: {
    // "X-CSRFToken": getCookie('csrftoken'),
    // "Accept": "application/json",
    // "Content-type": "application/x-www-form-urlencoded"
    // },
    // body: serialize({})
    // })
    // .then(r => r.json())
    // .then(data => {
    // console.log(data);
    // // this.addStudents(data);
    // if ("errors" in data){
    // // showFormErrors(data["errors"], document.getElementById("login"));
    // }else{
    // // window.location.href = getURLParameter('next');
    // }
    // })
    // .catch(function(reason) {
    // alert('failed students creation');
    // });

    // for (let element of document.getElementsByClassName('student')) {
    Array.from(document.getElementsByClassName('student')).forEach((element) => {
      // let id = parseInt(element.getAttribute("data-id"));
      // // console.log(id);
      // this.addStudents(id);

      element.addEventListener('click', (e) => {
        e.preventDefault();
        const id = parseInt(this.getAttribute('data-id'), 10);
        // console.log('get: ', id);
        // console.log(students);
        // students.get(id).edit();
        this.get(id).edit();
        // alert('a');
      });
      // // element.addEventListener("click", function(e) {
      // // // e.preventDefault();
      // // let L = new Lesson(this);
      // // L.edit();
      // // L.mark();
      // // // document.getElementById("week").classList.toggle("hide");
      // // // document.getElementById("new_student").classList.toggle("hide");
      // // });
    });
  }

  get(id) {
    // console.log(id);
    // console.log(this.students);
    return this.students[id];
  }

  addStudents(data) {
    // console.log('Students from: ', typeof data);
    if (Array.isArray(data)) {
      // console.log('Students from array');
      const first = data[0];
      if (typeof first === 'number') {
        alert('students from array of numbers');
      } else {
        // alert('students from array of data');
        // for (let student of data) {
        data.forEach((student) => {
          // console.log(student);
          // console.log('set', id);
          this.students[student.id] = new Student(student);
        });
      }
    } else {
      this.students[data] = new Student(data);
    }
    // console.log(this.students);
  }
}

window.students = new Students();
window.sch = new DaySchedule();

class Lesson {
  // constructor(height, width) {
  constructor(element, d = {}) {
    this.element = element;
    this.student = 1;
    this.data = d;

    this.start_hour = element.querySelector('.start.hour');

    // student_id input
    this.busy = element.querySelector('form input[name="student_id"]') !== null;
    this.empty = !this.busy;
    if (this.busy) {
      // get lesson data
      // let form = e.target;
      // fetch(e.target.getAttribute('action'), {
      //   method: 'POST',
      //   credentials: 'include',
      //   headers: {
      //     'X-CSRFToken': getCookie('csrftoken'),
      //     Accept: 'application/json',
      //     'Content-type': 'application/x-www-form-urlencoded',
      //   },
      //   body: serialize(formToJSON(form.elements)),
      // })
      //   .then(r => r.json())
      //   .then((data) => {
      //     if ('errors' in data) {
      //       showFormErrors(data.errors, document.getElementById('login'));
      //     } else {
      //       window.location.href = getURLParameter('next');
      //     }
      //   });
    }
    // this.student = ;
    // console.log(this.student);
  }

  edit() {
    if (this.empty) {
      document.getElementById('edit_lesson').classList.remove('hide');
    }
  }

  mark() {
    this.element.classList.toggle('selected');
    // console.log(document.getElementsByClassName('selected'));
  }

  timeStart() {
    // return this.start_hour + ':' + this.start_hour;
    return `${this.start_hour}:${this.start_hour}`;
  }

  getData() {
    if (this.data !== {}) ;
  }
}

class Week {
  constructor() {
    // for (let lesson of document.getElementsByClassName('lesson')) {
    Array.from(document.getElementsByClassName('lesson')).forEach((lesson) => {
      lesson.addEventListener('click', () => {
        // e.preventDefault();
        const L = new Lesson(this);
        L.edit();
        L.mark();
        // document.getElementById("week").classList.toggle("hide");
        // document.getElementById("new_student").classList.toggle("hide");
      });
    });
  }
}

{
  const ready = () => {
    document.week = new Week();
    // console.log(document.querySelector('#today span.hide.date'));
    // console.log('creating mystudents');
    // console.log(document.mystudents);
    // calendar drag - drop
    dragula({
      revertOnSpill: true,
      isContainer: el => el.classList.contains('day'),
      drop: () => {},
      // drop: (el, target, source, sibling) => {
      //   // return el.classList.contains('day');
      // },
    });

    // for (let time of document.getElementsByClassName('day-time')) {
    Array.from(document.getElementsByClassName('day-time')).forEach((time) => {
      time.addEventListener('click', (e) => {
        e.preventDefault();
        // console.log(e.target);
        // document.getElementById("week").classList.toggle("hide");
        // document.getElementById("new_student").classList.toggle("hide");
      });
    });

    // document.getElementById("new_student_btn").addEventListener("click", function(e) {
    // e.preventDefault();
    // document.getElementById("week").classList.toggle("hide");
    // document.getElementById("new_student").classList.toggle("hide");
    // });

    // "add student" form submit
    document.getElementById('new_student_form').addEventListener('submit', (e) => {
      e.preventDefault();
      const form = e.target;
      // console.log(form.elements);
      // console.log('a');
      // console.log(serialize(formToJSON(form.elements)));
      // console.log('b');
      fetch(e.target.getAttribute('action'), {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          Accept: 'application/json',
          'Content-type': 'application/x-www-form-urlencoded',
        },
        body: serialize(formToJSON(form.elements)),
      })
        .then(r => r.json())
        .then((data) => {
          if ('errors' in data) {
            showFormErrors(data.errors, document.getElementById('new_student_form'));
          } else {
            alert('Added!');
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
