<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let { src, mtl, upAxis = 'Y' }: { src: string; mtl?: string; upAxis?: 'Y' | 'Z' } = $props();

  let container: HTMLDivElement;
  let loading = $state(true);
  let error = $state<string | null>(null);
  let spinning = $state(true); // auto-rotate state exposed to UI

  let animationId: number;
  let renderer: import('three').WebGLRenderer | null = null;
  let destroyed = false;

  // Actions wired up after Three.js initialises
  let resetView = () => {};
  let zoomIn = () => {};
  let zoomOut = () => {};
  let toggleSpin = () => { spinning = !spinning; };

  onDestroy(() => { destroyed = true; });

  onMount(async () => {
    try {
      // During Astro View Transitions the component can mount while the
      // container still has zero dimensions. Wait for a real layout before
      // initialising Three.js, otherwise the renderer is created at 0×0 and
      // nothing ever appears without a hard refresh.
      if (container.clientWidth === 0 || container.clientHeight === 0) {
        await new Promise<void>((resolve) => {
          const ro = new ResizeObserver((entries) => {
            // Component may have been destroyed while we were waiting.
            if (destroyed) { ro.disconnect(); resolve(); return; }
            if (entries[0].contentRect.width > 0 && entries[0].contentRect.height > 0) {
              ro.disconnect();
              resolve();
            }
          });
          ro.observe(container);
        });
      }

      // Bail out if the component was unmounted (e.g. user navigated away
      // during a View Transition) before dimensions became available.
      if (destroyed || !container) return;

      const THREE = await import('three');
      const { OBJLoader } = await import('three/addons/loaders/OBJLoader.js');
      const { MTLLoader } = await import('three/addons/loaders/MTLLoader.js');
      const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');

      if (destroyed || !container) return;

      const width = container.clientWidth;
      const height = container.clientHeight;

      // Scene
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0xf5f2ed);

      // Camera
      const camera = new THREE.PerspectiveCamera(45, width / height, 0.01, 100000);
      camera.position.set(0, 0, 5);

      // Renderer
      renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      container.appendChild(renderer.domElement);

      // Lighting — warm tones to match site palette
      const ambientLight = new THREE.AmbientLight(0xfef3c7, 1.2); // amber-100
      scene.add(ambientLight);

      const keyLight = new THREE.DirectionalLight(0xffffff, 2.0);
      keyLight.position.set(5, 10, 7.5);
      scene.add(keyLight);

      const fillLight = new THREE.DirectionalLight(0xfde68a, 0.5); // amber-200
      fillLight.position.set(-5, 2, -5);
      scene.add(fillLight);

      // OrbitControls
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.screenSpacePanning = true;
      controls.enablePan = true;
      // Right-click or middle-click to pan; left-click to rotate
      controls.mouseButtons = {
        LEFT: THREE.MOUSE.ROTATE,
        MIDDLE: THREE.MOUSE.PAN,
        RIGHT: THREE.MOUSE.PAN,
      };
      // One-finger rotate, two-finger pinch-zoom + drag-pan
      controls.touches = {
        ONE: THREE.TOUCH.ROTATE,
        TWO: THREE.TOUCH.DOLLY_PAN,
      };
      controls.autoRotate = true;
      controls.autoRotateSpeed = 1.2;

      // Pause auto-rotate on interaction; resume after 4 s of inactivity
      let resumeTimer: ReturnType<typeof setTimeout>;
      controls.addEventListener('start', () => {
        controls.autoRotate = false;
        spinning = false;
        clearTimeout(resumeTimer);
      });
      controls.addEventListener('end', () => {
        resumeTimer = setTimeout(() => {
          controls.autoRotate = true;
          spinning = true;
        }, 4000);
      });

      // Load MTL if a URL was provided alongside the OBJ
      let materials: import('three/addons/loaders/MTLLoader.js').MTLLoader.MaterialCreator | null = null;

      if (mtl) {
        try {
          const mtlLoader = new MTLLoader();
          materials = await new Promise<import('three/addons/loaders/MTLLoader.js').MTLLoader.MaterialCreator>(
            (resolve, reject) => mtlLoader.load(mtl, resolve, undefined, reject)
          );
          materials.preload();
        } catch {
          // MTL failed to load — fall back to warm wood material
        }
      }

      const objLoader = new OBJLoader();
      if (materials) objLoader.setMaterials(materials);

      const object = await new Promise<THREE.Group>((resolve, reject) =>
        objLoader.load(src, resolve, undefined, reject)
      );

      // Correct axis convention: Fusion 360 exports Z-up, Three.js is Y-up
      if (upAxis === 'Z') {
        object.rotation.x = -Math.PI / 2;
        object.updateMatrixWorld(true);
      }

      // Fall back to a warm wood-tone material when no MTL was found
      if (!materials) {
        object.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            (child as THREE.Mesh).material = new THREE.MeshStandardMaterial({
              color: 0xb45309, // amber-700
              roughness: 0.75,
              metalness: 0.0,
            });
          }
        });
      }

      // Center model at origin and fit camera
      const box = new THREE.Box3().setFromObject(object);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      const maxDim = Math.max(size.x, size.y, size.z);

      object.position.sub(center);
      scene.add(object);

      const fov = camera.fov * (Math.PI / 180);
      const dist = (maxDim / 2) / Math.tan(fov / 2) * 2.2;
      const initialPos = new THREE.Vector3(dist * 0.6, dist * 0.35, dist * 0.8);
      camera.position.copy(initialPos);
      camera.near = dist / 100;
      camera.far = dist * 100;
      camera.lookAt(0, 0, 0);
      camera.updateProjectionMatrix();

      controls.minDistance = dist * 0.3;
      controls.maxDistance = dist * 6;
      controls.update();

      loading = false;

      // Button actions
      resetView = () => {
        camera.position.copy(initialPos);
        controls.target.set(0, 0, 0);
        controls.update();
      };
      zoomIn = () => {
        const dir = camera.position.clone().normalize();
        camera.position.addScaledVector(dir, -dist * 0.15);
        controls.update();
      };
      zoomOut = () => {
        const dir = camera.position.clone().normalize();
        camera.position.addScaledVector(dir, dist * 0.15);
        controls.update();
      };
      toggleSpin = () => {
        spinning = !spinning;
        controls.autoRotate = spinning;
        clearTimeout(resumeTimer);
      };

      // Resize observer
      const resizeObserver = new ResizeObserver(() => {
        const w = container.clientWidth;
        const h = container.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer!.setSize(w, h);
      });
      resizeObserver.observe(container);

      // Render loop
      const animate = () => {
        animationId = requestAnimationFrame(animate);
        controls.update();
        renderer!.render(scene, camera);
      };
      animate();

      return () => {
        clearTimeout(resumeTimer);
        resizeObserver.disconnect();
        cancelAnimationFrame(animationId);
        renderer!.dispose();
      };
    } catch (e) {
      console.error('[ModelViewer]', e);
      error = 'Could not load the 3D model.';
      loading = false;
    }
  });

  onDestroy(() => {
    if (animationId) cancelAnimationFrame(animationId);
    if (renderer) renderer.dispose();
  });
