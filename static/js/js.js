console.log("hello world")




var alerted=document.getElementById("remove")

setTimeout(() => {
    alerted.style.display=('none');
}, 3000);




let currentQuestionIndex=0 

function fetchQuestions(){
    fetch('https://opentdb.com/api.php?amount=10&category=27&difficulty=easy&type=multiple').then((response)=>{
    return response.json();
}).then((data)=>{
    questions=data.results;
    displayQuestion(questions[currentQuestionIndex]);
});
}




function shuffleArray(array) {
    const flattenedArray = array.flat(); // Flatten the nested array
    for (let i = flattenedArray.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [flattenedArray[i], flattenedArray[j]] = [flattenedArray[j], flattenedArray[i]];
    }
    return flattenedArray;
}
function displayQuestion(question){
    // Combine incorrect answers and correct answer into a single array
    const allOptions = question.incorrect_answers.concat(question.correct_answer);
    // Shuffle the combined array
    const shuffledOptions = shuffleArray(allOptions);
    
    // Find the index of the correct answer in the shuffled options
    const correctAnswerIndex = shuffledOptions.findIndex(option => option === question.correct_answer);
    
    // Move the correct answer to a random position within the shuffled options array
    const randomIndex = Math.floor(Math.random() * (shuffledOptions.length - 1));
    [shuffledOptions[correctAnswerIndex], shuffledOptions[randomIndex]] = [shuffledOptions[randomIndex], shuffledOptions[correctAnswerIndex]];

    // Display the shuffled options in the HTML
    question_container = document.getElementById('question-container');
    question_container.innerHTML = `
    <p><strong>${question.question}</strong></p>
    <ul>
        ${shuffledOptions.map(answer => `
            <li><input type="radio" name="question_${currentQuestionIndex}" value="${answer}">${answer}</li>
        `).join('')}
    </ul>
    `;
}





// function displayQuestion(question){
//     const allOptions = question.incorrect_answers.concat(question.correct_answer);
//     const shuffledOptions=shuffleArray(allOptions)
//     question_container=document.getElementById('question-container');
//     question_container.innerHTML=`
//     <p><strong>${question.question}</strong></p>
//     <ul>
//         <li><input type="radio" name="question_${currentQuestionIndex}" value="${question.correct_answer}">${question.correct_answer}</li>
//         ${shuffledOptions.map(answer => `
//             <li><input type="radio" name="question_${currentQuestionIndex}" value="${answer}">${answer}</li>
//         `).join('')}
//     </ul>
// `


//     // console.log(question.question)
//     // console.log('Options:')
//     // question.incorrect_answers.forEach(element => {
//     //     console.log(element)
//     // });
//     // console.log(question.correct_answer);
// }

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
            window.location.href="/home";
        } 
    }
    else{
        alert("Incorrect answer. Quiz ended");
        window.location.href="/home"
    }   
});


fetchQuestions()
