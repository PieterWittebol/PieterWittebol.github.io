<script lang="ts">
  interface Link {
    href: string;
    label: string;
  }

  let { links, currentPath }: { links: Link[]; currentPath: string } = $props();
  let open = $state(false);

  function toggle() {
    open = !open;
  }

  function close() {
    open = false;
  }

  function isActive(href: string): boolean {
    return currentPath === href || (href !== '/' && currentPath.startsWith(href));
  }
</script>

<div class="md:hidden">
  <button
    onclick={toggle}
    class="p-2 text-primary-700 hover:text-primary-900 transition-colors"
    aria-label={open ? 'Close menu' : 'Open menu'}
    aria-expanded={open}
  >
    {#if open}
      <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
    {:else}
      <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    {/if}
  </button>

  {#if open}
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="fixed inset-0 z-40 bg-black/20" onclick={close} onkeydown={(e) => e.key === 'Escape' && close()}></div>

    <nav
      class="absolute top-16 right-0 left-0 z-50 bg-primary-50 border-b border-primary-200 shadow-lg"
      aria-label="Mobile navigation"
    >
      <div class="px-4 py-3 space-y-1">
        {#each links as { href, label }}
          <a
            {href}
            onclick={close}
            class="block px-3 py-2 rounded-md text-base font-medium transition-colors {isActive(href)
              ? 'text-primary-900 bg-primary-100'
              : 'text-primary-600 hover:text-primary-900 hover:bg-primary-100'}"
          >
            {label}
          </a>
        {/each}
      </div>
    </nav>
  {/if}
</div>
