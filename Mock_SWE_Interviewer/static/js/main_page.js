const login = document.getElementById('login');
const user_login = document.getElementById('user');
const user_pass = document.getElementById('password');
const login_info = document.getElementById('login_info')

const r_info = document.getElementById('register_info');
const r_login = document.getElementById('r_user');
const r_password = document.getElementById('r_password');
const r_conf_password = document.getElementById('r_conf_password');
const register = document.getElementById('register');

// Setting play state for login pressing
let login_left = false
login.addEventListener('click', function(){
    login.classList.remove('slid_right');
    login.classList.add('slid_left');
    login_left = true;

    register.classList.add('faded');
    register.style.pointerEvents = 'none';

    login_info.classList.add('fade_in');
    login_info.style.pointerEvents = 'auto';
});

// Setting play state for register pressing
let register_left = false
register.addEventListener('click', function(){
    register.classList.remove('slid_right');
    register.classList.add('slid_left');
    register_left = true;

    login.classList.add('faded');
    login.style.pointerEvents = 'none';

    r_info.classList.add('fade_in');
    r_info.style.pointerEvents = 'auto';

});



document.addEventListener('click', (event) => {
    const isClickInsideLogin = login.contains(event.target);
    const isClickInsideRegister = register.contains(event.target);
    const isClickInsideUserLogin = user_login.contains(event.target);
    const isClickInsidePassLogin = user_pass.contains(event.target);
    const isClickInsideUserRegister = r_login.contains(event.target);
    const isClickInsidePassRegister = r_password.contains(event.target);
    const isClickInsidePassConfRegister = r_conf_password.contains(event.target);

    // if login info is no longer clicked, retracts and restarts 
    if (login_left && !isClickInsideLogin && !isClickInsideUserLogin && !isClickInsidePassLogin) {
        login.classList.remove('slid_left');
        login.classList.add('slid_right');
        login_left = false;
        
        register.classList.remove('faded');
        register.style.pointerEvents = 'auto';

        login_info.classList.remove('fade_in');
        login_info.style.pointerEvents='none';
    }
    // if register info is no longer clicked, retracts and restarts
    if (!isClickInsideRegister && register_left && !isClickInsideUserRegister && !isClickInsidePassRegister && !isClickInsidePassConfRegister) {
        register.classList.remove('slid_left');
        register.classList.add('slid_right');
        register_left = false;
        
        login.classList.remove('faded');
        login.style.pointerEvents = 'auto';

        r_info.classList.remove('fade_in');
        r_info.style.pointerEvents = 'none';
    }
});


document.getElementById('login_info').addEventListener('keypress', function(event) {
    // Check if the key pressed is Enter (key code 13)
    if (event.key === 'Enter') {
        if (user_login.value != '' && user_pass.value != ''){
            data = {username: user_login.value, password: user_pass.value};


            fetch('/get_login_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status == 'Credentials Wrong'){
                        // Makes the outline red to let user know its wrong
                        console.log('credential is wrong');
                        user_login.classList.add('error');
                        user_pass.classList.add('error');

                    } else {
                        window.location.href = '/dashboard_page';
                    }
                })
        }
    }
});

// Remove the red outline if there is when focused again
document.getElementById('login_info').addEventListener('focus', function(){
    user_login.classList.remove('error');
    user_pass.classList.remove('error');
});

document.getElementById('register_info').addEventListener('keydown', function(event){
    if (event.key == 'Enter'){
        if (r_login.value != '' && r_password.value != '' && r_conf_password.value != '' && r_conf_password.value == r_password.value){
            data = {username: r_login.value, password: r_password.value};

            fetch('/get_register_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status == 'User already exists'){
                        r_login.classList.add('error');
                        r_password.classList.add('error');
                        r_conf_password.classList.add('error');
                    }
                    else {
                        window.location.href = '/dashboard_page';
                    }
                })
        } else if (r_conf_password.value != r_password.value) {
            r_password.classList.add('error');
            r_conf_password.classList.add('error');
        } else {
            r_login.classList.add('error');
            r_password.classList.add('error');
            r_conf_password.classList.add('error');
        }
    }
});
