document.addEventListener('DOMContentLoaded', () => {
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
            if (postsContainer) {
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
                        postsContainer.appendChild(document.createElement('br'));
                        postsContainer.appendChild(document.createElement('br'));
                    });
                }
            }
        } catch (error) {
            console.error('Error loading blog posts:', error);
            const postsContainer = document.getElementById('posts');
            if (postsContainer) {
                postsContainer.innerHTML = '<h3>[WIP]</h3>';
            }
        }
    }

    // Load blog posts
    loadBlogPosts();
});
