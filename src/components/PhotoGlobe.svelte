<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let { countries }: { countries: Record<string, number> } = $props();

  let container: HTMLDivElement;
  let globe: any;
  let rotationTimer: ReturnType<typeof setTimeout>;

  // Map from plain English country name → ISO 3166-1 alpha-2 code.
  // Extend this table when adding photos from a new country.
  const COUNTRY_ISO: Record<string, string> = {
    'South Africa': 'ZA',
    'Namibia': 'NA',
    'Kenya': 'KE',
    'Oman': 'OM',
    'Sri Lanka': 'LK',
    'Sweden': 'SE',
  };

  // Reverse: ISO code → country name
  const ISO_COUNTRY: Record<string, string> = Object.fromEntries(
    Object.entries(COUNTRY_ISO).map(([name, iso]) => [iso, name])
  );

  let hoveredISO: string | null = null;

  function isVisited(feat: any): boolean {
    const iso: string = feat?.properties?.ISO_A2 ?? '';
    const name = ISO_COUNTRY[iso];
    return !!(name && countries[name]);
  }

  function getCapColor(feat: any): string {
    const iso: string = feat?.properties?.ISO_A2 ?? '';
    const name = ISO_COUNTRY[iso];
    if (!name || !countries[name]) return '#e8e4de';
    return iso === hoveredISO ? '#f26e6e' : '#b11d1d';
  }

  function startRotation() {
    globe?.controls().then?.((c: any) => { c.autoRotate = true; });
    try {
      const controls = globe?.controls();
      if (controls) {
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.3;
      }
    } catch (_) {}
  }

  function stopRotation() {
    try {
      const controls = globe?.controls();
      if (controls) controls.autoRotate = false;
    } catch (_) {}
    clearTimeout(rotationTimer);
  }

  function scheduleRotationResume() {
    clearTimeout(rotationTimer);
    rotationTimer = setTimeout(startRotation, 3000);
  }

  function solidColorDataURL(color: string): string {
    const canvas = document.createElement('canvas');
    canvas.width = 2;
    canvas.height = 2;
    const ctx = canvas.getContext('2d')!;
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, 2, 2);
    return canvas.toDataURL();
  }

  onMount(async () => {
    const { default: Globe } = await import('globe.gl');

    const geoRes = await fetch(
      'https://raw.githubusercontent.com/vasturiano/react-globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson'
    );
    const geoData = await geoRes.json();

    globe = Globe()(container)
      .width(container.clientWidth)
      .height(container.clientHeight)
      .backgroundColor('rgba(0,0,0,0)')
      .showAtmosphere(false)
      .globeImageUrl(solidColorDataURL('#d4cfc8'))
      .polygonsData(geoData.features)
      .polygonCapColor(getCapColor)
      .polygonSideColor(() => '#c9c4bc')
      .polygonStrokeColor(() => '#c9c4bc')
      .polygonAltitude(0.006)
      .polygonLabel((feat: any) => {
        const iso: string = feat?.properties?.ISO_A2 ?? '';
        const name = ISO_COUNTRY[iso];
        if (!name || !countries[name]) return '';
        const count = countries[name];
        return `<div style="background:#27272a;color:#fafafa;padding:4px 10px;border-radius:4px;font-size:13px;font-family:serif;pointer-events:none">${name} — ${count} photo${count !== 1 ? 's' : ''}</div>`;
      })
      .onPolygonHover((feat: any) => {
        const iso: string = feat?.properties?.ISO_A2 ?? '';
        const name = ISO_COUNTRY[iso];
        hoveredISO = name && countries[name] ? iso : null;
        container.style.cursor = hoveredISO ? 'pointer' : 'default';
        globe.polygonCapColor(getCapColor);
      })
      .onPolygonClick((feat: any) => {
        const iso: string = feat?.properties?.ISO_A2 ?? '';
        const name = ISO_COUNTRY[iso];
        if (name && countries[name]) {
          window.location.href = `/photography?country=${encodeURIComponent(name)}`;
        }
      });

    // Enable auto-rotation
    const controls = globe.controls();
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.3;

    // Pause on user interaction, resume after 3s
    container.addEventListener('pointerdown', () => {
      stopRotation();
    });
    container.addEventListener('pointerup', scheduleRotationResume);

    // Resize observer
    const ro = new ResizeObserver(() => {
      if (container) {
        globe.width(container.clientWidth).height(container.clientHeight);
      }
    });
    ro.observe(container);

    return () => {
      ro.disconnect();
    };
  });

  onDestroy(() => {
    clearTimeout(rotationTimer);
  });
</script>

<div bind:this={container} class="w-full h-full"></div>
