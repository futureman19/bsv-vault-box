--- Guide for dialog ---
# Dialog

## Overview

Use the native `<dialog>` element for modal and non-modal dialogs. It provides the accessibility semantics, focus handling, top-layer rendering and `Esc` handling that custom overlays have to rebuild by hand.

## Choose the overlay type

Pick the first rule that matches. If unsure, use Rule 1.

### Rule 1: The overlay interrupts the user and blocks the page (default)

Use for confirmations, forms, sign-in, destructive actions, and any "modal", "dialog", "lightbox" or "popup" request that does not say otherwise.

Use `<dialog>` opened as a modal, declaratively with `command="show-modal"` (see `declarative-dialog-popover-control` (via `npx -y modern-web-guidance@latest retrieve "declarative-dialog-popover-control"`)) or from script with `showModal()`.

```html
<button type="button" command="show-modal" commandfor="confirm">Delete</button>

<!-- MANDATORY: no role="dialog" or aria-modal; the native modal already provides them -->
<dialog id="confirm" aria-labelledby="confirm-title">
  <h2 id="confirm-title">Delete this item?</h2>
  <form method="dialog">
    <button value="cancel" autofocus>Cancel</button>
    <button value="delete">Delete</button>
  </form>
</dialog>
```

The browser provides: inert page, focus containment, top layer, `::backdrop`, `Esc` and back-gesture dismissal, and focus return to the invoker.

- **DON'T** add `role="dialog"`, `aria-modal`, a focus trap, `inert` toggling or an `Esc` handler.
- **DON'T** open it with `show()` or the `open` attribute.
- **DO** stop the page scrolling behind it with the CSS below. See `prevent-page-scroll-under-modal-dialog` (via `npx -y modern-web-guidance@latest retrieve "prevent-page-scroll-under-modal-dialog"`) for the details.
- **DON'T** lock scrolling with `overflow: hidden` or `position: fixed` on `html` or `body`.

```css
/* MANDATORY (both rules): without them, scrolling over the backdrop or inside the dialog scrolls the page behind it */
dialog:modal {
  overscroll-behavior: contain; /* stops scroll gestures in the dialog chaining to the page */
}
dialog::backdrop {
  overflow: hidden; /* ::backdrop is not a scroll container by default, so it would ignore overscroll-behavior */
  overscroll-behavior: contain;
}
```

Not for menus or tooltips: see Rule 3.

### Rule 2: The user keeps working in the page while the panel is open

Use for find bars, inspectors, palettes and compose panes that are still dialogs semantically.

Use `<dialog popover>` for a top-layer panel with popover dismissal (`auto` light-dismisses, `manual` does not). Use `dialog.show()` only when the panel must not be in the top layer.

```html
<button type="button" popovertarget="find">Find</button>
<dialog id="find" popover="manual" aria-labelledby="find-title">
  <h2 id="find-title">Find</h2>
  <input type="search" aria-label="Search">
  <button type="button" popovertarget="find" popovertargetaction="hide">Close</button>
</dialog>
```

The page stays interactive and is not made inert.

- **DO** include a visible close button.
- **DON'T** use `showModal()`, which blocks the page.

Not for blocking confirmations: see Rule 1.

### Rule 3: The overlay is not a dialog

Use for menus, dropdowns, tooltips, hovercards and toasts.

Use a semantic element with the `popover` attribute, not `<dialog>`.

```html
<button type="button" popovertarget="menu">Actions</button>
<ul id="menu" popover>
  <li><a href="/rename">Rename</a></li>
</ul>
```

## Choose how it can be dismissed

The default depends on how the dialog is opened. If `closedby` is absent or invalid, `showModal()` behaves as `closerequest` and any other way of opening behaves as `none`.

- **Esc and back gesture only (modal default):** set nothing, or `closedby="closerequest"`.
- **Also click outside to close:** use `closedby="any"`.
- **Only the developer closes it (for example a form with unsaved changes):** use `closedby="none"` and add a confirmation path. See Closing below.

## Guidelines

### Accessible name and initial focus

- **DO** name every dialog with `aria-labelledby` pointing at its heading, or `aria-label` when there is no visible title.
- **DO** put `autofocus` on the primary control or first field.
- **DO** put `autofocus` on the safe action (such as Cancel or Keep) in a destructive confirmation.
- **DON'T** write code to return focus on close. The browser returns it to the invoker.

### Opening

- **DO** open declaratively with `command="show-modal"` and `commandfor` on a `<button>`. See `declarative-dialog-popover-control` (via `npx -y modern-web-guidance@latest retrieve "declarative-dialog-popover-control"`).
- **DO** use `dialog.showModal()` when opening from script.

### Closing

- **DO** close with `<form method="dialog">` buttons or `command="close"`.
- **DO** choose `closedby` deliberately: `any` (light dismiss and `Esc`), `closerequest` (`Esc` only, the modal default) or `none` (developer-controlled close only).
- **DO** use `command="request-close"` or `requestClose()` for Cancel buttons that must honor unsaved-changes logic. They fire `cancel` first and ignore `closedby`.
- **DO** treat `closedby` as progressive enhancement. `Esc` and the mobile back gesture already close modals without it.

### Hooking into close

