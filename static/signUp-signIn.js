const signUp_btn = document.querySelector('.sign-up.btn');
const signIn_btn = document.querySelector('.sign-in.btn');
const main_container = document.querySelector('.main-container');
const forms = document.querySelectorAll('.form');
const forms_container = document.querySelector('.forms-container');
const form_signUp = document.querySelector('.sign-Up-form')


signUp_btn.addEventListener('click', show_signUp_form);
signIn_btn.addEventListener('click', show_signIn_form);
// save nakarde bodi brat save kardam ...
function show_signUp_form() {
    signUp_btn.classList.add('active');
    signIn_btn.classList.remove('active');
    main_container.style.height = "auto";
    form_signUp.style.display = 'flex';
    for (const form of forms) {
        form.classList.add('active'); // show signUp form
    }
}

function show_signIn_form() {
    signIn_btn.classList.add('active')
    signUp_btn.classList.remove('active')
    form_signUp.style.display = 'none';
    main_container.style.height = "420px";
    for (const form of forms) {
        form.classList.remove('active'); // show signIn form
    }
}