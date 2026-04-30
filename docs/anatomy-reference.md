# Saddle anatomy reference

This glossary defines the anatomical and saddle-making terms used throughout
the macros and README. Each term includes a cross-reference to the boolean
tools that target that region.

For coordinate-system context, see the [coordinate convention table](../README.md#coordinate-convention)
in the README.

---

## Tree regions

### Bars

The two longitudinal rails of the tree that lie along either side of the
horse's spine. The bars are the primary weight-bearing surface — they
distribute the rider's weight across a large area of the horse's back.

- **Rock** — the curvature of the bar along the horse's back (the
  front-to-back arch). A bar with more rock matches a horse with a
  rounder back profile. A flatter bar suits a straighter-backed horse.
- **Twist** — the angle of the bar relative to horizontal, which affects
  shoulder clearance at the front of the bar and hip clearance at the rear.
- **Spread** — the distance between the two bars, measured at the
  bar-to-bar width (gullet width). This is the primary horse-fit dimension.

Boolean tools: `BarCurveCutter_L` / `BarCurveCutter_R` (blue).

---

### Gullet channel

The arch-shaped channel running along the tree's underside, centred on
the horse's spine. The gullet must clear the spinous processes of the
withers and thoracic vertebrae at all times during riding.

**This is a safety-critical dimension.** A gullet that is too narrow
compresses the spine, causing pain, muscle atrophy, and permanent
skeletal damage.

