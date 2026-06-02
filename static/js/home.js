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
