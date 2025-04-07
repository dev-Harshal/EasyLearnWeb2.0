const profileForm = document.getElementById('profileForm')
if (profileForm) {
    profileForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const role = document.getElementById('role').value

        fetch(`/${role.toLowerCase()}/profile/`, {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(profileForm)
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
        .catch(error => {
            popAlert({'status':'error', 'message':error})
        })
        
    })
}

const createTeacherForm = document.getElementById('createTeacherForm')
if (createTeacherForm) {
    createTeacherForm.addEventListener('submit', function(event) {
        event.preventDefault();

        fetch('/admin/create/teacher/',{
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(createTeacherForm)
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success'){
                window.location.href = data.success_url
            }
            else{
                window.scrollTo({ top: 0, behavior: 'smooth' });
                popAlert(data)
            }
        })
        .catch(error => {
            popAlert({'status':'error', 'message':error})
        })
        
    })
}

const updateTeacherForm = document.getElementById('updateTeacherForm')
if (updateTeacherForm) {
    updateTeacherForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const userId = document.getElementById('userId').value

        fetch( `/admin/update/teacher/${userId}/`, {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(updateTeacherForm)
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success'){
                window.location.href = data.success_url
            }
            else{
                window.scrollTo({ top: 0, behavior: 'smooth' });
                popAlert(data)
            }
        })
        .catch(error => {
            popAlert({'status':'error', 'message':error})
        })
        
    })
}