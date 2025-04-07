const firstName = document.getElementById('firstName')
if (firstName) {
    firstName.addEventListener('keypress', function(event) {
        if (event.key >= '0' && event.key <= '9') {
            event.preventDefault();  
        }
    });
}

const lastName = document.getElementById('lastName')
if (lastName) {
    lastName.addEventListener('keypress', function (event) {
        if (event.key >= '0' && event.key <= '9') {
            event.preventDefault();
        }
    });
}

const email = document.getElementById('email');
if (email) {
    email.addEventListener('input', function(event) {
        this.value = this.value.toLowerCase();
    });
}

function popAlert(data) {
    const alertContainer = document.getElementById('alertContainer')
    alertContainer.innerHTML = ''

    const status = (data.status === 'error') ? 'danger' : 'success'
    let alert = document.createElement('div')
    alert.id = 'alert'
    alert.className = `alert alert-${status}`
    alert.role = 'alert'
    alert.innerHTML = `${data.message}`

    alertContainer.appendChild(alert)
    setTimeout(() => {
        alert.remove();
    },3000)
}

alertBox = document.getElementById('alert')
if (alertBox) {
    setTimeout(function() {
        alertBox.remove();
    }, 3000)
}

const registerForm = document.getElementById('registerForm')
if (registerForm) {
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();

        fetch('/register/', {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(registerForm)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.success_url
            }
            else {
                popAlert(data);
            }
        })
        .catch(error => {
            popAlert({'status':'error', 'message':error})
        })
    })
}

const resendButton = document.getElementById('resendBtn');
if (resendButton){
    resendButton.addEventListener('click', function(event) {
        event.preventDefault();
        if (!resendButton.disabled) {
            login();
        }
    });
}

function startTimer() {
    let countdown;
    let countdownTime = 30;
    let timerElement = document.getElementById('resendTimer');

    timerElement.textContent = countdownTime;
    resendButton.disabled = true;

    countdown = setInterval(() => {
        countdownTime--;
        timerElement.textContent = countdownTime;
        if (countdownTime <= 0) {
            clearInterval(countdown);
            resendButton.disabled = false;
        }
    }, 1000);  
}

function showOtpSection(data) {
    const verifyBtn = document.getElementById('verifyBtn')
    const loginBtn = document.getElementById('loginBtn')

    document.getElementById('otpSection').classList.remove('d-none')
    document.getElementById('email').disabled = true
    document.getElementById('password').disabled = true
    document.getElementById('otpCode').disabled = false
    verifyBtn.classList.remove('d-none')
    verifyBtn.disabled = false
    loginBtn.disabled = true
    loginBtn.classList.add('d-none')

    startTimer();
    popAlert(data);
}

function login() {
    const formData = new FormData();
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const role = document.querySelector('input[name="role"]').value;

    formData.append('email', email);
    formData.append('password', password);
    
    fetch(`/login/${role}/`, {
        method : 'POST',
        headers : {
            'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body : formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showOtpSection(data);
        }
        else {
            popAlert(data);
        }
    })
    .catch(error => {
        popAlert({'status':'error', 'message':error})
    })
}

function verifyOtp() {
    const formData = new FormData();
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const otp_code = document.querySelector('input[name="otp_code"]').value;

    formData.append('email', email);
    formData.append('password', password);
    formData.append('otp_code', otp_code);

    fetch('/verify-otp/',{
        method:'POST',
        headers:{
            'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: formData 
    })
    .then(response => response.json())
    .then(data => {
        if(data.status === 'success'){
            window.location.href = data.success_url
        }
        else{
            popAlert(data)
        }
    })
    .catch(error => {
        popAlert({'status':'error', 'message':error})
    })

}

const loginForm = document.getElementById('loginForm')
if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        (event.submitter.id == 'loginBtn') ? login() : verifyOtp()
    })
}

const changePasswordForm = document.getElementById('changePasswordForm')
if (changePasswordForm) {
    changePasswordForm.addEventListener('submit', function(event) {
        event.preventDefault();

        fetch('/change-password/', {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(changePasswordForm)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.success_url
            }
            else {
                popAlert(data)
            }
        })
        
    })
}