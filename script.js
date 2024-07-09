const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

function setTheme(isDark) {
    body.classList.toggle('light', !isDark);
    themeToggle.classList.toggle('light', !isDark);
}

const savedTheme = localStorage.getItem('theme');
setTheme(savedTheme !== 'light');

themeToggle.addEventListener('click', () => {
    const isDark = !body.classList.contains('light');
    setTheme(!isDark);
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
});
