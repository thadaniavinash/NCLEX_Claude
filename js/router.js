/* Addresses and the browser's Back / Forward buttons.

   Each page of the frame has its own address, so a reload or a bookmark opens the same page:
     practice site   ./                  Home
                     ./?page=progress    My progress
                     ./?page=practise    Practise (session builder)
     studio          ./?studio           Overview   (./?author=1 and ./?studio=1 still work)
                     ./?studio&page=bank Question bank
   The sign-in page keeps the address of the studio page it leads to.
   The exam player, the editor, results and the paused page keep the address they were opened from but
   get their own history entry, so Back leaves them for the page underneath (the player saves the
   student's answers first, the editor saves the item first).

   Every entry's state is { view, prev }: prev is the view of the entry underneath, so a button that
   returns to that view (the editor's "Question bank", Home after results) steps back in history instead
   of adding an entry, and Back afterwards does what the author expects. */

const ROUTED_VIEWS = {
  home: '',
  progress: 'page=progress',
  student: 'page=practise',
  overview: 'studio',
  dashboard: 'studio&page=bank'
};
const OVERLAY_VIEWS = ['player', 'editor', 'results', 'paused', 'signin', 'link'];

let routerOn = false;
let routerStarted = false;      // set by initApp once it starts showing the page the address asks for
let routerFromHistory = false; // true while a Back / Forward is being shown
let routerInitialDone = false;

function urlForView(view) {
  if (view === 'signin') view = (typeof signinReturnView !== 'undefined' && ROUTED_VIEWS[signinReturnView] !== undefined) ? signinReturnView : 'overview';
  const q = ROUTED_VIEWS[view];
  return window.location.pathname + (q ? `?${q}` : '');
}

function isStudioAddress(params) {
  return params.has('studio') || params.get('author') === '1';
}

// The page an address asks for (ignoring item links such as ?case=, handled in initApp).
function viewFromUrl(search) {
  const params = new URLSearchParams(search === undefined ? window.location.search : search);
  const page = params.get('page');
  if (isStudioAddress(params)) return page === 'bank' ? 'dashboard' : 'overview';
  if (page === 'progress') return 'progress';
  if (page === 'practise' || page === 'practice') return 'student';
  return 'home';
}

function currentRouteState() {
  return history.state && history.state.view ? history.state : null;
}

// The first entry: an item link (?case=, ?code=) keeps its address and is marked as such.
function markInitialLinkEntry() {
  if (!routerOn || !routerStarted) return;
  history.replaceState({ view: 'link', prev: null }, '', window.location.href);
  routerInitialDone = true;
}

// Called by switchView after it has shown `view`.
function recordViewInHistory(view) {
  if (!routerOn || !routerStarted || routerFromHistory) return;
  const routed = ROUTED_VIEWS[view] !== undefined;
  const url = routed || view === 'signin' ? urlForView(view) : window.location.pathname + window.location.search;
  const cur = currentRouteState();

  if (!routerInitialDone || !cur) {
    routerInitialDone = true;
    history.replaceState({ view, prev: null }, '', url);
    return;
  }
  if (cur.view === view) {
    if (routed || view === 'signin') history.replaceState(cur, '', url);
    return;
  }
  const curIsOverlay = OVERLAY_VIEWS.includes(cur.view);
  // Back to the page underneath (editor -> Question bank, results -> Home): step back instead.
  if (curIsOverlay && cur.prev === view && cur.view !== 'link') {
    routerSkipNextPop = view;
    history.back();
    return;
  }
  // The session ended (results or the paused page take the player's place), the sign-in page gives way
  // to the page it led to: replace, keeping what is underneath.
  if ((cur.view === 'player' && (view === 'results' || view === 'paused')) || cur.view === 'signin') {
    history.replaceState({ view, prev: cur.prev }, '', url);
    return;
  }
  history.pushState({ view, prev: cur.view }, '', url);
}

let routerSkipNextPop = null;

function activeViewId() {
  const active = document.querySelector('.view.active');
  return active ? active.id.replace(/-view$/, '') : null;
}

// Leaving the player or the editor because of Back: keep the student's answers, save the author's edits.
// Returns false when the editor could not save (it then stays open).
function leaveOverlayForHistory(active) {
  ['resume-modal', 'test-submit-modal', 'skip-question-modal'].forEach(id => {
    const m = document.getElementById(id);
    if (m) m.classList.add('hidden');
  });
  if (typeof closeShareDialog === 'function') closeShareDialog();
  if (active === 'player' && typeof saveCurrentAttempt === 'function' && sessionConfig && !sessionConfig.isRemediation) saveCurrentAttempt();
  if (active === 'editor') {
    if (!saveCurrentStepData(false, true)) return false;
    saveCurrentCaseOrStandalone();
  }
  return true;
}

function showFromHistory(view) {
  routerFromHistory = true;
  try { switchView(view); } finally { routerFromHistory = false; }
}

function onRouterPopState(e) {
  const state = e.state && e.state.view ? e.state : { view: viewFromUrl(), prev: null };
  const active = activeViewId();
  if (routerSkipNextPop && routerSkipNextPop === state.view) {
    // The app already shows this page (it asked for the step back itself).
    routerSkipNextPop = null;
    return;
  }
  routerSkipNextPop = null;
  if (active === state.view) return;

  if (active === 'player' || active === 'editor') {
    if (!leaveOverlayForHistory(active)) {
      // The editor stays open: put its entry back.
      history.pushState({ view: 'editor', prev: state.view }, '', window.location.href);
      return;
    }
  }

  let target = state.view;
  // Entries of a session or editor that has since closed (Forward, or Back past them): show the page
  // they were opened from instead.
  if (target === 'player' || target === 'editor' || target === 'link' || target === 'signin') {
    target = ROUTED_VIEWS[state.prev] !== undefined ? state.prev : viewFromUrl();
    if (target === 'home' && isStudioAddress(new URLSearchParams(window.location.search))) target = 'overview';
    if (state.view === 'editor') target = 'dashboard';
    history.replaceState({ view: target, prev: null }, '', urlForView(target));
  }
  if ((target === 'results' || target === 'paused') && !(typeof currentCase !== 'undefined' && currentCase)) {
    target = 'home';
    history.replaceState({ view: target, prev: null }, '', urlForView(target));
  }
  showFromHistory(target);
}

// From here on, switchView records history (views shown while the app loads are not pages yet).
function startRouting() {
  routerStarted = true;
}

function initRouter() {
  routerOn = !!(window.history && history.replaceState);
  if (routerOn) window.addEventListener('popstate', onRouterPopState);
}
