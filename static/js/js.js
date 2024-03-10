console.log("hello world")




var alerted=document.getElementById("remove")

setTimeout(() => {
    alerted.style.display=('none');
}, 2000);




let currentQuestionIndex=0 

function fetchQuestions(){
    fetch('https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=multiple').then((response)=>{
    return response.json();
}).then((data)=>{
    questions=data.results;
    displayQuestion(questions[currentQuestionIndex]);
});
}

function displayQuestion(question){
    question_container=document.getElementById('question-container');
    question_container.innerHTML=`
    <p><strong>${question.question}</strong></p>
    <ul>
        <li><input type="radio" name="question_${currentQuestionIndex}" value="${question.correct_answer}">${question.correct_answer}</li>
        ${question.incorrect_answers.map(answer => `
            <li><input type="radio" name="question_${currentQuestionIndex}" value="${answer}">${answer}</li>
        `).join('')}
    </ul>
`


    // console.log(question.question)
    // console.log('Options:')
    // question.incorrect_answers.forEach(element => {
    //     console.log(element)
    // });
    // console.log(question.correct_answer);
}

document.getElementById('quiz-form').addEventListener('submit', function(event){
    event.preventDefault();

    const selectedAnswer=document.querySelector(`input[name="question_${currentQuestionIndex}"]:checked`);
    if(!selectedAnswer){
        alert("please select an answer.")
        return;
    }

    const isCorrect = selectedAnswer.value === questions[currentQuestionIndex].correct_answer;
    if(isCorrect){
        currentQuestionIndex++
        if(currentQuestionIndex < questions.length){
            displayQuestion(questions[currentQuestionIndex]);
        } else{
            alert("Quiz Completed!!!")
        } 
    }
    else{
        alert("Incorrect answer. Quiz ended");
        window.location.href="/";
    }   
});


fetchQuestions()
