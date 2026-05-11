import { s as store_get, h as head, b as attr, a as escape_html, e as ensure_array_like, u as unsubscribe_stores, f as stringify } from "../../../../chunks/renderer.js";
import { p as page } from "../../../../chunks/stores.js";
import "@dfinity/agent";
import "@dfinity/auth-client";
import "../../../../chunks/toast.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let namespace, filePath, filename;
    namespace = decodeURIComponent(store_get($$store_subs ??= {}, "$page", page).params.namespace);
    filePath = store_get($$store_subs ??= {}, "$page", page).params.path;
    filename = filePath.split("/").pop() ?? filePath;
    head("zk3bgy", $$renderer2, ($$renderer3) => {
      $$renderer3.title(($$renderer4) => {
        $$renderer4.push(`<title>${escape_html(filename)} — ${escape_html(namespace)} — IC File Registry</title>`);
      });
    });
    $$renderer2.push(`<div class="space-y-6 animate-fade-in"><nav class="flex items-center gap-2 text-sm flex-wrap"><a href="/" class="text-primary-500 hover:text-primary-700 transition-colors">Registry</a> <svg class="w-4 h-4 text-primary-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"></path></svg> <a${attr("href", `/${stringify(encodeURIComponent(namespace))}`)} class="text-primary-500 hover:text-primary-700 transition-colors font-mono">${escape_html(namespace)}</a> <svg class="w-4 h-4 text-primary-300 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5"></path></svg> <span class="text-primary-800 font-medium font-mono">${escape_html(filename)}</span></nav> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="grid grid-cols-1 lg:grid-cols-[1fr_280px] gap-6"><div><div class="card p-4 mb-4"><div class="flex items-center gap-3 mb-4"><div class="skeleton h-6 w-48"></div></div> <div class="skeleton h-3 w-32 mb-2"></div> <div class="skeleton h-3 w-24"></div></div> <div class="card overflow-hidden"><!--[-->`);
      const each_array = ensure_array_like([1, 2, 3, 4, 5, 6, 7, 8]);
      for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
        each_array[$$index];
        $$renderer2.push(`<div class="px-4 py-2 border-b border-primary-100"><div class="skeleton h-4 w-full"></div></div>`);
      }
      $$renderer2.push(`<!--]--></div></div> <div class="card p-4"><div class="skeleton h-4 w-20 mb-4"></div> <!--[-->`);
      const each_array_1 = ensure_array_like([1, 2, 3]);
      for (let $$index_1 = 0, $$length = each_array_1.length; $$index_1 < $$length; $$index_1++) {
        each_array_1[$$index_1];
        $$renderer2.push(`<div class="skeleton h-12 w-full mb-2 rounded-lg"></div>`);
      }
      $$renderer2.push(`<!--]--></div></div>`);
    }
    $$renderer2.push(`<!--]--></div>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
