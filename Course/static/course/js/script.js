const createCourseForm = document.getElementById('createCourseForm')
if (createCourseForm) {
    createCourseForm.addEventListener('submit', function(event) {
        event.preventDefault();

        fetch('/course/create/', {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(createCourseForm)
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

const updateCourseForm = document.getElementById('updateCourseForm')
if (updateCourseForm) {
    updateCourseForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const courseId = document.getElementById('courseId').value

        fetch(`/course/update/${courseId}/`, {
            method : 'POST',
            headers : {
                'X-CSRFToken':document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body : new FormData(updateCourseForm)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.success_url
            }
            else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
                popAlert(data)
            }
        })
    })
}

function createSection(sectionNumber) {
    return `
        <div class="col-11 section-item" data-prefix="sections" data-section-number="${sectionNumber}">

            <div class="card border border-dark shadow">
                
                <div class="card-header border-bottom border-dark bg-secondary-subtle">

                    <div class="row align-items-center">

                        <div class="col-10">
                            <div class="row">
                                <label class="col-sm-2 col-form-label text-dark fw-semibold section-label">Section (${sectionNumber}) :</label>
                                <div class="col-sm-10">
                                    <input type="text" class="form-control" name="section_title[]" required>
                                    <input type="hidden" class="form-control" name="section_order[]" value="${sectionNumber}">
                                </div>
                            </div>
                        </div>

                        <div class="col-2 text-end">
                            <i class="bi bi-trash text-danger fs-5 remove-section"></i>
                        </div>

                    </div>

                </div>

                <div class="card-body pt-4">

                    <div class="row g-3 item-container">
                        ${createVideoItem(sectionNumber, 1)}
                    </div>

                    <div class="row justify-content-end">

                        <div class="col-auto">
                            <div class="btn-group">
                                <button type="button" class="btn btn-primary btn-sm dropdown-toggle add-item-dropdown" data-bs-toggle="dropdown" aria-expanded="false">
                                    <i class="bi bi-plus"></i> Add Item
                                </button>
                                <ul class="dropdown-menu">
                                    <li><a class="dropdown-item addItem" href="#" data-type="video" data-section="${sectionNumber}">Video</a></li>
                                    <li><a class="dropdown-item addItem" href="#" data-type="quiz" data-section="${sectionNumber}">Quiz</a></li>
                                </ul>
                            </div>
                        </div>

                    </div>

                </div>

            </div>

        </div>
    `
}

function createVideoItem(sectionNumber, order) {
    return `
        <div class="col-12 item">

            <input type="hidden" class="form-control" name="sections[${sectionNumber}][items][type][]" value="lesson">
            <input type="hidden" class="form-control" name="sections[${sectionNumber}][items][order][]" value="${order}">

            <div class="row align-items-center video-item">

                <!-- Video Item Fields -->
                <div class="col-11">

                    <div class="row g-3 justify-content-end">
                        
                        <!-- Video Item Title Field -->
                        <div class="col-12">

                            <div class="row">
                                <label class="col-sm-3 col-form-label video-label">(${order}) Video Title :</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" name="sections[${sectionNumber}][items][${order}][title][]" required>
                                </div>
                            </div>

                        </div>

                        <!-- Video Item Files Fields -->
                        <div class="col-9">

                            <div class="row">
                                <div class="col-6">
                                    <label class="form-label">Video File :</label>
                                    <input type="file" class="form-control" name="sections[${sectionNumber}][items][${order}][video_file][]" required>
                                </div>

                                <div class="col-6">
                                    <label class="form-label">Note File (Optional) :</label>
                                    <input type="file" class="form-control" name="sections[${sectionNumber}][items][${order}][note_file][]">
                                </div>    
                            </div>

                        </div>

                    </div>

                </div>
                
                <!-- Delete Video Item -->
                <div class="col-1 text-end">
                    <i class="bi bi-trash text-danger fs-5 remove-item"></i>
                </div>

            </div>
            
            <hr>
        </div>
    
    `
}

function createQuizItem(sectionNumber, order) {
    return `
        <div class="col-12 item">

            <input type="hidden" class="form-control" name="sections[${sectionNumber}][items][type][]" value="quiz">
            <input type="hidden" class="form-control" name="sections[${sectionNumber}][items][order][]" value="${order}">

            <div class="row align-items-center quiz-item">

                <!-- Quiz Item Fields -->
                <div class="col-11">

                    <div class="row g-3 justify-content-end">

                        <!-- Quiz Item Question Field -->
                        <div class="col-12">

                            <div class="row">
                                <label class="col-sm-3 col-form-label quiz-label">(${order}) Quiz :</label>
                                <div class="col-sm-9">
                                    <input type="text" class="form-control" name="sections[${sectionNumber}][items][${order}][question][]" required>
                                </div>
                            </div>

                        </div>

                        <!-- Quiz Item Option Fields -->
                        <div class="col-9">
                            
                            <div class="row g-2">
                                ${createQuizOption(sectionNumber, order, 1)}
                                ${createQuizOption(sectionNumber, order, 2)}
                                ${createQuizOption(sectionNumber, order, 3)}
                                ${createQuizOption(sectionNumber, order, 4)}
                            </div>

                        </div>

                    </div>

                </div>

                <!-- Delete Quiz Item -->
                <div class="col-1 text-end">
                    <i class="bi bi-trash text-danger fs-5 remove-item"></i>
                </div>

            </div>

        <hr>

        </div>

    `
}

function createQuizOption(sectionNumber, order, optionNumber) {
    return `
        <div class="col-6">

            <div class="row">

                <label class="col-sm-3 col-form-label">(${optionNumber}) :</label>
                <div class="col-sm-7">
                    <input type="text" class="form-control" name="sections[${sectionNumber}][items][${order}][options][${optionNumber}][text][]" required>
                </div>
                <div class="col-sm-2">
                    <input type="radio" name="sections[${sectionNumber}][items][${order}][is_correct][]" value="${optionNumber}" class="form-check-input" required>
                </div>
            </div>

        </div>
    `;
}

function scrollToElement(element) {
    element.scrollIntoView({ behavior: "smooth", block: "center" });
}

function updateSectionNumbers() {
    const sections = document.querySelectorAll(".section-item");

    sections.forEach((section, index) => {
        let newSectionNumber = index + 1;
        section.setAttribute('data-section-number', newSectionNumber);
        section.setAttribute('data-section', newSectionNumber);
        sectionOrder = section.querySelector(`input[name="section_order[]"]`);
        sectionOrder.value = newSectionNumber;

        const sectionLabel = section.querySelector(".section-label");
        if (sectionLabel) {
            sectionLabel.textContent = `Section (${newSectionNumber}) :`;
        }
        updateItemNumber(section);
    });
}

function updateItemNumber(section) {
    const itemContainer = section.querySelector('.item-container');
    const items = itemContainer.querySelectorAll('.item')
    const sectionPrefix = section.dataset.prefix;
    
    items.forEach((item, index) => {
        const itemId = item.querySelector(`input[name^='old_sections'][name$='[items][item_id][]']`);
        const itemType = item.querySelector(`input[name$='[items][type][]']`);
        const itemOrder = item.querySelector(`input[name$='[items][order][]']`);
        const videoLabel = item.querySelector(".video-label");
        const quizLabel = item.querySelector(".quiz-label");
        newOrderNumber = index + 1

        if (itemId) {
            itemId.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][item_id][]`
        }
        itemOrder.value = newOrderNumber

        if (videoLabel) {
            const videoId = item.querySelector(`input[name^='old_sections'][name$='[video_id][]']`);
            const videoTitle = item.querySelector(`input[name$='[title][]']`);
            const videoFile = item.querySelector(`input[name$='[video_file][]']`);
            const noteFile = item.querySelector(`input[name$='[note_file][]']`);

            if (videoId) {
                videoId.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][video_id][]`
            }

            videoLabel.textContent = `(${newOrderNumber}) Video Title :`;
            itemType.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][type][]`
            itemOrder.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][order][]`
            videoTitle.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][title][]`;
            videoFile.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][video_file][]`;
            noteFile.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][note_file][]`;
        }

        if (quizLabel) {
            const quizId = item.querySelector(`input[name^='old_sections'][name$='[quiz_id][]']`);
            const quizQuestion = item.querySelector(`input[name$='[question][]']`);

            const optionIds = item.querySelectorAll(`input[name^='old_sections'][name*='[options]'][name$='[option_id][]'`);     
            const quizOptions = item.querySelectorAll(`input[name*='[options]'][name$='[text][]`);     
            const correctAnswerRadios = item.querySelectorAll(`input[type='radio']`);

            
            if (quizId) {
                console.log("FOUND")
                quizId.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][quiz_id][]`
            }

            quizLabel.textContent = `(${newOrderNumber}) Quiz :`;
            itemType.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][type][]`
            itemOrder.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][order][]`
            quizQuestion.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][question][]`;

            optionIds.forEach((option, optionIndex) => {
                option.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][options][${optionIndex + 1}][option_id][]`;
            });

            quizOptions.forEach((option, optionIndex) => {
                option.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][options][${optionIndex + 1}][text][]`;
            });

            correctAnswerRadios.forEach((radio) => {
                radio.name = `${sectionPrefix}[${section.dataset.sectionNumber}][items][${newOrderNumber}][is_correct][]`;
            });
        }
    });
}

