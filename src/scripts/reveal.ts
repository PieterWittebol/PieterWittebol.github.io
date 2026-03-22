let observer: IntersectionObserver | null = null;

function setupReveal(): void {
  // Disconnect any previous observer
  if (observer) observer.disconnect();

  // Handle data-reveal-group: write data-reveal="up" + staggered delays onto each direct child
  document.querySelectorAll('[data-reveal-group]').forEach((group) => {
    Array.from(group.children).forEach((child, i) => {
      child.setAttribute('data-reveal', 'up');
      (child as HTMLElement).style.transitionDelay = `${i * 80}ms`;
    });
  });

  // Observe all [data-reveal] elements
  const elements = document.querySelectorAll<HTMLElement>('[data-reveal]');

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer?.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' },
  );

  elements.forEach((el) => {
    el.classList.add('reveal');
    observer!.observe(el);
  });
}

// Strip is-visible from the incoming document BEFORE the swap so cached pages
// (e.g. back-navigation) don't arrive with elements already in their visible state.
// This fires during the view-transition animation — while the outgoing page exits
// and the incoming page enters — so the new content starts hidden and reveals fresh.
document.addEventListener('astro:before-swap', (event) => {
  const incoming = (event as CustomEvent & { newDocument: Document }).newDocument;
  incoming.querySelectorAll('.is-visible').forEach((el) => el.classList.remove('is-visible'));
});

// Re-run on every page load (initial load + ClientRouter navigations)
document.addEventListener('astro:page-load', setupReveal);
