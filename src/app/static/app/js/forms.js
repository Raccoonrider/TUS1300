// Restrict Elites to marathon

let routeDropdown = document.querySelector("#id_route")
let categoryDropdown = document.querySelector("#id_category")

let marathonId = routeDropdown.querySelectorAll("option")[0]
let eliteId = categoryDropdown.querySelectorAll("option")[1]

categoryDropdown.onchange = () => {
    if (categoryDropdown.value == eliteId){
        routeDropdown.value = marathonId
    }
}

routeDropdown.onchange = () => {
    if (routeDropdown.value != marathonId){
        categoryDropdown.value = 0
    }
}