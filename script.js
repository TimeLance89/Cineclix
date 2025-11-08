const initAccordion = () => {
  const accordions = document.querySelectorAll('[data-accordion]');
  accordions.forEach((accordion) => {
    const triggers = accordion.querySelectorAll('.accordion-trigger');
    triggers.forEach((trigger) => {
      const content = trigger.nextElementSibling;
      trigger.addEventListener('click', () => {
        const expanded = trigger.getAttribute('aria-expanded') === 'true';
        trigger.setAttribute('aria-expanded', String(!expanded));
        content.hidden = expanded;
      });
      trigger.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          trigger.click();
        }
      });
    });
  });
};

const initTocHighlight = () => {
  const tocLinks = Array.from(document.querySelectorAll('.toc a'));
  if (tocLinks.length === 0 || typeof IntersectionObserver === 'undefined') return;

  const sectionMap = tocLinks
    .map((link) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return null;
      return { link, target };
    })
    .filter(Boolean);

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const match = sectionMap.find((item) => item.target === entry.target);
        if (!match) return;
        if (entry.isIntersecting) {
          tocLinks.forEach((anchor) => anchor.classList.remove('is-active'));
          match.link.classList.add('is-active');
        }
      });
    },
    {
      rootMargin: '-45% 0px -45% 0px',
      threshold: [0.1, 0.25]
    }
  );

  sectionMap.forEach((item) => observer.observe(item.target));
};

const initSmoothScroll = () => {
  const tocLinks = document.querySelectorAll('.toc a');
  tocLinks.forEach((link) => {
    link.addEventListener('click', (event) => {
      const targetId = link.getAttribute('href');
      if (!targetId?.startsWith('#')) return;
      const target = document.querySelector(targetId);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', targetId);
    });
  });
};

window.addEventListener('DOMContentLoaded', () => {
  initAccordion();
  initTocHighlight();
  initSmoothScroll();
});
