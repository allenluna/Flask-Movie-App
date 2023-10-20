let search = document.getElementById("search");
let searhBtn = document.getElementById("searchBtn");
let searchData = document.getElementById("searchData");
let searchMenu = document.querySelector(".search-menu");

let dataArray;
fetch(`${window.origin}`, { 
    "method" : "POST",
    "headers" : {"Content-Type" : "application/json"},
    "body" : JSON.stringify({"search" : search.value})
}).then(res => res.json()).then((res) => {
    dataArray = res["data"];
}).then(() => {
    
    datas = []
    search.addEventListener("input", (e) => {
        const value = e.target.value.toLowerCase();
        datas.forEach(data => {
            const isVisible = data.title.includes(value);
            data.element.classList.toggle("data", !isVisible)

        });

    });

    
        
    datas = dataArray.map(searchData => {
        
        let a = document.createElement("a");
        let div = document.createElement("div");
        let wrapper = document.createElement("div");
        let img = document.createElement("img");
        let p = document.createElement("p");

        a.classList.add("text-secondary");
        a.classList.add("datas");
        div.classList.add("search-data");
        wrapper.classList.add("search-wrapper");
        
        
        
        a.appendChild(div);
        div.appendChild(wrapper);
        wrapper.appendChild(img);
        wrapper.appendChild(p);

        img.setAttribute("src", searchData.image);
        p.innerHTML = searchData.title;
        
        searchMenu.appendChild(a)

        return {title: searchData.title.toLowerCase(), element: a}

    })
    
});
