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
  var CLAW_HOME_X = null // set on first layout
  var CLAW_REST_TOP = 120
  var CLAW_GRAB_TOP = 318
  var CHUTE_X = 40

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
  function homeX () {
    if (CLAW_HOME_X === null) CLAW_HOME_X = Math.round(cabinet.clientWidth / 2)
    return CLAW_HOME_X
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

  /* ---------- machine sequence ---------- */
  async function play () {
    if (state.busy) return
    state.busy = true
    playBtn.disabled = true
    claw.classList.remove('sway')

    var loot = pit.querySelectorAll('.loot')
    var target = loot[Math.floor(Math.random() * loot.length)]
    var targetX = parseInt(target.style.left, 10) + 19 // center of loot

    // 1. move above target
    setClawY(CLAW_REST_TOP); setClawX(targetX)
    await wait(1150)

    // 2. descend
    setClawY(CLAW_GRAB_TOP)
    await wait(950)

    // 3. grab
    claw.classList.add('closed')
    await wait(500)
    target.classList.add('caught')

    // 4. lift with prize
    setClawY(CLAW_REST_TOP)
    target.style.transition = 'top .9s cubic-bezier(.5,0,.4,1), left 1.1s cubic-bezier(.45,.02,.3,1)'
    target.style.bottom = ''
    target.style.top = (CLAW_REST_TOP + 34) + 'px'
    target.style.left = (targetX - 19) + 'px'
    await wait(950)

    // 5. carry to chute
    setClawX(CHUTE_X)
    target.style.left = (CHUTE_X - 19) + 'px'
    await wait(1150)

    // 6. release
    claw.classList.remove('closed')
    target.style.transition = 'top .35s ease-in, opacity .3s .35s'
    target.style.top = (cabinet.clientHeight - 120) + 'px'
    target.style.opacity = '0'
    await wait(450)
    target.remove()

    // 7. chute lights
    chute.classList.add('lit'); catchLight.classList.add('on')
    await wait(600)

    // 8. reveal
    showReveal()

    // reset machine behind the overlay
    setClawX(homeX()); setClawY(CLAW_REST_TOP)
    setTimeout(function () {
      chute.classList.remove('lit'); catchLight.classList.remove('on')
      spawnLoot()
      claw.classList.add('sway')
      state.busy = false
      playBtn.disabled = false
    }, 1500)
  }

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
