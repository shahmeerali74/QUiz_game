
document.getElementById('loginForm').addEventListener('submit',function(event){

    if(!document.getElementById('exampleCheck1').checked){
        alert('Please check the checkbox');
        event.preventDefault()
    }
})