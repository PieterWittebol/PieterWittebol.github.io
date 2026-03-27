<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  let { src, mtl }: { src: string; mtl?: string } = $props();

  let container: HTMLDivElement;
  let loading = $state(true);
  let error = $state<string | null>(null);

  let animationId: number;
  let renderer: import('three').WebGLRenderer | null = null;

  onMount(async () => {
    try {
      const THREE = await import('three');
      const { OBJLoader } = await import('three/addons/loaders/OBJLoader.js');
      const { MTLLoader } = await import('three/addons/loaders/MTLLoader.js');
      const { OrbitControls } = await import('three/addons/controls/OrbitControls.js');

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
      camera.position.set(dist * 0.6, dist * 0.35, dist * 0.8);
      camera.near = dist / 100;
      camera.far = dist * 100;
      camera.lookAt(0, 0, 0);
      camera.updateProjectionMatrix();

      controls.maxDistance = dist * 6;
      controls.update();

      loading = false;

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

  <!-- Controls hint -->
  {#if !loading && !error}
    <p class="absolute bottom-2 right-3 text-xs text-gray-400 select-none pointer-events-none">
      Drag to rotate · Scroll to zoom
    </p>
  {/if}
</div>
