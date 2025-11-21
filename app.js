document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.querySelector('.sidebar');
  const toggle = document.querySelector('.sidebar-toggle');
  const navLinks = document.querySelectorAll('.nav-link');
  const page = document.body.dataset.page;

  if (page) {
    const activeLink = document.querySelector(`.nav-link[data-link="${page}"]`);
    if (activeLink) activeLink.classList.add('active');
  }

  toggle?.addEventListener('click', () => {
    sidebar?.classList.toggle('open');
  });

  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      if (sidebar?.classList.contains('open')) {
        sidebar.classList.remove('open');
      }
    });
  });

  document.querySelectorAll('[data-checkbox]').forEach((box) => {
    box.addEventListener('click', () => {
      box.classList.toggle('checked');
    });
  });
});
