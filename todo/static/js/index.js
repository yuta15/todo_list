
const delete_form = document.getElementById('delete');
delete_form.addEventListener('click', () => {
    delete_todo(delete_form);
})

function delete_todo(todo_tag){
    // deleteボタンがクリックされた際の処理
    
    const current_url = window.location.href;
    console.log(todo_tag);
    console.log(current_url);
}