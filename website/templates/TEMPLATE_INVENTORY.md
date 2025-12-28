# BlackRoad Template Inventory

**Last Updated:** December 28, 2024
**Total Templates:** 12 files (477KB total)

---

## Design System Templates

| File | Size | Purpose | Status |
|------|------|---------|--------|
| schematiq-design-system.html | 58KB | Complete design system showcase with golden ratio, typography, colors | ✅ Complete |
| schematiq-animation-system.html | 192B | Placeholder for animation system | ⚠️ Placeholder |

---

## Motion & Animation Templates

| File | Size | Purpose | Key Features |
|------|------|---------|--------------|
| **blackroad-animation.html** | 63KB | **WINNER** - Most comprehensive animation library | 14 sections, easing previews, star morph, timeline component, JetBrains Mono |
| blackroad-ultimate.html | 62KB | Ultimate motion system with animated logo | Golden ratio, 12 loaders, blinking eye logo, 15 particles, emoji marquee |
| blackroad-motion.html | 48KB | Motion design showcase | Mouse-tracking 3D tilts, Apple easing, golden ratio |

---

## Earth & World Visualizations

### 3D Globe Templates

| File | Size | Technology | Features |
|------|------|------------|----------|
| blackroad-earth.html | 52KB | Three.js + GLSL shaders | 46 global locations, network connections, 500 agent particles, procedural continents |
| earth-replica.html | 21KB | Three.js photorealistic | NASA Blue Marble 8K textures, bump maps, specular water, city lights |

### 2D Map Templates

| File | Size | Technology | Features |
|------|------|------------|----------|
| blackroad-earth-street.html | 32KB | MapLibre GL | 5 tile providers, globe projection, Nominatim search, z0-z22 zoom |

---

## Interactive World Templates

### Living Ecosystems

| File | Size | Type | Entities |
|------|------|------|----------|
| **blackroad-living-world.html** | 61KB | **MOST POLISHED** Living ecosystem | 730 entities: trees, flowers, houses, animals, agents, birds, fish, butterflies + weather |
| blackroad-living-planet.html | 48KB | Evolution simulation / god-mode game | 10 eras (Primordial → Space Age), build actions, environmental stats |

### Games

| File | Size | Genre | Systems |
|------|------|-------|---------|
| **blackroad-game.html** | 59KB | City-builder RPG hybrid | Quest system, inventory, XP/levels, resource economy, day/night cycle, weather |
| blackroad-3d-world.html | 31KB | Infinite road racer (Tron-style) | Procedural highway, WASD controls, wireframe buildings, animated logo |

---

## Recommended Usage

### For Documentation
**Primary:** `blackroad-animation.html` (most comprehensive, educational)
**Secondary:** `blackroad-ultimate.html` (ultimate logo showcase)

### For Landing Pages
**Earth Network:** `blackroad-earth.html` (shows global infrastructure)
**Interactive Demo:** `blackroad-living-world.html` (most polished, impressive)

### For Agent World (Lucidia.earth)
**Best Choice:** `blackroad-game.html` (quests, agents, progression system)
**Alternative:** `blackroad-living-planet.html` (evolution theme)

### For Tech Demos
**Motion Design:** `blackroad-motion.html` (Apple-level easing)
**3D Racing:** `blackroad-3d-world.html` (fast, fun)

---

## Technical Stack

All templates use:
- **Fonts:** SF Pro Display (Apple) or JetBrains Mono (code-focused)
- **3D:** Three.js r128 for WebGL rendering
- **Maps:** MapLibre GL for street maps
- **Colors:** BlackRoad brand palette (Hot Pink #FF1D6C, Amber #F5A623, Electric Blue #2979FF)
- **Design:** Golden ratio spacing (φ = 1.618)
- **Animations:** Apple-style cubic-bezier easing curves

---

## File Sizes Summary

```
Total: 477KB across 12 files

Largest:
- blackroad-animation.html (63KB) - Most comprehensive
- blackroad-ultimate.html (62KB) - Ultimate logo
- blackroad-living-world.html (61KB) - Polished ecosystem

Smallest:
- schematiq-animation-system.html (192B) - Placeholder only
- earth-replica.html (21KB) - Photorealistic Earth
- blackroad-3d-world.html (31KB) - Road racer game
```

---

## Next Steps

1. **Remove placeholder:** Delete or replace `schematiq-animation-system.html` (currently 192B placeholder)
2. **Create index:** Build unified landing page linking to all templates
3. **Deploy demos:** Host on Vercel/Cloudflare Pages for live previews
4. **Extract components:** Pull best animations into reusable React components

---

## Integration Notes

These templates are **standalone HTML files** with embedded CSS/JavaScript. To integrate into CarPool:

1. **Option A - iFrame:** Embed as iframes in Next.js pages
2. **Option B - Extract:** Convert animations to React components with Framer Motion
3. **Option C - Reference:** Use as design spec for rebuilding in Next.js + Tailwind

Recommended: **Option B** for production, **Option A** for rapid prototyping