</script>

<div class="relative w-full aspect-video rounded-lg overflow-hidden border border-gray-200 shadow-md">
  <!-- Three.js mounts its canvas here -->
  <div bind:this={container} class="w-full h-full"></div>

  <!-- Loading overlay -->
  {#if loading && !error}
    <div class="absolute inset-0 flex flex-col items-center justify-center bg-[#f5f2ed]">
      <div class="w-9 h-9 rounded-full border-2 border-gray-200 border-t-amber-500 animate-spin mb-3"></div>
      <p class="text-sm text-gray-400 tracking-wide">Loading model…</p>
    </div>
  {/if}

  <!-- Error state -->
  {#if error}
    <div class="absolute inset-0 flex items-center justify-center bg-[#f5f2ed]">
      <p class="text-sm text-gray-400">{error}</p>
    </div>
  {/if}

  <!-- Control buttons -->
  {#if !loading && !error}
    <div class="absolute top-3 right-3 flex flex-col gap-1.5">
      <!-- Zoom in -->
      <button
        onclick={zoomIn}
        title="Zoom in"
        class="w-8 h-8 flex items-center justify-center rounded bg-white/80 border border-gray-200 text-gray-500 hover:text-amber-700 hover:border-amber-300 shadow-sm transition-colors backdrop-blur-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/>
        </svg>
      </button>
      <!-- Zoom out -->
      <button
        onclick={zoomOut}
        title="Zoom out"
        class="w-8 h-8 flex items-center justify-center rounded bg-white/80 border border-gray-200 text-gray-500 hover:text-amber-700 hover:border-amber-300 shadow-sm transition-colors backdrop-blur-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="8" y1="11" x2="14" y2="11"/>
        </svg>
      </button>
      <!-- Reset view -->
      <button
        onclick={resetView}
        title="Reset view"
        class="w-8 h-8 flex items-center justify-center rounded bg-white/80 border border-gray-200 text-gray-500 hover:text-amber-700 hover:border-amber-300 shadow-sm transition-colors backdrop-blur-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>
        </svg>
      </button>
      <!-- Toggle auto-rotate -->
      <button
        onclick={toggleSpin}
        title={spinning ? 'Pause rotation' : 'Resume rotation'}
        class="w-8 h-8 flex items-center justify-center rounded border shadow-sm transition-colors backdrop-blur-sm
          {spinning
            ? 'bg-amber-50 border-amber-300 text-amber-700'
            : 'bg-white/80 border-gray-200 text-gray-500 hover:text-amber-700 hover:border-amber-300'}"
      >
        {#if spinning}
          <!-- Pause icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>
          </svg>
        {:else}
          <!-- Play icon -->
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
        {/if}
      </button>
    </div>

    <!-- Controls hint -->
    <p class="absolute bottom-2 right-3 text-xs text-gray-400 select-none pointer-events-none">
      Drag to rotate · Right-drag to pan · Scroll to zoom
    </p>
  {/if}
</div>
