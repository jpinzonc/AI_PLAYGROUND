const sidebar = document.getElementById('sidebar');
const toggleSidebarBtn = document.getElementById('toggle-sidebar-btn');
const themeToggleBtn = document.getElementById('theme-toggle-btn');
const body = document.body;
const userIdentificationCountInput = document.getElementById('user-identification-count');
const additionalUserIdentificationsContainer = document.getElementById('additional-user-identifications');

userIdentificationCountInput.addEventListener('change', () => {
	const count = parseInt(userIdentificationCountInput.value);
	additionalUserIdentificationsContainer.innerHTML = '';
	for (let i = 0; i < count - 1; i++) {
		const newUserIdentification = document.createElement('div');
		newUserIdentification.className = 'user-identification';
		newUserIdentification.innerHTML = `
			<input type="text" placeholder="Name">
			<input type="text" placeholder="Other ID">
		`;
		additionalUserIdentificationsContainer.appendChild(newUserIdentification);
	}
});

toggleSidebarBtn.addEventListener('click', () => {
	sidebar.classList.toggle('hidden');
});

themeToggleBtn.addEventListener('click', () => {
	body.classList.toggle('dark-mode');
	if (body.classList.contains('dark-mode')) {
		themeToggleBtn.textContent = '🌕';
	} else {
		themeToggleBtn.textContent = '☀️';
	}
});