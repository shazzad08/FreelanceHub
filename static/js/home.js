// Project Slider Controls
const slider = document.getElementById('projectSlider');

document.getElementById('nextBtn').onclick = () => {
    slider.scrollBy({
        left: 320,
        behavior: 'smooth'
    });
};

document.getElementById('prevBtn').onclick = () => {
    slider.scrollBy({
        left: -320,
        behavior: 'smooth'
    });
};




  
const searchInput = document.getElementById("searchInput");
const suggestionsBox = document.getElementById("suggestions");

console.log("Autocomplete loaded");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {
        const query = this.value.trim();

        console.log("Typing:", query);

        if (query.length < 1) {
            suggestionsBox.innerHTML = "";
            return;
        }

        fetch(`/projects/search-suggestions/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                console.log("Suggestions:", data);

                suggestionsBox.innerHTML = "";

                data.forEach(item => {
                    const div = document.createElement("div");
                    div.classList.add("suggestion-item");
                    div.innerText = item;

                    div.onclick = function () {
                        searchInput.value = item;
                        suggestionsBox.innerHTML = "";
                    };

                    suggestionsBox.appendChild(div);
                });
            })
            .catch(error => console.error(error));
    });
}