- **DO** read `dialog.returnValue` in a `close` listener to learn which button was used, then reset it with `dialog.returnValue = ''`. `Esc` and other close requests set no value, and browsers differ on whether they clear the previous one, so without the reset a stale value can leak. Treat `''` as "dismissed without choosing".
- **DO** use `cancel` to intercept `Esc` and `request-close`, but do not rely on `preventDefault()` for repeated `Esc` presses without user activation.
- **DO** use `closedby="none"` with an explicit confirmation step for dirty forms.
- **DO** tell the user why the dialog stayed open when `cancel` is prevented: show a visible message and reference it with `aria-describedby` from the control that receives focus (such as Discard), so a screen reader reads it when focus moves. Without it, focus moving to a new button announces only that button's name.
- **DON'T** let the confirmation move controls under the pointer. Reserve the message's space (hide it with `visibility`, not `display` or `hidden`) and add the destructive button where existing buttons do not move (for example first in a right-aligned row), so a second click at the same spot cannot discard the user's changes.

### Non-modal dialogs

- **DO** use `<dialog popover>` (`auto` or `manual`) for a top-layer panel, and `dialog.show()` when you do not want the top layer.
- **DO** include a visible close button in every non-modal dialog.

### Backdrop and styling

- **DO** style `::backdrop` and use `dialog:modal` to target modal-only styles.
- **DO** leave animation to `animate-to-from-top-layer` (via `npx -y modern-web-guidance@latest retrieve "animate-to-from-top-layer"`), dragging to `drag` (via `npx -y modern-web-guidance@latest retrieve "drag"`), and reparenting to `persistent-top-layer-ui` (via `npx -y modern-web-guidance@latest retrieve "persistent-top-layer-ui"`).
- **DON'T** set `display` on `dialog` unconditionally. It overrides the closed state. Scope it with `dialog[open]`.

### Accessibility

- **DON'T** add `role="dialog"`, `aria-modal`, a manual focus trap or `inert` toggling to a native modal.
- **DO** use a native `<button>` with an accessible name for close controls.
- **DO** use one consistent heading level for dialog titles.

## Fallback strategies

### `closedby` (`dialog-closedby`)

Browser support for <dialog closedby>: Limited availability.
Supported by: Chrome 134 (Mar 2025), Edge 134 (Mar 2025), and Firefox 141 (Jul 2025).
Unsupported in: Safari.

Without `closedby`, a modal still closes with `Esc` and the back gesture; only click-outside is lost, so this is graceful degradation. `closedby="none"` is ignored the same way: `Esc` fires `cancel` and then closes the dialog. Keep the unsaved-changes guard in a `cancel` handler, not in `closedby="none"` alone, so it also protects where `closedby` is missing. If your Baseline target requires light dismiss, add this where `closedby` is missing:

```js
if (!('closedBy' in HTMLDialogElement.prototype)) {
  // Test the pointer position, not event.target: the <dialog> is also the target for its own
  // padding and the gaps between its children, so a target check would close on those clicks
  const outside = (e, dialog) => {
    const r = dialog.getBoundingClientRect();
    return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
  };
  for (const dialog of document.querySelectorAll('dialog[closedby="any"]')) {
    let pressedOutside = false;
    dialog.addEventListener('pointerdown', (e) => { pressedOutside = outside(e, dialog); });
    // Require the press and the release outside, so a text-selection drag that ends on the backdrop does not dismiss
    dialog.addEventListener('pointerup', (e) => { if (pressedOutside && outside(e, dialog)) dialog.close(); });
  }
}
```

### `overscroll-behavior`

Browser support for overscroll-behavior: Limited availability.
Supported by: Chrome 144 (Jan 2026), Edge 144 (Jan 2026), and Firefox 150 (Apr 2026).
Unsupported in: Safari.

Treat scroll containment as progressive enhancement. Do not feature-detect it: `@supports` reports the property as supported even where non-scrollable containers ignore it. Where it is not enforced, the dialog still contains scroll whenever its own content overflows, and `showModal()` still makes the page inert. Do not fall back to `overflow: hidden` or `position: fixed` on `html` or `body`, which removes the root scrollbar and shifts the layout.

### Invoker Commands (`command` / `commandfor`)

Baseline status for Invoker commands: Newly available. It's been Baseline since 2025-12-12.
Supported by: Chrome 135 (Apr 2025), Edge 135 (Apr 2025), Firefox 144 (Oct 2025), and Safari 26.2 (Dec 2025).

If your Baseline target does not include Invoker Commands, keep the same markup and conditionally load the polyfill (the same experience, as progressive enhancement). Detect on the interface and never load it unconditionally:

```js
// MANDATORY: feature detect on HTMLButtonElement.prototype and load only when native support is missing
if (!('commandForElement' in HTMLButtonElement.prototype)) {
  import('invokers-polyfill'); // npm install invokers-polyfill
}
```

Only Rules 2 and 3 use Popover.

### Fallbacks & browser support for Popover

Baseline status for Popover: Newly available. It's been Baseline since 2025-01-27.
Supported by: Chrome 116 (Aug 2023), Edge 116 (Aug 2023), Firefox 125 (Apr 2024), Safari 17 (Sep 2023), and Safari iOS 18.3 (Jan 2025).

The Popover API is mostly **progressive enhancement**, but its defining behaviors — top-layer promotion, light-dismiss, and `popovertarget` invocation — have no CSS-only equivalent. Older browsers need a polyfill, or a manual fallback if you would rather not ship one.

