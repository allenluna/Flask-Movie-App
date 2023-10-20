if(document.querySelector(".popularWatchList") != null){
    document.querySelector(".popularWatchList").addEventListener("click", () => {
        let id = document.querySelector(".popularWatchList").id
        fetch(`/mylist-item?popular_id=${id}`)
        .then(res => res.json())
        .then(res => {
            let popularData = res["results"]
            if(popularData != "Already added in a lists."){
                window.setTimeout(() => {
                    $("#success-alert").fadeTo(2000, 500).slideUp(500, function() {
                        $("#success-alert").slideUp(500);
                    });
                    document.querySelector("#success-alert").insertAdjacentHTML(
                        "afterbegin",
                    `${popularData.title} has been added to the list.`
                    )
                });
            }else{
                window.setTimeout(() => {
                    $("#success-alert").fadeTo(2000, 500).slideUp(500, function() {
                        $("#success-alert").slideUp(500);
                    });
                    document.querySelector("#success-alert").innerHTML =`
                        ${popularData}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    
                    `
                    
                });
            }
            
        })
    })
}else if(document.querySelector(".upcommingWatchList") != null){
    document.querySelector(".upcommingWatchList").addEventListener("click", () => {
        let id = document.querySelector(".upcommingWatchList").id
        fetch(`/mylist-item?upcomming_id=${id}`)
        .then(res => res.json())
        .then(res => {
            let popularData = res["results"]
            if(popularData != "Already added in a lists."){
                window.setTimeout(() => {
                    $("#success-alert").fadeTo(2000, 500).slideUp(500, function() {
                        $("#success-alert").slideUp(500);
                    });
                    document.querySelector("#success-alert").insertAdjacentHTML(
                        "afterbegin",
                    `${popularData.title} has been added to the list.`
                    )
                });
            }else{
                window.setTimeout(() => {
                    $("#success-alert").fadeTo(2000, 500).slideUp(500, function() {
                        $("#success-alert").slideUp(500);
                    });
                    document.querySelector("#success-alert").innerHTML =`
                        ${popularData}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    
                    `
                    
                });
            }
            
        })
    })
}else if(document.querySelector(".moviesWatchList") != null){
    document.querySelector(".moviesWatchList").addEventListener("click", () => {
        let id = document.querySelector(".moviesWatchList").id
        fetch(`/mylist-item?movie_id=${id}`)
        .then(res => res.json())
        .then(res => {
            let popularData = res["results"]
            if(popularData != "Already added in a lists."){
                window.setTimeout(() => {
                    $("#success-alert").fadeTo(2000, 500).slideUp(500, function() {
                        $("#success-alert").slideUp(500);
                    });
                    document.querySelector("#success-alert").insertAdjacentHTML(
                        "afterbegin",
                    `${popularData.title} has been added to the list.`
                    )
                });
            }else{
                window.setTimeout(() => {
                    $("#success-alert").fadeTo(2000, 500).slideUp(500, function() {
                        $("#success-alert").slideUp(500);
                    });
                    document.querySelector("#success-alert").innerHTML =`
                        ${popularData}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    
                    `
                    
                });
            }
            
        })
    })
}

