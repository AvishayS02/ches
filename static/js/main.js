    document.addEventListener('DOMContentLoaded', function (){ 
        const accessToken = localStorage.getItem('access_token');
        const navbarAuth = document.getElementById('authNav');
        const appDiv = document.getElementById('app');

        if (accessToken) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
            verifyToken(accessToken)
                .then(valid => {
                    if (valid) {
                        updateAuthenticatedUI();
                    } else {
                        handleLogout();
                    }
                })
                .catch(error => {
                    console.error('Token verification error:', error);
                    handleLogout();
                });
        } else {
            updateNavbarForGuest();
        }

    // Update Navbar for Authenticated User
function updateAuthenticatedUI() {
        const username = localStorage.getItem('username');
        navbarAuth.innerHTML = `
            <li class="nav-item">
                <span class="nav-link text-white">Welcome, ${username}!</span>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link btn btn-outline-light" id="logoutButton">Logout</a>
            </li>
        `;

        // Add logout event listener
        document.getElementById('logoutButton').addEventListener('click', handleLogout);
    }

    // Handle Logout
function handleLogout() {
    localStorage.clear(); // Remove tokens and username
    delete axios.defaults.headers.common['Authorization']; // Remove token from headers
    updateNavbarForGuest(); // Update UI for guest
    appDiv.innerHTML = ''; // Clear any app-specific content
    window.location.href = '/login/'; // Redirect to login page
    }

    // Verify JWT Token
async function verifyToken(token) {
        try {
            await axios.post('http://127.0.0.1:8000/api/users/token/verify/', { token });
        } catch (error) {
            throw new Error('Token verification failed');
        }
    }

    // Update Navbar for Guests
function updateNavbarForGuest() {
        navbarAuth.innerHTML = `
            <li class="nav-item">
                <a href="/login/" class="nav-link">Login</a>
            </li>
            <li class="nav-item">
                <a href="/register/" class="nav-link">Register</a>
            </li>
        `;
    }

    // Handle Login Form Submission
const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            axios.post('http://127.0.0.1:8000/api/users/login/', {
                username: username,
                password: password
            })
            .then(response => {
                const { access, refresh } = response.data;
                if (access && refresh) {
                    localStorage.setItem('access_token', access);
                    localStorage.setItem('refresh_token', refresh);
                    localStorage.setItem('username', username);
                    axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
                    updateAuthenticatedUI();
                    window.location.href = '/';
                } else {
                    alert('Login successful but no tokens received.');
                }
            })
            .catch(error => {
                console.error('Login error:', error.response ? error.response.data : error);
                const errorMessageDiv = document.getElementById('errorMessage');
                if (errorMessageDiv) {
                    errorMessageDiv.style.display = 'block';
                    errorMessageDiv.textContent = error.response && error.response.data
                        ? 'Invalid username or password. Please try again.'
                        : 'An unexpected error occurred. Please try again later.';
                }
            });
        });
    }
});
