/* Shared deterministic machine mechanics. Aiming selects wrapping, not contents. */
(function () {
  'use strict'
  var clamp = function (v, lo, hi) { return Math.max(lo, Math.min(hi, v)) }
  var ease = function (t) { return t * t * (3 - 2 * t) }
  var mix = function (a, b, t) { return a + (b - a) * t }
  var spots = Array.from({ length: 6 }, function (_, i) { return { x: (i % 3 - 1) * .67, z: i < 3 ? .35 : -.33 } })
  function create () {
    var s = { phase: 'idle', x: 0, z: 0, y: 3.08, close: 0, remaining: 30, selected: -1, prize: null, flash: false, drops: 0 }
    var input = { x: 0, z: 0 }, vx = 0, vz = 0, last = null, deadline = 0, start = 0, origin, callback, reduced = false
    var phases = ['descend', 'grab', 'lift', 'carry', 'drop', 'flash']
    var lengths = [1100, 650, 1100, 1400, 650, 550]
    function arm (options) {
      if (s.phase !== 'idle' && s.phase !== 'reveal') return false
      callback = options && options.onDrop
      reduced = matchMedia('(prefers-reduced-motion: reduce)').matches
      Object.assign(s, { phase: 'armed', x: 0, z: 0, y: 3.08, close: 0, remaining: 30, selected: -1, prize: null, flash: false, drops: 0, reason: null, travel: 0 })
      vx = vz = input.x = input.z = 0; last = performance.now(); deadline = last + 30000
      return true
    }
    function disarm () { s.phase = 'idle'; callback = null; input.x = input.z = vx = vz = 0 }
    function move (x, z) { input.x = clamp(x, -1, 1); input.z = clamp(z, -1, 1) }
    function drop (reason) {
      if (s.phase !== 'armed') return false
      s.phase = 'descend'; s.drops++; s.reason = reason || 'button'; start = performance.now()
      origin = { x: s.x, z: s.z }
      s.selected = spots.reduce(function (best, p, i) { return Math.hypot(p.x - s.x, p.z - s.z) < Math.hypot(spots[best].x - s.x, spots[best].z - s.z) ? i : best }, 0)
      s.prize = { x: spots[s.selected].x, y: 1.355, z: spots[s.selected].z, squash: 1 }
      input.x = input.z = vx = vz = 0
      return true
    }
    function step (now) {
      var dt = last === null ? 0 : clamp((now - last) / 1000, 0, .05); last = now
      if (s.phase === 'armed') {
        s.remaining = Math.max(0, Math.ceil((deadline - now) / 1000))
        if (now >= deadline) { drop('timeout'); return }
        var n = Math.max(1, Math.hypot(input.x, input.z)), follow = 1 - Math.exp(-22 * dt)
        vx += (input.x / n * .85 - vx) * follow; vz += (input.z / n * .85 - vz) * follow
        s.x = clamp(s.x + vx * dt, -.9, .9); s.z = clamp(s.z + vz * dt, -.5, .5)
        return
      }
      var index = phases.indexOf(s.phase)
      if (index < 0) return
      var duration = lengths[index] * (reduced ? .25 : 1), t = clamp((now - start) / duration, 0, 1), e = ease(t), p = s.prize
      if (s.phase === 'descend') s.y = mix(3.08, 2.605, e)
      if (s.phase === 'grab') { s.close = e; p.x = mix(spots[s.selected].x, s.x, e); p.z = mix(spots[s.selected].z, s.z, e) }
      if (s.phase === 'lift') { s.y = mix(2.605, 3.08, e); p.y = s.y - 1.25 }
      if (s.phase === 'carry') { s.travel = e; s.x = mix(origin.x, -.48, e); s.z = mix(origin.z, .58, e); p.x = s.x; p.z = s.z }
      if (s.phase === 'drop') { s.close = 1 - Math.min(1, t * 4); p.y = mix(1.83, .55, Math.min(1, t * t * 1.4)); p.squash = t > .85 ? .75 + .25 * (t - .85) / .15 : 1 }
      if (s.phase === 'flash') s.flash = true
      if (t === 1) {
        s.phase = phases[index + 1] || 'reveal'; start = now
        if (s.phase === 'reveal' && callback) { var done = callback; callback = null; done({ selected: s.selected, reason: s.reason }) }
      }
    }
    return { state: s, arm: arm, disarm: disarm, move: move, drop: drop, step: step }
  }
  window.ClawMotion = { create: create, spots: spots }
})()