- **Minimum safe width:** 70 mm (2.75") measured at the narrowest point,
  which is typically at or just behind the pommel.
- Width is controlled by the positions of `GulletCutter_L` and
  `GulletCutter_R`: shifting them toward X = 0 widens the channel;
  shifting them away from X = 0 narrows it.

Boolean tools: `GulletCutter_L` / `GulletCutter_R` (teal).

---

### Pommel (hornless trees)

The front arch of the tree on hornless trees (endurance, trail, some
cutting designs). The pommel bridges the two bars at the front and
defines the front of the gullet opening.

On hornless trees a flat or gently rounded **pommel cap** sits at the
top of the fork in place of a horn, and can be built up or given a
forward-tilted profile using the `PommelCapAdder`.

Boolean tools: `PommelCapAdder` (green).

---

### Swell / fork

The upward flare of the tree on either side of the horn (or on either
side of the pommel on hornless trees). The swell provides lateral
security — it prevents the rider's legs from sliding too far forward
and helps keep them in position through sudden movements.

- A **high swell** (as on the high-swell-tree) is wide and tall,
  providing maximum lateral security for ranch work and barrel racing.
- A **low swell** or **narrow fork** gives more freedom of leg movement
  for posting trot, two-point, and any discipline where the rider
  moves around frequently.

Boolean tools: `SwellCutter` (blue).

---

### Horn

The vertical projection rising from the swell/fork, present on western
saddles. The horn serves as a rope anchor for roping work (where the
rider wraps the rope around it — called a **dally**) and as a grab
point on steep terrain.

- **Horn height** — taller horns give more rope clearance for dally
  wrapping; shorter horns are lighter and less obstructive.
- **Neck diameter** — stouter necks withstand higher rope loads
  (roping trees); slimmer necks are lighter (trail trees).
- **Cap** — the flattened or rounded top of the horn. A wider cap
  gives more surface for the rope to wrap around.

Boolean tools: `HornCutter` (blue), `HornAdder` (green).

---

### Seat

The rider's contact surface, spanning from behind the swell/fork to
the front face of the cantle. The seat shape profoundly affects rider
comfort and position.

- A **deep, cupped seat** holds the rider forward and down into the
  saddle — maximum security but slower to exit.
- A **flat seat** allows quick dismount (roping standard) and easier
  posting trot.
- A **semi-flat seat** (endurance standard) allows posting trot and
  two-point while still providing contact for rough terrain.

The seat is shaped with a vertical cylinder whose radius controls the
dish depth: larger radius = flatter; smaller = deeper cup.

Boolean tools: `SeatScoopCutter` (orange cylinder).

---

### Cantle

The rear upswept portion of the tree, providing back support for the
rider. Cantle design varies considerably by discipline.

- **High cantle** — used in barrel racing and some ranch work; provides
  maximum rear support during hard stops and turns.
- **Low cantle** — used in endurance and trail riding; lighter and less
  restrictive to hip extension.
- **Solid cantle** — a continuous rear wall.
- **Split cantle** — a central vertical slot through the rear face,
  leaving two independent lateral wings. Reduces weight and allows
  the pelvis to tilt rearward for a more neutral, lower-back-friendly
  seated position on long rides.

Boolean tools: `CantleCutter` / `CantleAdder` (blue/green),
`CantleSplitCutter` (red — signature feature on split-cantle trees),
`CantleWingCutter_L` / `_R` (blue), `CantleBodyCutter` (blue).

---

### Rigging mortises

Shallow recesses (mortises) routed into the underside and sides of the
bars, into which the **rigging plates** (metal D-ring hardware) are set.
The cinch billets attach to the rigging rings, holding the saddle onto
the horse.

- **Single-rigged** — one cinch, one ring per side (most trail and
  endurance saddles).
- **Double-rigged** — front and rear cinch, two rings per side (roping
  and heavy ranch use). The front ring is the primary attachment;
  the rear (flank) ring prevents the saddle back from lifting during
  roping.
- **Rigging position** — how far forward the ring sits relative to the
  seat. Common positions: full (directly under the fork), 7/8 (slightly
  rearward), 3/4, and 5/8.

Boolean tools: `RiggingMortise_FL` / `_FR` / `_RL` / `_RR` (purple).

---

## Horse anatomy terms (relevant to saddle fit)

### Withers

The bony ridge at the base of the horse's neck, formed by the tallest
thoracic vertebral spinous processes. The front of the gullet channel
must clear the withers without touching them under any movement.
The two-finger test: run two fingers along the gullet channel with the
saddle on the horse — they should move freely at all points.

### Spinous processes

The vertical bony projections of the thoracic vertebrae running along
the horse's back. The gullet channel must not contact these at any point
along the full bar length.

### Scapula (shoulder blade)

The shoulder blade, which moves rearward as the horse extends its front
leg. The front of the bar must clear the rear edge of the scapula during
full stride extension. Bar twist adjustments (via `BarCurveCutter_L`)
affect how much shoulder clearance the tree provides.

### Back profile

The curvature of the horse's back from withers to croup:
- **Round back** — needs more bar rock (more arch) to follow the contour.
- **Flat back** — needs flatter bars.
- **Mutton-withered horse** — broad, flat withers; typically requires a
  wider gullet.
- **High-withered horse** — prominent withers; requires more gullet
  clearance at the front of the channel.

---

## Cross-reference: boolean tools by region

| Region | Tool | Colour | Operation |
|--------|------|--------|-----------|
| Cantle — main body | `CantleCutter` / `CantleAdder` | Blue / Green | Cut / Union |
| Cantle — split slot | `CantleSplitCutter` | Red | Cut (apply first) |
| Cantle — split wings | `CantleWingCutter_L` / `_R` | Blue | Cut |
| Cantle — lower zone | `CantleBodyCutter` | Blue | Cut |
| Seat | `SeatScoopCutter` | Orange | Cut |
| Bars — rock and twist | `BarCurveCutter_L` / `_R` | Blue | Cut |
| Gullet channel | `GulletCutter_L` / `_R` | Teal | Cut |
| Pommel cap (hornless) | `PommelCapAdder` | Green | Union |
| Swell / fork | `SwellCutter` | Blue | Cut |
| Horn | `HornCutter` / `HornAdder` | Blue / Green | Cut / Union |
| Rigging mortises | `RiggingMortise_FL/FR/RL/RR` | Purple | Cut |