let sectionCount = document.querySelectorAll('.section-item').length || 0;

const sectionContainer = document.getElementById("sectionContainer");
if (sectionContainer) {

    if (sectionCount === 0) {
        sectionCount++
        sectionContainer.innerHTML += createSection(sectionCount);    
    }

    const addSection = document.getElementById("addSection");
    if (addSection) {
        addSection.addEventListener("click", function(event) {
            event.preventDefault();  
            let sectionCount = document.querySelectorAll('.section-item').length || 0;
            sectionCount++;
            const newSection = createSection(sectionCount);
            document.getElementById("sectionContainer").insertAdjacentHTML('beforeend', newSection);
            scrollToElement(document.querySelector(`[data-section-number="${sectionCount}"]`));
        });
    }   
    

    sectionContainer.addEventListener("click", function (e) {

        // ADD NEW ITEM
        if (e.target && e.target.classList.contains("addItem")) {
            e.preventDefault();
            const sectionNumber = e.target.getAttribute('data-section');
            const section = e.target.closest('.section-item');
            const itemContainer = section.querySelector('.item-container');
            let itemType = e.target.getAttribute('data-type');
            let newItem;

            if (itemType === 'video') {
                newItem = createVideoItem(sectionNumber, itemContainer.querySelectorAll('.item').length + 1);
            } 
            else if (itemType === 'quiz') {
                newItem = createQuizItem(sectionNumber, itemContainer.querySelectorAll('.item').length + 1);
            }

            itemContainer.insertAdjacentHTML('beforeend', newItem);
            scrollToElement(itemContainer.lastElementChild);
        }

        // Handle remove Video/Quiz
        if (e.target && e.target.classList.contains("remove-item")) {
            const section = e.target.closest('.section-item');
            e.target.closest('.item').remove();
            updateItemNumber(section);  
        }

        // Handle remove section
        if (e.target && e.target.classList.contains("remove-section")) {
            e.target.closest('.section-item').remove();
            updateSectionNumbers();  // Update section numbers after removal
        }
    });

}

