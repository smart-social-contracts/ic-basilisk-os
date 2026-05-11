import { e as ensure_array_like, s as store_get, a as escape_html, u as unsubscribe_stores, b as attr, c as slot } from "../../chunks/renderer.js";
import { i as isAuthenticated, p as principal } from "../../chunks/auth.js";
import { t as toasts } from "../../chunks/toast.js";
function Toast($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    $$renderer2.push(`<div class="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm"><!--[-->`);
    const each_array = ensure_array_like(store_get($$store_subs ??= {}, "$toasts", toasts));
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let toast = each_array[$$index];
      $$renderer2.push(`<div class="card px-4 py-3 flex items-start gap-3 shadow-lg" role="alert"><div class="shrink-0 mt-0.5">`);
      if (toast.type === "success") {
        $$renderer2.push("<!--[0-->");
        $$renderer2.push(`<svg class="w-4 h-4 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path></svg>`);
      } else if (toast.type === "error") {
        $$renderer2.push("<!--[1-->");
        $$renderer2.push(`<svg class="w-4 h-4 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path stroke-linecap="round" d="M12 8v4m0 4h.01"></path></svg>`);
      } else {
        $$renderer2.push("<!--[-1-->");
        $$renderer2.push(`<svg class="w-4 h-4 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path stroke-linecap="round" d="M12 16v-4m0-4h.01"></path></svg>`);
      }
      $$renderer2.push(`<!--]--></div> <p class="text-sm text-primary-800 flex-1">${escape_html(toast.message)}</p> <button class="shrink-0 text-primary-400 hover:text-primary-700 transition-colors" aria-label="Dismiss"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path></svg></button></div>`);
    }
    $$renderer2.push(`<!--]--></div>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
function _layout($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    $$renderer2.push(`<div class="min-h-screen bg-[var(--color-bg-secondary)]"><nav class="sticky top-0 z-30 bg-white border-b border-[var(--color-border-primary)]" style="box-shadow: var(--shadow-sm);"><div class="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between"><a href="/" class="flex items-center gap-2.5 group"><div class="w-7 h-7 rounded-lg flex items-center justify-center" style="background: var(--gradient-institutional);"><svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M20.25 6.375c0 2.278-3.694 4.125-8.25 4.125S3.75 8.653 3.75 6.375m16.5 0c0-2.278-3.694-4.125-8.25-4.125S3.75 4.097 3.75 6.375m16.5 0v11.25c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125V6.375m16.5 0v3.75c0 2.278-3.694 4.125-8.25 4.125s-8.25-1.847-8.25-4.125v-3.75"></path></svg></div> <span class="text-lg font-semibold text-primary-900 group-hover:text-primary-700 transition-colors">IC File Registry</span></a> <div class="flex items-center gap-3">`);
    if (store_get($$store_subs ??= {}, "$isAuthenticated", isAuthenticated)) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<span class="hidden sm:block text-xs text-primary-400 font-mono truncate max-w-[180px]"${attr("title", store_get($$store_subs ??= {}, "$principal", principal))}>${escape_html(store_get($$store_subs ??= {}, "$principal", principal).slice(0, 5))}...${escape_html(store_get($$store_subs ??= {}, "$principal", principal).slice(-5))}</span> <button class="btn-ghost btn-sm"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9"></path></svg> <span class="hidden sm:inline">Log out</span></button>`);
    } else {
      $$renderer2.push("<!--[-1-->");
      $$renderer2.push(`<button class="btn-primary btn-sm"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0"></path></svg> Login with Internet Identity</button>`);
    }
    $$renderer2.push(`<!--]--></div></div></nav> <main class="max-w-6xl mx-auto px-4 sm:px-6 py-6 sm:py-8"><!--[-->`);
    slot($$renderer2, $$props, "default", {});
    $$renderer2.push(`<!--]--></main> <footer class="border-t border-[var(--color-border-primary)] mt-auto"><div class="max-w-6xl mx-auto px-4 sm:px-6 py-4"><p class="text-xs text-primary-400 text-center">IC File Registry · On-chain file storage on the Internet Computer</p></div></footer></div> `);
    Toast($$renderer2);
    $$renderer2.push(`<!---->`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _layout as default
};
