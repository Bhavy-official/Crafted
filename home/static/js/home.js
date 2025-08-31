const postsContainer = document.getElementById('posts-container');
const searchInput = document.getElementById('search');
const sortSelect = document.getElementById('sort-filter');
const blogToggle = document.getElementById('blog-toggle');
const projectToggle = document.getElementById('project-toggle');
const colors = ['#1e3a8a', '#581c87', '#065f46', '#9d174d', '#7c2d12'];

const authAxios = axios.create();

authAxios.interceptors.request.use(config => {
  const accessToken = localStorage.getItem("access_token");
  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }
  return config;
});

authAxios.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem("refresh_token");
      if (refreshToken) {
        try {
          const res = await axios.post('/api/refresh/', { refresh: refreshToken });
          const newAccessToken = res.data.access;
          localStorage.setItem("access_token", newAccessToken);
          originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
          return authAxios(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }
    return Promise.reject(error);
  }
);

function sortPosts(posts, sortType) {
  switch (sortType) {
    case 'latest':
      return posts.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    case 'oldest':
      return posts.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    case 'likes':
      return posts.sort((a, b) => (b.likes_count || 0) - (a.likes_count || 0));
    default:
      return posts;
  }
}

async function fetchPosts(postType = 'blog', query = '', sort = '') {
  let url = `/api/posts/?post_type=${postType}`;
  if (query) url += `&search=${encodeURIComponent(query)}`;

  try {
    const res = await authAxios.get(url);
    let posts = res.data;

    posts = sortPosts(posts, sort);

    postsContainer.innerHTML = '';

    if (posts.length === 0) {
      postsContainer.innerHTML = `<p>No ${postType.charAt(0).toUpperCase() + postType.slice(1)} found, Be the first one to Write it.</p>`;
      return;
    }

    posts.forEach((post) => {
      const snippet =
        post.description.length > 150
          ? post.description.slice(0, 150) + '...'
          : post.description;
      const tagsHtml = post.tags
        ? post.tags
            .split(',')
            .map(tag => `<span style="background-color: ${getTagColor(tag.trim())}; color: #fff;">${tag.trim()}</span>`)
            .join(' ')
        : '';

      postsContainer.innerHTML += `
        <article class="card">
          ${post.image ? `<img src="${post.image}" alt="${post.title}">` : ''}
          <div class="card-content">
            <div class="card-tags">${tagsHtml}</div>
            <h2>${post.title}</h2>
            <p class="card-para">${snippet}</p>
            <div class="card-actions">
              <div class="like_comts">
                <span><span class="material-symbols-outlined" style="color:red;">favorite</span> ${post.likes_count || 0}</span>
                <span><span class="material-symbols-outlined" style="color:#0040ff;">comment</span> ${post.comments_count || 0}</span>
              </div>
              <a href="/post/${post.id}/">Read More <span class="material-symbols-outlined">arrow_forward</span></a>
            </div>
          </div>
        </article>
      `;
    });
  } catch (err) {
    console.error(err);
    postsContainer.innerHTML = '<p>Failed to load posts.</p>';
  }
}

function getTagColor(tag) {
  const index = hashTag(tag) % colors.length;
  return colors[index];
}

function hashTag(tag) {
  let hash = 0;
  for (let i = 0; i < tag.length; i++) {
    hash = (hash << 5) - hash + tag.charCodeAt(i);
  }
  return hash;
}

searchInput.addEventListener('keyup', e => {
  const postType = blogToggle.classList.contains('active') ? 'blog' : 'project';
  fetchPosts(postType, e.target.value, sortSelect.value);
});

sortSelect.addEventListener('change', () => {
  const postType = blogToggle.classList.contains('active') ? 'blog' : 'project';
  fetchPosts(postType, searchInput.value, sortSelect.value);
});

blogToggle.addEventListener('click', () => {
  blogToggle.classList.add('active');
  projectToggle.classList.remove('active');
  fetchPosts('blog', searchInput.value, sortSelect.value);
});

projectToggle.addEventListener('click', () => {
  projectToggle.classList.add('active');
  blogToggle.classList.remove('active');
  fetchPosts('project', searchInput.value, sortSelect.value);
});

const toggleBtn = document.getElementById('dark-mode-toggle');
const darkModeIcon = document.getElementById('dark-mode-icon');

if (document.body.classList.contains('dark-mode')) {
  darkModeIcon.classList.remove('fa-sun');
  darkModeIcon.classList.add('fa-moon');
} else {
  darkModeIcon.classList.remove('fa-moon');
  darkModeIcon.classList.add('fa-sun');
}

toggleBtn.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
  if (document.body.classList.contains('dark-mode')) {
    darkModeIcon.classList.remove('fa-sun');
    darkModeIcon.classList.add('fa-moon');
  } else {
    darkModeIcon.classList.remove('fa-moon');
    darkModeIcon.classList.add('fa-sun');
  }
});

function getRandomPosition() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  return {
    x: Math.random() * width,
    y: Math.random() * height,
  };
}

function createFloatingIcons() {
  const icons = ['fa-star', 'fa-cloud', 'fa-heart', 'fa-moon', 'fa-sun', 'fa-rocket'];
  const iconContainer = document.createElement('div');
  iconContainer.classList.add('floating-icons');

  icons.forEach((iconClass, index) => {
    const icon = document.createElement('i');
    icon.classList.add('fas', iconClass, 'floating-icon');
    const position = getRandomPosition();
    icon.style.top = `${position.y}px`;
    icon.style.left = `${position.x}px`;
    iconContainer.appendChild(icon);
  });

  document.querySelector('header').appendChild(iconContainer);
}

window.onload = createFloatingIcons;

fetchPosts('blog');

function updateAuthLinks() {
  const accessToken = localStorage.getItem("access_token");

  const loginLink = document.getElementById('login-link');
  const logoutLink = document.getElementById('logout-link');

  if (accessToken) {
    loginLink.style.display = 'none';
    logoutLink.style.display = 'inline-block';
  } else {
    loginLink.style.display = 'inline-block';
    logoutLink.style.display = 'none';
  }
}

updateAuthLinks();

document.getElementById('logout-link').addEventListener('click', () => {
  // Clear tokens from local storage
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');


  window.location.reload();  
});