const saveCurriculumForm = document.getElementById('saveCurriculumForm')
if (saveCurriculumForm) {
    saveCurriculumForm.addEventListener('submit', function(event) {
        event.preventDefault();
    
        const courseId = document.getElementById('courseId').value;
        const url = `/course/save/curriculum/${courseId}/`;
    
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            },
            body: new FormData(saveCurriculumForm)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.success_url;
            } else {
                popAlert(data);
            }
        });
    });
}


function createQuestionField(order) {
    return `
        <div class="col-11 question-item" data-prefix="question" data-question-number="${order}">
            <div class="row align-items-center">

                <div class="col-11">

                    <div class="row g-3 justify-content-end">
                        <div class="col-12">
                            <div class="row">
                                <label class="col-sm-2 col-form-label question-label">(${order}) Question :</label>
                                <div class="col-sm-8">
                                    <input type="hidden" class="form-control" name="question[order][]" value="${order}">
                                    <textarea class="form-control" name="question[]" required></textarea>
                                </div>
                                <div class="col-sm-2">
                                    <input type="number" class="form-control" name="mark[]" placeholder="Marks" required>
                                </div>
                            </div>
                        </div>

                        <!-- Options -->
                        <div class="col-10">
                            <div class="row g-2">
                                ${createAnswerField(order, 1)}
                                ${createAnswerField(order, 2)}
                                ${createAnswerField(order, 3)}
                                ${createAnswerField(order, 4)}
                            </div>
                        </div>
                    </div>
                    
                </div>

                <div class="col-1 text-end">
                    <i class="bi bi-trash text-danger fs-5 remove-question"></i>
                </div>
            </div>

        </div>
    `;
}

