import { i as fallback, a as escape_html, d as attr_class, j as bind_props, f as stringify, s as store_get, u as unsubscribe_stores, h as head, b as attr, e as ensure_array_like } from "../../../chunks/renderer.js";
import { p as page } from "../../../chunks/stores.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/root.js";
import "../../../chunks/state.svelte.js";
import { f as formatBytes, t as timeAgo } from "../../../chunks/api.js";
import { i as isAuthenticated } from "../../../chunks/auth.js";
import "../../../chunks/toast.js";
function ConfirmModal($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let open = fallback($$props["open"], false);
    let title = fallback($$props["title"], "Confirm");
    let message = fallback($$props["message"], "");
    let confirmLabel = fallback($$props["confirmLabel"], "Confirm");
    let danger = fallback($$props["danger"], false);
    if (open) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="fixed inset-0 z-40 flex items-center justify-center"><div class="absolute inset-0 bg-primary-900/40 backdrop-blur-sm"></div> <div class="relative bg-white rounded-xl shadow-xl max-w-md w-full mx-4 p-6"><h3 class="text-lg font-semibold text-primary-900 mb-2">${escape_html(title)}</h3> <p class="text-sm text-primary-600 mb-6">${escape_html(message)}</p> <div class="flex items-center justify-end gap-3"><button class="btn-secondary btn-sm">Cancel</button> <button${attr_class(`${stringify(danger ? "btn-danger" : "btn-primary")} btn-sm`)}>${escape_html(confirmLabel)}</button></div></div></div>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]-->`);
    bind_props($$props, { open, title, message, confirmLabel, danger });
  });
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let namespace, filtered;
    let files = [];
    let search = "";
    let copiedPath = "";
    let confirmOpen = false;
    let confirmTitle = "";
    let confirmMessage = "";
    namespace = decodeURIComponent(store_get($$store_subs ??= {}, "$page", page).params.namespace);
    filtered = files.filter((f) => f.path.toLowerCase().includes(search.toLowerCase()) || f.content_type.toLowerCase().includes(search.toLowerCase()));
    let $$settled = true;
    let $$inner_renderer;
    function $$render_inner($$renderer3) {
      head("1ydds2c", $$renderer3, ($$renderer4) => {
        $$renderer4.title(($$renderer5) => {
          $$renderer5.push(`<title>${escape_html(namespace)} — IC File Registry</title>`);
        });
      });
      $$renderer3.push(`<div class="space-y-6 animate-fade-in"><nav class="flex items-center gap-2 text-sm"><a href="/" class="text-primary-500 hover:text-primary-700 transition-colors">Registry</a> <svg class="w-4 h-4 text-primary-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"></path></svg> <span class="text-primary-800 font-medium font-mono">${escape_html(namespace)}</span></nav> <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4"><div><h1 class="text-xl font-bold text-primary-900 font-mono">${escape_html(namespace)}</h1> <p class="text-xs text-primary-500 mt-0.5">${escape_html(files.length)} ${escape_html(files.length === 1 ? "file" : "files")}</p></div> <div class="flex items-center gap-2 self-start"><button class="btn-icon" title="Refresh"><svg${attr_class(`w-4 h-4 ${stringify("animate-spin")}`)} fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182"></path></svg></button> `);
      if (store_get($$store_subs ??= {}, "$isAuthenticated", isAuthenticated)) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`<button class="btn-secondary btn-sm"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"></path></svg> ACL</button> <button class="btn-danger btn-sm"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"></path></svg> Delete</button>`);
      } else {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]--></div></div> `);
      {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]--> `);
      {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]--> `);
      if (store_get($$store_subs ??= {}, "$isAuthenticated", isAuthenticated)) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`<div role="region" aria-label="File upload area"${attr_class(`card border-2 border-dashed p-8 text-center transition-all cursor-pointer ${stringify("border-primary-200 hover:border-primary-400")}`)}>`);
        {
          $$renderer3.push("<!--[-1-->");
          $$renderer3.push(`<svg class="w-8 h-8 mx-auto text-primary-300 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5"></path></svg> <p class="text-primary-500 text-sm mb-3">Drag &amp; drop files here, or</p> <label class="cursor-pointer"><span class="btn-primary btn-sm">Choose files</span> <input type="file" multiple="" class="hidden"/></label> <p class="text-xs text-primary-400 mt-3">Files > 500 KB are uploaded in chunks automatically.</p>`);
        }
        $$renderer3.push(`<!--]--></div>`);
      } else {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]--> `);
      if (files.length > 5) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`<div class="relative"><svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-primary-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><path stroke-linecap="round" d="m21 21-4.35-4.35"></path></svg> <input type="text"${attr("value", search)} placeholder="Filter files..." class="input pl-10"/></div>`);
      } else {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]--> `);
      if (files.length === 0) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`<div class="card overflow-hidden"><div class="px-4 py-3 bg-primary-50 border-b border-primary-200"><div class="skeleton h-3 w-20"></div></div> <!--[-->`);
        const each_array_1 = ensure_array_like([1, 2, 3, 4, 5]);
        for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
          each_array_1[$$index_1];
          $$renderer3.push(`<div class="px-4 py-3 border-b border-primary-100 flex items-center justify-between"><div class="skeleton h-4 w-48"></div> <div class="skeleton h-4 w-16"></div></div>`);
        }
        $$renderer3.push(`<!--]--></div>`);
      } else if (files.length === 0) {
        $$renderer3.push("<!--[1-->");
        $$renderer3.push(`<div class="text-center py-12"><svg class="w-12 h-12 mx-auto text-primary-200 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"></path></svg> <p class="text-primary-500 text-sm font-medium">No files in this namespace yet</p> `);
        if (store_get($$store_subs ??= {}, "$isAuthenticated", isAuthenticated)) {
          $$renderer3.push("<!--[0-->");
          $$renderer3.push(`<p class="text-primary-400 text-xs mt-1">Upload files using the area above.</p>`);
        } else {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]--></div>`);
      } else {
        $$renderer3.push("<!--[-1-->");
        $$renderer3.push(`<div class="card overflow-hidden"><div class="overflow-x-auto"><table class="w-full text-sm"><thead><tr class="bg-primary-50 border-b border-primary-200"><th class="text-left px-4 py-3 text-xs font-semibold text-primary-500 uppercase tracking-wider">File</th><th class="text-left px-4 py-3 text-xs font-semibold text-primary-500 uppercase tracking-wider hidden sm:table-cell">Type</th><th class="text-right px-4 py-3 text-xs font-semibold text-primary-500 uppercase tracking-wider">Size</th><th class="text-right px-4 py-3 text-xs font-semibold text-primary-500 uppercase tracking-wider hidden md:table-cell">Updated</th><th class="text-right px-4 py-3 text-xs font-semibold text-primary-500 uppercase tracking-wider w-24"></th></tr></thead><tbody><!--[-->`);
        const each_array_2 = ensure_array_like(filtered);
        for (let $$index_2 = 0, $$length = each_array_2.length; $$index_2 < $$length; $$index_2++) {
          let file = each_array_2[$$index_2];
          $$renderer3.push(`<tr class="border-b border-primary-100 hover:bg-primary-50/50 transition-colors"><td class="px-4 py-3"><a${attr("href", `/${stringify(encodeURIComponent(namespace))}/${stringify(file.path)}`)} class="font-mono text-xs text-primary-700 hover:text-primary-900 hover:underline transition-colors">${escape_html(file.path)}</a></td><td class="px-4 py-3 text-xs text-primary-400 hidden sm:table-cell">${escape_html(file.content_type)}</td><td class="px-4 py-3 text-xs text-primary-500 text-right">${escape_html(formatBytes(file.size))}</td><td class="px-4 py-3 text-xs text-primary-400 text-right hidden md:table-cell">${escape_html(timeAgo(file.updated))}</td><td class="px-4 py-3"><div class="flex items-center justify-end gap-1"><a${attr("href", `/${stringify(encodeURIComponent(namespace))}/${stringify(file.path)}`)} class="btn-icon p-1.5" title="View file"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"></path><circle cx="12" cy="12" r="3"></circle></svg></a> <button title="Copy URL" class="btn-icon p-1.5">`);
          if (copiedPath === file.path) {
            $$renderer3.push("<!--[0-->");
            $$renderer3.push(`<svg class="w-4 h-4 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"></path></svg>`);
          } else {
            $$renderer3.push("<!--[-1-->");
            $$renderer3.push(`<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184"></path></svg>`);
          }
          $$renderer3.push(`<!--]--></button> `);
          if (store_get($$store_subs ??= {}, "$isAuthenticated", isAuthenticated)) {
            $$renderer3.push("<!--[0-->");
            $$renderer3.push(`<button title="Delete file" class="btn-icon p-1.5 hover:!text-red-500"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"></path></svg></button>`);
          } else {
            $$renderer3.push("<!--[-1-->");
          }
          $$renderer3.push(`<!--]--></div></td></tr>`);
        }
        $$renderer3.push(`<!--]--></tbody></table></div></div> `);
        {
          $$renderer3.push("<!--[-1-->");
        }
        $$renderer3.push(`<!--]-->`);
      }
      $$renderer3.push(`<!--]--></div> `);
      ConfirmModal($$renderer3, {
        title: confirmTitle,
        message: confirmMessage,
        confirmLabel: "Delete",
        danger: true,
        get open() {
          return confirmOpen;
        },
        set open($$value) {
          confirmOpen = $$value;
          $$settled = false;
        }
      });
      $$renderer3.push(`<!---->`);
    }
    do {
      $$settled = true;
      $$inner_renderer = $$renderer2.copy();
      $$render_inner($$inner_renderer);
    } while (!$$settled);
    $$renderer2.subsume($$inner_renderer);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
