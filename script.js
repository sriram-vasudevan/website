// Theme toggle functionality
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

// Function to format date as "Month DD, YYYY"
function formatDate(dateString) {
    const [day, month, year] = dateString.split('-');
    const date = new Date(year, month - 1, day);
    return `[${date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}]`;
}

// Function to fetch and display blog posts
async function loadBlogPosts() {
    try {
        const response = await fetch('posts.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const posts = await response.json();

        const postsContainer = document.getElementById('posts');
        if (posts.length === 0) {
            postsContainer.innerHTML = '<h3>[WIP]</h3>';
        } else {
            posts.forEach(post => {
                const formattedDate = formatDate(post.date);
                const link = document.createElement('a');
                link.href = `posts/${post.filename}`;
                link.className = 'post-link';
                link.textContent = `${formattedDate} ${post.title}`;
                postsContainer.appendChild(link);
            });
        }
    } catch (error) {
        console.error('Error loading blog posts:', error);
        document.getElementById('posts').innerHTML = '<h3>[WIP]</h3>';
    }
}

// Load blog posts when the page is ready
document.addEventListener('DOMContentLoaded', loadBlogPosts);