function createAnswerField(order, number) {
    return `
        <div class="col-6">
            <div class="row">
                <label class="col-sm-2 col-form-label">${number} :</label>
                <div class="col-sm-8">
                    <input type="text" class="form-control" name="question[answer][${order}][]" required>
                </div>
                <div class="col-sm-2">
                    <input type="radio" name="question[is_correct][${order}][]" value="${number}" class="form-check-input" required>
                </div>
            </div>
        </div>
    `;
}

let questionCount = document.querySelectorAll('.question-item').length || 0;

const examContainer = document.getElementById("examContainer");
if (examContainer) {

    if (questionCount === 0) {
        questionCount++;
        examContainer.innerHTML += createQuestionField(questionCount);    
    }

    const addQuestion = document.getElementById("addQuestion");
    if (addQuestion) {
        addQuestion.addEventListener("click", function(event) {
            event.preventDefault();  
            questionCount++;
            const newQuestion = createQuestionField(questionCount);
            examContainer.insertAdjacentHTML('beforeend', newQuestion);
            scrollToElement(document.querySelector(`[data-question-number="${questionCount}"]`));
        });
    }


    examContainer.addEventListener('click', function(event) {
        if (event.target && event.target.classList.contains("remove-question")) {
            event.target.closest('.question-item').remove();
            updateQuestionNumbers();
        }
    });
}



function updateQuestionNumbers() {
    const questions = document.querySelectorAll(".question-item");
    
    questions.forEach((question, index) => {

        let newQuestionNumber = index + 1;
        question.setAttribute('data-question-number', newQuestionNumber);
        
        const questionOrder = question.querySelector(`input[name*='[order]']`)
        questionOrder.value = newQuestionNumber

        // Update question label
        const questionLabel = question.querySelector(".question-label");
        if (questionLabel) {
            questionLabel.textContent = `(${newQuestionNumber}) Question :`;
        }

        const answer_ids = question.querySelectorAll(`input[name*='[answer_id]']`);        
        answer_ids.forEach((answer) => {
            const name = answer.getAttribute("name");
            const newName = name.replace(/\[answer_id]\[(\d+)]/, `[answer_id][${newQuestionNumber}]`);
            answer.setAttribute("name", newName);
        })

        const answers = question.querySelectorAll('input[name*="[answer]"]');
        answers.forEach((answer) => {
            const name = answer.getAttribute("name");
            const newName = name.replace(/\[answer]\[(\d+)]/, `[answer][${newQuestionNumber}]`);
            answer.setAttribute("name", newName);
        });

        const correctAnswerRadios = question.querySelectorAll('input[name*="[is_correct]"]');
        correctAnswerRadios.forEach((radio) => {
            const name = radio.getAttribute("name");
            const newName = name.replace(/\[is_correct]\[(\d+)]/, `[is_correct][${newQuestionNumber}]`);
            radio.setAttribute("name", newName);
        });

    });
}

// Form submission with fetch
const createQuestionForm = document.getElementById('createQuestionForm');
if (createQuestionForm) {
    createQuestionForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const courseId = document.getElementById('courseId').value;

        const url = `/course/detail/exam/${courseId}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value,
            },
            body: new FormData(createQuestionForm),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.success_url;
            } else {
                popAlert(data);
            }
        });
    });
}