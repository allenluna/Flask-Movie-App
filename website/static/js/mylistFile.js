let listId;
let cardToDelete;
document.querySelectorAll(".remove-list").forEach(list => {
    list.addEventListener("click", (e) => {
        listId = list.id
        cardToDelete = list.parentElement.parentElement
    })
})
document.querySelector("#delete-list").addEventListener("click", () => {
    fetch(`/mylist-delete?delete=${listId}`)
    .then(res => res.json())
    .then(res => {
        document.querySelector("#mylist-wrapper").removeChild(cardToDelete);
    })
})
