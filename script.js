document.addEventListener('DOMContentLoaded', () => {
    // Function to format date as "Mon 'YY"
    function formatDate(dateString) {
        const [day, month, year] = dateString.split('-');
        const date = new Date(year, month - 1, day);
        return `${date.toLocaleString('en-US', { month: 'short' })} '${year.slice(-2)}`;
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
                        const postElement = document.createElement('div');
                        postElement.className = 'post-item';
                        
                        const dateSpan = document.createElement('span');
                        dateSpan.className = 'post-date';
                        dateSpan.textContent = formattedDate;
                        
                        const titleLink = document.createElement('a');
                        titleLink.href = `posts/${post.filename}`;
                        titleLink.className = 'post-title';
                        titleLink.textContent = post.title;
                        
                        postElement.appendChild(dateSpan);
                        postElement.appendChild(document.createTextNode(' ')); // Space between date and title
                        postElement.appendChild(titleLink);
                        
                        postsContainer.appendChild(postElement);
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
