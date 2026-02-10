# app.py
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PCSE 3D Prototype", layout="wide")
st.title("PCSE + Streamlit + Three.js (3D Interactive Prototype)")

# --- Simple controllable state (replace with PCSE later) ---
if "state" not in st.session_state:
    st.session_state.state = {"dvs": 0.10, "lai": 0.50, "tagp": 100.0}

with st.sidebar:
    st.header("Controls")
    irrigation = st.slider("Irrigation today (mm)", 0, 30, 5)
    step_day = st.button("Simulate 1 day", type="primary")
    st.caption("Now this is a toy update. Next step: replace with a real PCSE daily step.")

if step_day:
    # Toy growth update (deterministic and stable)
    st.session_state.state["dvs"] = min(2.0, st.session_state.state["dvs"] + 0.02)
    st.session_state.state["lai"] = min(6.0, st.session_state.state["lai"] + 0.10 + irrigation * 0.01)
    st.session_state.state["tagp"] = st.session_state.state["tagp"] + 50.0 + irrigation * 2.0

state_json = json.dumps(st.session_state.state)

# --- Three.js scene (ES Modules, OrbitControls works) ---
html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <style>
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #111;
    }}
    #info {{
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(0,0,0,0.65);
      color: #fff;
      padding: 10px 12px;
      font-family: sans-serif;
      border-radius: 8px;
      z-index: 10;
      line-height: 1.35;
      white-space: pre-wrap;
      max-width: 60%;
    }}
  </style>
</head>
<body>
  <div id="info">Loading Three.js...</div>

  <script type="module">
    const info = document.getElementById("info");

    // Always show runtime errors inside the iframe
    window.addEventListener("error", (e) => {{
      info.textContent = "JS Error:\\n" + (e.message || e.error || e);
    }});
    window.addEventListener("unhandledrejection", (e) => {{
      info.textContent = "Promise Rejection:\\n" + (e.reason?.message || e.reason || e);
    }});

    try {{
      // Use a different CDN that often works better in sandboxed iframes
      import * as THREE from "https://esm.sh/three@0.160.0";
      import {{ OrbitControls }} from "https://esm.sh/three@0.160.0/examples/jsm/controls/OrbitControls.js";

      const state = {state_json};

      info.textContent =
        "DVS: " + state.dvs.toFixed(2) + "\\n" +
        "LAI: " + state.lai.toFixed(2) + "\\n" +
        "TAGP: " + state.tagp.toFixed(0) + "\\n\\n" +
        "Drag to orbit, scroll to zoom.";

      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x9fbad0);

      const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 100);
      camera.position.set(4, 4, 6);

      const renderer = new THREE.WebGLRenderer({{ antialias: true }});
      renderer.setPixelRatio(window.devicePixelRatio || 1);
      document.body.appendChild(renderer.domElement);

      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;

      const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
      dirLight.position.set(5, 10, 5);
      scene.add(dirLight);
      scene.add(new THREE.AmbientLight(0xffffff, 0.45));

      const ground = new THREE.Mesh(
        new THREE.PlaneGeometry(20, 20),
        new THREE.MeshStandardMaterial({{ color: 0x6b8e23 }})
      );
      ground.rotation.x = -Math.PI / 2;
      scene.add(ground);

      const tile = new THREE.Mesh(
        new THREE.BoxGeometry(1.2, 0.1, 1.2),
        new THREE.MeshStandardMaterial({{ color: 0x8b6f47 }})
      );
      tile.position.set(0, 0.05, 0);
      scene.add(tile);

      const crop = new THREE.Mesh(
        new THREE.CylinderGeometry(0.15, 0.22, 1.0, 16),
        new THREE.MeshStandardMaterial({{ color: 0x1f7a1f }})
      );
      crop.position.set(0, 0.55, 0);
      scene.add(crop);

      const h = Math.max(0.2, Math.min(3.0, state.lai));
      crop.scale.y = h;

      function resize() {{
        const w = document.documentElement.clientWidth;
        const h = document.documentElement.clientHeight;
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      }}
      window.addEventListener("resize", resize);
      resize();

      function animate() {{
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
      }}
      animate();
    }} catch (err) {{
      info.textContent = "Failed to load Three.js modules.\\n" + (err?.message || err);
    }}
  </script>
</body>
</html>
"""


components.html(html, height=720, scrolling=False)