**Polyfill:** To support the `popover` attribute in older browsers, conditionally load [`@oddbird/popover-polyfill`](https://github.com/oddbird/popover-polyfill). **MANDATORY:** Feature detect by checking for the `popover` property on `HTMLElement.prototype`, and load the polyfill **only** when native support is missing — do NOT load it unconditionally.

With a bundler or import map:

```js
// MANDATORY: Feature detect 'popover' on HTMLElement.prototype.
if (!Object.hasOwn(HTMLElement.prototype, "popover")) {
  import("@oddbird/popover-polyfill");
}
```

If not using a package manager, import from a CDN, e.g. `"https://unpkg.com/@oddbird/popover-polyfill@latest/dist/popover.min.js"`.

Caveats when using the polyfill:
- Do NOT use the `popover` IDL attribute for any code that may run before the polyfill is fully loaded. It will not be mirrored as an attribute, the popover will not be picked up by the polyfill, and the property will be shadowing the accessor the polyfill adds forever. Use `setAttribute()`/`removeAttribute()` instead.
- **Styling caveat:** The polyfill cannot define the real `:popover-open` pseudo-class, so it applies a `.\:popover-open` class instead. **MANDATORY:** Combine the two with `:is()` or `:where()`, otherwise browsers that lack `:popover-open` discard the entire rule:

```css
[popover]:is(:popover-open, .\:popover-open) {
  display: block;
}
```


--- Guide for js ---
# JavaScript

Modern JavaScript and Web platform runtimes provide built-in primitives for deep cloning, non-mutating collection transforms, asynchronous coordination, query-string parsing, binary text encoding, and DOM mutation. Replacing legacy userland workarounds (`JSON.parse(JSON.stringify(...))`, `[...arr].sort()`, `.reduce()` bucket accumulators, manual `AbortController` timers, and `innerHTML = ''` clearing loops) eliminates subtle data corruption, prototype pollution, call-stack overflows, and unnecessary parser overhead.

## Table of Contents

- [Use-Case Guide Matrix](#use-case-guide-matrix)

1. [Immutable Data, Deep Cloning, and Grouping](#1-immutable-data-deep-cloning-and-grouping)
   - [Deep Cloning with `structuredClone()`](#deep-cloning-with-structuredclone)
   - [Non-Mutating Array Copies and Reverse Search](#non-mutating-array-copies-and-reverse-search)
   - [Grouping Iterable Collections (`Object.groupBy()` and `Map.groupBy()`)](#grouping-iterable-collections-objectgroupby-and-mapgroupby)
2. [Asynchronous Coordination, Cancellation, and Error Chaining](#2-asynchronous-coordination-cancellation-and-error-chaining)
   - [Externalized Promise Settlement (`Promise.withResolvers()`)](#externalized-promise-settlement-promisewithresolvers)
   - [Declarative Timeout and Composite Cancellation (`AbortSignal.timeout()` and `AbortSignal.any()`)](#declarative-timeout-and-composite-cancellation-abortsignaltimeout-and-abortsignalany)
   - [Chaining Error Causes with Error Cause Options](#chaining-error-causes-with-error-cause-options)
3. [URL Query Manipulation and Binary Text Encoding](#3-url-query-manipulation-and-binary-text-encoding)
   - [Parsing and Constructing Query Strings (`URLSearchParams`)](#parsing-and-constructing-query-strings-urlsearchparams)
   - [Binary UTF-8 Text Decoding and Encoding (`TextDecoder` and `TextEncoder`)](#binary-utf-8-text-decoding-and-encoding-textdecoder-and-textencoder)
4. [DOM Child Replacement and Custom Events](#4-dom-child-replacement-and-custom-events)
   - [Atomic Child Replacement and Clearing (`Element.prototype.replaceChildren()`)](#atomic-child-replacement-and-clearing-elementprototypereplacechildren)
   - [Constructing Standard and Custom Events (`new Event()` and `new CustomEvent()`)](#constructing-standard-and-custom-events-new-event-and-new-customevent)

## Use-Case Guide Matrix

For specialized temporal, scheduling, and security workflows, consult the dedicated guides below:

| Workflow / Domain | Guide |
| :--- | :--- |
| Calculating exact calendar durations (`years`, `months`, `days`) between dates or events | `calculate-event-differentials` (via `npx -y modern-web-guidance@latest retrieve "calculate-event-differentials"`) |
| Representing calendar dates (`PlainDate`), wall-clock times (`PlainTime`), or recurring rules without time-zone shift bugs | `capture-location-agnostic-data` (via `npx -y modern-web-guidance@latest retrieve "capture-location-agnostic-data"`) |
| Converting instants across IANA time zones (`ZonedDateTime`) with DST disambiguation | `coordinate-global-events` (via `npx -y modern-web-guidance@latest retrieve "coordinate-global-events"`) |
| Sorting and comparing nanosecond-precision timestamps (`Temporal.Instant.compare`) | `sort-high-precision-timestamps` (via `npx -y modern-web-guidance@latest retrieve "sort-high-precision-timestamps"`) |
| Projecting dates into non-Gregorian calendar systems (`hebrew`, `islamic-civil`, `japanese`, `chinese`) | `support-global-calendar-systems` (via `npx -y modern-web-guidance@latest retrieve "support-global-calendar-systems"`) |
| Sanitizing untrusted HTML strings before DOM insertion | `sanitize-untrusted-html` (via `npx -y modern-web-guidance@latest retrieve "sanitize-untrusted-html"`) |

---

## 1. Immutable Data, Deep Cloning, and Grouping

### Deep Cloning with `structuredClone()`

Use `structuredClone(value)` to deep-copy nested objects, arrays, and built-in platform types without round-tripping through a JSON string.

#### Guidelines

- **DO** use `structuredClone(value)` instead of `JSON.parse(JSON.stringify(value))` or recursive cloning utilities (`_.cloneDeep`) when copying structured state in memory.
- **DO** rely on `structuredClone()` to preserve cyclic references, shared object references (DAGs), `Date` instances, `RegExp`, `Map`, `Set`, `ArrayBuffer`, `TypedArray`, `DataView`, `BigInt`, `Error` instances, `undefined` property values, `NaN`, `Infinity`, `-0`, and sparse array holes.
- **DO** pass a `{ transfer: [arrayBuffer] }` options object when moving ownership of `ArrayBuffer` or `MessagePort` instances without copying underlying bytes.
- **DO NOT** replace `JSON.parse(JSON.stringify(value))` with `structuredClone(value)` when callers depend on **JSON wire normalization** or transforms:
  - Converting `Date` instances to ISO-8601 strings (`Date.prototype.toJSON()`), or running `JSON.stringify` `replacer` allowlists/redactions or `JSON.parse` `reviver` transforms.
  - Invoking custom `.toJSON()` methods on objects (`structuredClone()` ignores inherited or non-enumerable `.toJSON()` methods and throws `DataCloneError` if an object has own enumerable function properties such as `.toJSON` or imported library singleton/options methods).
  - Stripping keys whose values are `undefined`, Functions, or `Symbol`s, converting `NaN`, `Infinity`, `-Infinity`, and sparse array holes to `null` (and `-0` to `+0`), or intentionally breaking shared DAG references (`a.x !== a.y` so callers can mutate aliased branches independently).
- **DO NOT** pass non-cloneable values to `structuredClone()`. It throws a `DOMException` (`DataCloneError`) on:
  - Functions or imported library singletons/options objects with own enumerable methods (whereas `JSON.stringify` silently omits function properties on objects or turns array elements into `null`).
  - `Symbol` values or `Symbol`-keyed properties (which `JSON.stringify` silently ignores).
  - DOM nodes (`Element`, `Document`, `Node`), live browser/WebIDL objects (`window.location`, `localStorage`, `element.dataset` (`DOMStringMap`), `getComputedStyle(el)` (`CSSStyleDeclaration`), DOM `Event`, `URLSearchParams`, `FormData`, `Headers`—whereas serializable geometry objects like `DOMRect` do clone), `Promise`, `WeakMap`, `WeakSet`, or any `Proxy` instance (both generic `Proxy` wrappers and reactive stores such as Vue `reactive()` or MobX observables).
- **DO NOT** expect `structuredClone()` to preserve custom class prototypes, class methods, non-enumerable properties, property descriptors, or `#private` fields. Like `JSON.parse(JSON.stringify(...))`, `structuredClone()` strips custom prototype chains to `Object.prototype`, drops non-enumerable properties and `#private` fields, and evaluates enumerable getters once into plain data properties.

> [!NOTE]
> `structuredClone` is a host-provided global rather than an intrinsic ECMAScript language global. In isolated Node.js `vm.createContext({})` sandboxes or legacy custom test environments that do not expose host globals on the context object, `structuredClone` may be `undefined` unless explicitly injected into the context.

#### Code Example

```js
const original = {
  id: 'session-42',
  createdAt: new Date('2026-03-15T12:00:00Z'),
  tags: new Set(['admin', 'audit']),
  metrics: new Float64Array([0.98, 0.99]),
  optionalNote: undefined,
};
original.self = original; // Circular reference

const copy = structuredClone(original);

console.assert(copy !== original);
console.assert(copy.createdAt instanceof Date);
console.assert(copy.tags instanceof Set && copy.tags !== original.tags);
console.assert(copy.self === copy);
console.assert('optionalNote' in copy && copy.optionalNote === undefined);
```

---

### Non-Mutating Array Copies and Reverse Search

Use the copying array methods (`.toSorted()`, `.toReversed()`, `.toSpliced()`, `.with()`) and reverse search methods (`.findLast()`, `.findLastIndex()`) to transform or query arrays without mutating the source reference or allocating intermediate shallow clones.

#### Guidelines

- **DO** use `array.toSorted(compareFn)` instead of `[...array].sort(compareFn)`, `array.slice().sort(compareFn)`, or `Array.from(array).sort(compareFn)`.
- **DO** use `array.toReversed()` instead of `[...array].reverse()` or `array.slice().reverse()`.
- **DO** use `array.toSpliced(start, deleteCount, ...items)` for immutable insertions, deletions, and replacements instead of cloning and calling `.splice()`.
- **DO** use `array.with(index, value)` (which supports negative indices) for single-index immutable updates instead of copying and assigning `clone[index] = value`.
- **DO** use `array.findLast(predicate)` and `array.findLastIndex(predicate)` instead of `[...array].reverse().find(predicate)` or reversing indices manually.
- **DO NOT** refactor `arr.slice().reverse().findIndex(fn)` without auditing multi-argument callbacks and `-1` miss math: `findLast()`/`findLastIndex()` pass the **original** forward `index` to `(item, index, arr)` rather than the reversed-copy index, and `arr.length - 1 - (-1) === arr.length` evaluates to an out-of-bounds index on a miss whereas `findLastIndex()` returns `-1`.
- **DO NOT** drop `[...iterable]` / `Array.from()` conversion when the receiver is a `string`, non-Array iterable, or array-like object (`Set`, `Map.keys()`, `Map.values()`, generator, `NodeList`, `HTMLCollection`, or `arguments`). Calling `.toSorted()` or `.toReversed()` directly on a `string`, `Set`, or `NodeList` throws a `TypeError`; convert first and chain the mutating method (`[...set].sort(compareFn)`, `[...nodeList].reverse()`, or `Array.from(str).toReversed().join('')`) rather than allocating redundant copies.
- **DO NOT** replace `[...typedArray].sort()` with `typedArray.toSorted()` unless numeric ordering and a `TypedArray` return type are intended:
  - `Array.prototype.sort()` / `.toSorted()` converts elements to UTF-16 strings by default (`[10, 2].toSorted()` yields `[10, 2]`), whereas `%TypedArray%.prototype.toSorted()` sorts numerically (`new Uint8Array([10, 2]).toSorted()` yields `Uint8Array [2, 10]`) and returns a `TypedArray` instead of a plain `Array`.
  - `%TypedArray%.prototype` does **not** implement `.toSpliced()` (because TypedArrays have fixed byte lengths).
- **DO NOT** use `.toSorted()` or `.toReversed()` when code intentionally relies on sparse array hole preservation (`!(i in arr)`). Copying methods always produce dense arrays where sparse holes become `undefined` elements (`0 in [, 1].toReversed()` is `true`), whereas `Array.prototype.slice()`, `.sort()`, and `.reverse()` preserve empty slots.

#### Code Example

```js
const tasks = [
  { id: 1, priority: 2, status: 'done' },
  { id: 2, priority: 5, status: 'open' },
  { id: 3, priority: 1, status: 'done' },
];

// Immutable sort and single-element update without mutating `tasks`
const byPriority = tasks.toSorted((a, b) => b.priority - a.priority);
const reopened = tasks.with(-1, { ...tasks.at(-1), status: 'open' });

// Reverse search without allocating a reversed copy
const lastCompleted = tasks.findLast((task) => task.status === 'done');
const lastCompletedIndex = tasks.findLastIndex((task) => task.status === 'done');
```

---

### Grouping Iterable Collections (`Object.groupBy()` and `Map.groupBy()`)

Use `Object.groupBy(items, callbackFn)` and `Map.groupBy(items, callbackFn)` to partition any iterable into array buckets in a single step.

#### Guidelines

- **DO** use `Object.groupBy(items, (item, index) => key)` instead of `items.reduce((acc, item) => { (acc[key] ??= []).push(item); return acc; }, {})` when grouping into string or symbol property keys and each bucket holds unmodified original elements (`Object.groupBy()` uses `CreateDataProperty`, so keys like `'constructor'` or `'toString'` never collide with `Object.prototype`).
- **DO** use `Map.groupBy(items, (item, index) => key)` when grouping by object references, class instances, or primitive keys whose non-string types (`number`, `boolean`, `undefined`, `BigInt`) must be preserved without `ToPropertyKey` coercion (`Object.groupBy()` coerces keys with `String(key)`, turning objects into `'[object Object]'`).
- **DO** use `Object.hasOwn(groups, key)` or nullish coalescing (`groups[key] ?? []`) when reading buckets from `Object.groupBy()`.
- **DO NOT** call `Object.prototype` methods (`groups.hasOwnProperty(key)`) or rely on `grouped instanceof Object` on `Object.groupBy()` results: it returns a `null`-prototype object (`Object.getPrototypeOf(grouped) === null`, `grouped instanceof Object === false`), so `groups.hasOwnProperty` is `undefined` and calling it throws a `TypeError`.
- **DO NOT** replace `.reduce()` accumulators that simultaneously transform elements (`acc[key].push(item.id)`), compute scalar aggregations (counts, sums, min/max), or pre-seed empty keys that have zero matching items (`Object.groupBy()` only creates keys that appear at least once in `items`).

#### Code Example

```js
const deliveries = [
  { id: 'd1', region: 'eu-west', weightKg: 4.2 },
  { id: 'd2', region: 'us-east', weightKg: 1.1 },
  { id: 'd3', region: 'eu-west', weightKg: 8.5 },
];

// String-keyed null-prototype dictionary of arrays
const byRegion = Object.groupBy(deliveries, (item) => item.region);
const euShipments = byRegion['eu-west'] ?? [];

// Non-string or object keys preserved in a Map
const heavyKey = { tier: 'heavy' };
const standardKey = { tier: 'standard' };
const byTier = Map.groupBy(deliveries, (item) =>
  item.weightKg >= 5 ? heavyKey : standardKey,
);
```

---

## 2. Asynchronous Coordination, Cancellation, and Error Chaining

### Externalized Promise Settlement (`Promise.withResolvers()`)

Use `Promise.withResolvers()` when a promise's `resolve` and `reject` callbacks must be stored or invoked outside the `new Promise` executor scope (such as in event listeners, worker message handlers, stream queues, or cancellation tokens).

#### Guidelines

- **DO** use `const { promise, resolve, reject } = Promise.withResolvers()` instead of declaring mutable outer variables (`let resolve, reject; const promise = new Promise((res, rej) => { resolve = res; reject = rej; });`), or `Promise.withResolvers.call(SubPromise)` when constructing a `Promise` subclass.
- **DO** keep standard `new Promise((resolve, reject) => { ... })` when the asynchronous operation is self-contained inside the executor callback.
- **DO NOT** move synchronous setup code out of a `new Promise((resolve, reject) => { ... })` executor into `Promise.withResolvers()` without wrapping it in `try / catch` calling `reject(err)`: synchronous throws inside an executor automatically reject the promise, whereas throws after `Promise.withResolvers()` become uncaught synchronous exceptions.

#### Code Example

```js
export function createRequestGate() {
  const { promise, resolve, reject } = Promise.withResolvers();
  return {
    waitUntilReady: () => promise,
    open: (config) => resolve(config),
    abort: (reason) => reject(new Error(`Gate aborted: ${reason}`)),
  };
}
```

---

### Declarative Timeout and Composite Cancellation (`AbortSignal.timeout()` and `AbortSignal.any()`)

Use `AbortSignal.timeout(ms)` for time-bounded asynchronous operations and `AbortSignal.any(signals)` to combine multiple cancellation sources without manual timer bookkeeping.

#### Guidelines

- **DO** pass `{ signal: AbortSignal.timeout(ms) }` directly to `fetch()`, `addEventListener()`, streams, or abortable APIs instead of creating a one-off `AbortController` and `setTimeout(() => controller.abort(), ms)`.
- **DO** combine user-initiated cancellation (`AbortController`) with a deadline using `AbortSignal.any([controller.signal, AbortSignal.timeout(ms)])`. The composite signal aborts as soon as the first input signal aborts and propagates that signal's `reason`.
- **DO** check for both `'TimeoutError'` and `'AbortError'` when inspecting `error.name` in `catch` blocks if distinguishing user cancellation from a deadline matters.
- **DO NOT** assume `AbortSignal.timeout(ms)` aborts with `error.name === 'AbortError'`. Whereas `controller.abort()` without arguments sets `signal.reason` to `DOMException(..., 'AbortError')`, `AbortSignal.timeout(ms)` sets `DOMException(..., 'TimeoutError')` (`error.name === 'TimeoutError'`, `err.code === DOMException.TIMEOUT_ERR` / `23`).
- **DO NOT** pass `0`-arg or negative delays to `AbortSignal.timeout(ms)` (omitting `ms` throws `TypeError`; negative delays throw `RangeError` or `TypeError`), do not expect `AbortSignal.timeout(ms)` to keep a Node.js event loop alive on its own (Node.js uses an unref'd timer), and do not replace manual `AbortController` + `setTimeout` timers that reset on activity (sliding/idle debounce) or require a custom abort reason before expiry.

#### Code Example

```js
export async function fetchJsonWithDeadline(url, userSignal, timeoutMs = 5_000) {
  const signal = userSignal
    ? AbortSignal.any([userSignal, AbortSignal.timeout(timeoutMs)])
    : AbortSignal.timeout(timeoutMs);

  try {
    const response = await fetch(url, { signal });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status} for ${url}`);
    }
    return await response.json();
  } catch (err) {
    if (err instanceof DOMException && err.name === 'TimeoutError') {
      throw new Error(`Request to ${url} timed out after ${timeoutMs}ms`, { cause: err });
    }
    throw err;
  }
}
```

---

### Chaining Error Causes with Error Cause Options

Attach the original caught error via the `{ cause }` options parameter whenever wrapping and re-throwing an exception across architectural layers.

#### Guidelines

- **DO** pass `{ cause: err }` as the second argument to `new Error(message, { cause: err })` (or built-in subclasses: `TypeError`, `RangeError`, `SyntaxError`, `URIError`, `EvalError`, `AggregateError`); custom `Error` subclasses must accept and forward `(message, options)` to `super(message, options)` to preserve `.cause`.
- **DO** replace string-concatenated re-throws (`new Error('Failed: ' + err.message)`) with `new Error(message, { cause: err })` when concatenation was used solely as a substitute for structured error chaining—and retain interpolated `${err.message}` alongside `{ cause: err }` whenever callers or tests assert on the outer `.message` substring—rather than mutating `wrapper.cause = err` after construction (which sets an enumerable property instead of the non-enumerable spec property).
- **DO NOT** expose raw internal `cause` chains directly to untrusted client responses if the underlying error contains sensitive database queries, file paths, or credentials; log the full `error.cause` chain server-side and sanitize client-facing payloads.

#### Code Example

```js
export class ProfileLoadError extends Error {
  constructor(message, options) {
    super(message, options);
    this.name = 'ProfileLoadError';
  }
}

export async function loadUserProfile(userId, readRecord) {
  try {
    const raw = await readRecord(`users:${userId}`);
    return JSON.parse(raw);
  } catch (err) {
    throw new ProfileLoadError(
      `Failed to load profile for user "${userId}": ${err.message}`,
      { cause: err },
    );
  }
}
```

---

## 3. URL Query Manipulation and Binary Text Encoding

### Parsing and Constructing Query Strings (`URLSearchParams`)

Use `URLSearchParams` (and `new URL(input, base).searchParams`) to parse, inspect, mutate, and serialize query strings instead of manual `.split('&')` / `.split('=')` loops and `decodeURIComponent`.

#### Guidelines

- **DO** use `new URLSearchParams(search)` to read or mutate parameters (`.get(key)`, `.getAll(key)`, `.has(key)`, `.set(key, value)`, `.toString()`) or convert to a plain key-value dictionary with `Object.fromEntries(new URLSearchParams(search))`.
- **DO** use `new URL(fullUrl, baseOrigin).searchParams` when starting from a full URL string (`https://example.com/path?a=1#section`) rather than passing a full URL directly to `new URLSearchParams(fullUrl)` (which only strips a single leading `?` and treats `https://example.com/path?a` as part of the first key name).
- **DO** rely on `URLSearchParams` to preserve `=` characters inside parameter values (such as Base64 padding `?token=aGVsbG8=`, which `.split('=')[1]` truncates) and to avoid `Object.prototype` pollution when building lookup maps.
- **DO** account for the `application/x-www-form-urlencoded` rules enforced by `URLSearchParams`:
  - **Plus (`+`) decoding:** `URLSearchParams` decodes `+` as a space (`' '`), whereas `decodeURIComponent('a+b')` preserves `a+b`. Encode literal `+` values (phone numbers, Base64) as `%2B` at the source when `+` must stay literal.
  - **Valueless flags (`?debug` vs `?debug=`):** Both normalize to `""` (`params.has('debug') === true`, `params.get('debug') === ''`), whereas custom `split('=')` parsers sometimes assign `undefined` or `true`.
  - **Duplicate keys (`?tag=a&tag=b`):** `params.get('tag')` returns the **first** value (`'a'`), `Object.fromEntries(params)` retains the **last** value (`'b'`), and `params.getAll('tag')` returns `['a', 'b']`.
  - **Invalid percent-encoding, bracket keys, and `'??'`:** Non-hex escapes (`%ZZ`) stay literal `'%ZZ'` and invalid UTF-8 byte sequences (`%E0%A4%A`) become `\uFFFD` without throwing (keep `decodeURIComponent` inside `try / catch` when strict malformed-URI rejection is required); bracket keys (`?ids[]=1&user[name]=alice`) remain flat literal keys; and only a single leading `?` is stripped (`new URLSearchParams('??a=1')` keeps `'?a'` as the first key).
- **DO NOT** pass `location.hash` or hash-routing fragments directly to `new URLSearchParams(...)`: `URLSearchParams` does not strip `#`, so `'#tab=2'` parses the key as `'#tab'` (use `slice(1)`), and hash-routing fragments (`'#/route?a=1'`) require extracting the query segment after `?` before parsing (`hash.slice(hash.indexOf('?') + 1)`).
- **DO NOT** use `URLSearchParams` to parse semicolon-delimited strings (such as `document.cookie` or RFC 6265 `Cookie` headers); `URLSearchParams` splits exclusively on `&`.

#### Code Example

```js
// Parsing a query string into a plain object (last value wins on duplicate keys)
const query = '?filter=active&token=eyJhbGciOiJIUzI1NiJ9==&tag=js&tag=web';
const params = new URLSearchParams(query);

const token = params.get('token'); // 'eyJhbGciOiJIUzI1NiJ9==' (preserves trailing '==')
const allTags = params.getAll('tag'); // ['js', 'web']
const lastWinsDict = Object.fromEntries(params); // { filter: 'active', token: '...', tag: 'web' }

// Mutating query parameters on a full URL safely
const endpoint = new URL('https://api.example.com/v1/items?page=1#results');
endpoint.searchParams.set('page', '2');
endpoint.searchParams.append('limit', '50');
```

---

### Binary UTF-8 Text Decoding and Encoding (`TextDecoder` and `TextEncoder`)

Use `TextDecoder` and `TextEncoder` to convert between `Uint8Array` byte buffers and JavaScript strings.

#### Guidelines

- **DO** use `new TextDecoder().decode(bytes)` instead of `decodeURIComponent(escape(binaryString))`, `String.fromCharCode.apply(null, bytes)`, or `String.fromCharCode(...bytes)` when decoding UTF-8 byte buffers into text (`String.fromCharCode` treats bytes as UTF-16 code units—corrupting multi-byte UTF-8 into Latin-1 mojibake and overflowing the call stack at ~65 KB+—while `Uint16Array` elements `> 0xFF` represent 16-bit code units rather than raw UTF-8 bytes).
- **DO** use `new TextEncoder().encode(str)` to encode strings into UTF-8 `Uint8Array` byte arrays instead of manual character-code loops.
- **DO** reuse a single `TextDecoder` instance with `decoder.decode(chunk, { stream: true })` for chunked streams (`ReadableStream`, WebSocket frames, file chunks), followed by a final `decoder.decode()` flush call, so multi-byte code points split across chunk boundaries reassemble cleanly.
- **DO** pass `{ fatal: true }` when invalid UTF-8 sequences must throw `TypeError` instead of `\uFFFD` (note `TypeError` rather than `URIError`, and `decoder.decode(string)` always throws `TypeError`), and pass `{ ignoreBOM: true }` when a leading UTF-8 BOM (`0xEF 0xBB 0xBF`) must not be stripped by default.
- **DO** use `new TextDecoder('latin1')` (or `'iso-8859-1'`) only when a 1-byte-per-character mapping is needed on large buffers without call-stack limits, noting that per WHATWG Encoding both labels map to `windows-1252` (decoding bytes `0x80`–`0x9F` as characters such as `€` (`\u20AC`) rather than `\u0080`–`\u009F`).
- **DO NOT** replace `String.fromCharCode` with `new TextDecoder('utf-8')` when constructing a raw 1-byte-per-code-unit binary string (`0x00`–`0xFF`) for `btoa()` / `atob()`: use `TextEncoder` / `TextDecoder` for UTF-8 text payloads and chunked `String.fromCharCode` (or Node.js `Buffer.from(bytes).toString('base64')`) for raw binary strings passed to `btoa()`, since passing multi-byte UTF-8 `TextDecoder` output to `btoa()` throws `InvalidCharacterError`.

#### Code Example

```js
const encoder = new TextEncoder();
const decoder = new TextDecoder('utf-8', { fatal: true });

// Encode string to UTF-8 Uint8Array and decode back without stack limits
const bytes = encoder.encode('🚀 Modern Web Platform — 100% UTF-8');
const text = decoder.decode(bytes);

// Streaming decode across arbitrary chunk boundaries
export async function readUtf8Stream(readableStream) {
  const streamDecoder = new TextDecoder();
  let output = '';
  for await (const chunk of readableStream) {
    output += streamDecoder.decode(chunk, { stream: true });
  }
  output += streamDecoder.decode(); // Flush any trailing bytes
  return output;
}
```

---

## 4. DOM Child Replacement and Custom Events

### Atomic Child Replacement and Clearing (`Element.prototype.replaceChildren()`)

Use `element.replaceChildren(...nodesOrStrings)` to clear a container or replace all of its existing children in a single operation.

#### Guidelines

- **DO** call `container.replaceChildren()` with no arguments to remove all `childNodes` instead of `container.innerHTML = ''` (which invokes the HTML parser and fails under Trusted Types) or child-removal loops (forward `for` loops over live `children`/`childNodes` skip every other node, and `replaceChildren()` batches mutations into a single `MutationObserver` `childList` record—emitting `0` records on an already-empty element—and fires Custom Element `disconnectedCallback()` via `[CEReactions]` after all removals complete rather than interleaved per node).
- **DO** call `container.replaceChildren(...nodes)` to atomically clear and insert new `Node` instances or `DocumentFragment`s (`HierarchyRequestError` pre-validation fails atomically before mutating existing children).
- **DO** pass plain strings directly to `container.replaceChildren(text)` when inserting literal text without parsing HTML (note `el.replaceChildren('')` inserts an empty `Text` node with `childNodes.length === 1`, unlike `el.replaceChildren()`).
- **DO** target `templateElement.content.replaceChildren(...)` when clearing or replacing the contents of a `<template>` element (calling `templateElement.replaceChildren()` leaves its inert `content` `DocumentFragment` untouched), and narrow `Node` references to `ParentNode` (`Element`, `Document`, `DocumentFragment`) in TypeScript since leaf `Node`s (`Text`, `Comment`) do not implement `replaceChildren()`.
- **DO NOT** replace `while (el.firstElementChild) el.removeChild(el.firstElementChild)` when inline `Text` or `Comment` nodes must remain intact (`replaceChildren()` removes all `childNodes`), do not replace chained assignments (`a.innerHTML = b.innerHTML = ''`, since `replaceChildren()` returns `undefined`), do not pass raw HTML markup strings (`'<li>Item</li>'`) expecting parsed elements (for untrusted HTML strings, follow `sanitize-untrusted-html` (via `npx -y modern-web-guidance@latest retrieve "sanitize-untrusted-html"`)), do not pass a live `HTMLCollection`/`NodeList` (`source.children`) when `source` must keep copies, and do not replace `element.innerHTML = ''` on `<object>` or `<embed>` plugin containers or test harnesses asserting HTML parser steps.

#### Code Example

```js
export function renderNotificationList(listElement, messages) {
  const items = messages.map((msg) => {
    const li = document.createElement('li');
    li.className = 'notification-item';
    li.textContent = msg;
    return li;
  });

  // Atomically replaces all existing <li> children in a single DOM operation
  listElement.replaceChildren(...items);
}

// Clearing a <template> element's inert DocumentFragment
export function clearTemplate(templateEl) {
  templateEl.content.replaceChildren();
}
```

---

### Constructing Standard and Custom Events (`new Event()` and `new CustomEvent()`)

Use `new Event(type, options)`, `new CustomEvent(type, options)`, and specialized WebIDL event constructors instead of the deprecated `document.createEvent()` and `initEvent()` / `initCustomEvent()` methods.

#### Guidelines

- **DO** use `new Event(type, { bubbles, cancelable, composed })` for standard notifications, `new CustomEvent(type, { detail, bubbles, cancelable, composed })` for structured `event.detail` payloads, and specialized WebIDL constructors (`new MouseEvent()`, `new KeyboardEvent()`, `new UIEvent()`) when replacing `initMouseEvent` / `initKeyboardEvent` / `initUIEvent` (avoiding legacy `initKeyboardEvent` argument quirks and read-only `keyCode === 0` issues).
- **DO** specify `bubbles: true` and `cancelable: true` explicitly whenever an event must bubble up the DOM tree or support `event.preventDefault()` (both default to `false`), and set `composed: true` when crossing a Shadow DOM boundary.
- **DO NOT** use `document.createEvent('Event')`, `document.createEvent('CustomEvent')`, `event.initEvent()`, or `event.initCustomEvent()`, and do not pass non-`EventTarget` values for WebIDL dictionary fields (e.g., `relatedTarget: 0` in `MouseEventInit` throws `TypeError`).

#### Code Example

```js
// Dispatching a bubbling, shadow-piercing custom event with payload data
export function notifyFilterChange(filterPanel) {
  const filterChanged = new CustomEvent('filter-change', {
    detail: { category: 'architecture', minScore: 80 },
    bubbles: true,
    cancelable: true,
    composed: true,
  });

  return filterPanel.dispatchEvent(filterChanged);
}
```

