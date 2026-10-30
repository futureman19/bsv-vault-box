/* boxsv.com — claw machine flow. Zero dependencies.
   Demo v1: no payment; wallet connect via BRC-100 (window.CWI, Yours). */
(function () {
  'use strict'

  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  function wait (ms) { return new Promise(function (r) { setTimeout(r, reduced ? Math.min(ms * 0.3, 250) : ms) }) }
  function $(id) { return document.getElementById(id) }

  var cabinet = $('cabinet'), trolley = $('trolley'), cable = $('cable'), claw = $('claw'),
      pit = $('pit'), chute = $('chute'), catchLight = $('catchLight'),
      playBtn = $('playBtn'), chip = $('walletChip'),
      modal = $('walletModal'), werr = $('werr'), yoursState = $('yoursState'),
      reveal = $('reveal'), present = $('present'), burst = $('burst'),
      prizeCard = $('prizeCard'), prizeKey = $('prizeKey')

  var state = { mode: null, identity: null, busy: false }

  var LOOT_COLORS = ['#7c3aed', '#0ea5e9', '#dc2626', '#16a34a', '#db2777', '#ca8a04']
  var machine = null, fallbackMachine = window.ClawMotion.create()
  // A late WebGL mount observes an already-armed fallback game, never a new round.
  window.clawMotionHandle = fallbackMachine
  var wrap = document.querySelector('.machine-wrap'), joystick = $('joystick'), stick = $('stick'), dropBtn = $('dropBtn')
  var clock = document.createElement('div'); clock.className = 'game-clock'; clock.hidden = true; wrap.appendChild(clock)
  var keys = {}, pointer = null, axis = { x: 0, z: 0 }
  function clearInput () { keys = {}; pointer = null; axis.x = axis.z = 0; stick.style.transform = ''; if (machine) machine.move(0, 0) }

  function spawnLoot () {
    pit.innerHTML = ''
    var w = cabinet.clientWidth
    var spots = [0.10, 0.26, 0.42, 0.58, 0.74, 0.34]
    for (var i = 0; i < 6; i++) {
      var l = document.createElement('div')
      l.className = 'loot'
      l.style.left = Math.round(spots[i] * (w - 70)) + 'px'
      l.style.bottom = (8 + (i % 2) * 34) + 'px'
      l.style.background = LOOT_COLORS[i]
      l.style.setProperty('--tilt', ((i * 17) % 23) - 11 + 'deg')
      l.style.animationDelay = (i * 0.35) + 's'
      pit.appendChild(l)
    }
  }

  function setClawX (px) {
    trolley.style.left = px + 'px'
    cable.style.left = px + 'px'
    claw.style.left = px + 'px'
  }
  function setClawY (topPx) {
    claw.style.top = topPx + 'px'
    cable.style.height = Math.max(0, topPx - 60) + 'px'
  }

  /* ---------- wallet detection (BRC-100 / window.CWI) ---------- */
  function detectCWI () {
    var ok = typeof window.CWI !== 'undefined' && window.CWI !== null
    yoursState.textContent = ok ? 'detected ✓' : 'not installed — play demo instead'
    var go = $('optYours').querySelector('.go')
    if (go) go.textContent = ok ? 'CONNECT →' : 'GET WALLET'
    return ok
  }
  window.addEventListener('cwiReady', detectCWI)
  detectCWI(); setTimeout(detectCWI, 800); setTimeout(detectCWI, 2000)

  function setChip () {
    if (state.identity) {
      chip.textContent = 'connected: ' + state.identity.slice(0, 10) + '…' + state.identity.slice(-6)
    } else if (state.mode === 'demo') {
      chip.textContent = 'demo mode — no wallet connected'
    }
    chip.className = 'wallet-chip on'
  }

  /* ---------- modal ---------- */
  function openModal () { werr.textContent = ''; modal.className = 'overlay on' }
  function closeModal () { modal.className = 'overlay' }

  $('optCancel').addEventListener('click', closeModal)

  $('optDemo').addEventListener('click', function () {
    state.mode = 'demo'; state.identity = null
    setChip(); closeModal(); play()
  })

  $('optYours').addEventListener('click', async function () {
    werr.textContent = ''
    if (typeof window.CWI === 'undefined' || window.CWI === null) {
      window.open('https://yours.org', '_blank', 'noopener,noreferrer')
      return
    }
    try {
      await window.CWI.waitForAuthentication({})
      var id = await window.CWI.getPublicKey({ identityKey: true })
      if (!id || !id.publicKey) throw new Error('wallet returned no identity key')
      state.mode = 'wallet'; state.identity = id.publicKey
      setChip(); closeModal(); play()
    } catch (e) {
      werr.textContent = (e && e.message) ? e.message : 'wallet connection failed'
    }
  })

  /* Shared input and timing, independent of rendering. */
  function play () {
    if (state.busy) return
    machine = window.claw3dHandle && !window.claw3dHandle.disposed ? window.claw3dHandle : fallbackMachine
    clearInput(); spawnLoot(); cabinet.classList.add('interactive'); claw.classList.remove('sway', 'closed')
    state.busy = true; playBtn.hidden = true
    $('aimControls').hidden = $('aimHint').hidden = clock.hidden = false
    machine.arm({ onDrop: function () { clearInput(); state.busy = false; showReveal() } })
    joystick.disabled = dropBtn.disabled = false
    joystick.focus({ preventScroll: true })
  }
  function requestDrop (reason) { if (machine && machine.drop(reason)) clearInput() }
  dropBtn.addEventListener('click', function () { requestDrop('button') })
  document.addEventListener('keydown', function (e) {
    if (e.target instanceof Element && e.target.closest('#box-demo')) { clearInput(); return }
    if (!machine || machine.state.phase !== 'armed' || e.altKey || e.ctrlKey || e.metaKey) return
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) { e.preventDefault(); keys[e.key] = true }
    if (e.code === 'Space' || e.key === 'Enter') { e.preventDefault(); if (!e.repeat) requestDrop('keyboard') }
  })
  document.addEventListener('keyup', function (e) { delete keys[e.key] })
  window.addEventListener('blur', clearInput)
  document.addEventListener('visibilitychange', function () { if (document.hidden) clearInput() })
  function bindDrag (element) {
    element.addEventListener('pointerdown', function (e) {
      if (!machine || machine.state.phase !== 'armed' || pointer || e.button !== 0) return
      e.preventDefault(); element.setPointerCapture(e.pointerId)
      var r = element.getBoundingClientRect()
      pointer = { id: e.pointerId, x: element === joystick ? r.left + r.width / 2 : e.clientX, y: element === joystick ? r.top + r.height / 2 : e.clientY }
      drag(e)
    })
    function drag (e) {
      if (!pointer || pointer.id !== e.pointerId) return
      var x = (e.clientX - pointer.x) / 32, z = (e.clientY - pointer.y) / 32, n = Math.max(1, Math.hypot(x, z))
      axis.x = x / n; axis.z = z / n
      stick.style.transform = 'translate(' + axis.x * 24 + 'px,' + axis.z * 24 + 'px)'
    }
    element.addEventListener('pointermove', drag)
    ;['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function (name) { element.addEventListener(name, function (e) { if (pointer && pointer.id === e.pointerId) clearInput() }) })
  }
  bindDrag(joystick); bindDrag(wrap)
  function renderCSS (s) {
    var w = cabinet.clientWidth, px = function (x) { return w / 2 + x * (w - 90) / 1.8 }, ground = function (z) { return 285 + (z + .5) * 54 }
    var chuteOffset = (43 - px(-.48)) * (s.travel || 0)
    var clawTop = ground(s.z) - 34 - (s.y - 2.605) * 330
    setClawX(px(s.x) + chuteOffset); setClawY(clawTop)
    claw.classList.toggle('closed', s.close > .5)
    Array.from(pit.children).forEach(function (el, i) {
      var spot = window.ClawMotion.spots[i], selected = i === s.selected && s.prize
      var p = selected ? s.prize : { x: spot.x, z: spot.z, y: 1.355, squash: 1 }
      var top = ground(p.z) - (p.y - 1.355) * 330
      if (selected && ['drop', 'flash', 'reveal'].includes(s.phase)) {
        var fall = (1.83 - p.y) / 1.28
        top = clawTop + 34 + (cabinet.clientHeight - 58 - clawTop - 34) * fall
      }
      el.style.left = px(p.x) + (selected ? chuteOffset : 0) - 14 - 19 + 'px'; el.style.bottom = ''
      el.style.top = top - pit.offsetTop + 'px'
      el.style.zIndex = selected ? '6' : ''
      el.style.transform = 'scaleY(' + p.squash + ')'; el.style.opacity = s.phase === 'reveal' && i === s.selected ? '0' : '1'
    })
    chute.classList.toggle('lit', s.flash); catchLight.classList.toggle('on', s.flash)
  }
  function tick (now) {
    if (machine) {
      // A lost WebGL context keeps the same mechanics; only the renderer changes.
      machine.move(axis.x + (keys.ArrowRight ? 1 : 0) - (keys.ArrowLeft ? 1 : 0), axis.z + (keys.ArrowDown ? 1 : 0) - (keys.ArrowUp ? 1 : 0))
      machine.step(now)
      var s = machine.state, armed = s.phase === 'armed'
      dropBtn.disabled = joystick.disabled = !armed
      clock.textContent = armed ? 'TIME ' + String(s.remaining).padStart(2, '0') : s.phase === 'reveal' ? 'YOUR BOX' : 'RETRIEVING'
      if (!wrap.classList.contains('claw3d-ready')) renderCSS(s)
      wrap.dataset.phase = s.phase
    }
    requestAnimationFrame(tick)
  }
  window.clawGame = { get state () { return machine ? Object.assign({}, machine.state) : { phase: 'idle' } } }
  requestAnimationFrame(tick)

  /* ---------- prize reveal ---------- */
  async function showReveal () {
    present.classList.remove('open', 'shake')
    burst.classList.remove('on')
    prizeCard.classList.remove('on')
    reveal.className = 'reveal on'

    await wait(400)
    present.classList.add('shake')
    await wait(reduced ? 400 : 1900)

    present.classList.add('open')
    burst.classList.add('on')

    if (state.identity) {
      prizeKey.textContent = 'Minted-to key (demo): ' + state.identity.slice(0, 14) + '…' + state.identity.slice(-8) +
        ' — at launch this is a real on-chain VAULT box only this key can open.'
    } else {
      prizeKey.textContent = 'Demo box. At launch it is minted to your connected wallet key — only that key can open it.'
    }
    prizeCard.classList.add('on')
  }

  $('againBtn').addEventListener('click', function () {
    reveal.className = 'reveal'
    play() // mode already chosen; straight back into the machine
  })

  /* ---------- entry ---------- */
  playBtn.addEventListener('click', function () {
    if (state.busy) return
    if (state.mode) { play(); return } // wallet/demo already chosen this session
    openModal()
  })

  spawnLoot()
})()
