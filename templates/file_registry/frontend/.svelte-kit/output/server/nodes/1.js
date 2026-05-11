

export const index = 1;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/fallbacks/error.svelte.js')).default;
export const imports = ["_app/immutable/nodes/1.0eeN_KYo.js","_app/immutable/chunks/Dg3Y8UVu.js","_app/immutable/chunks/BRWXwaBk.js","_app/immutable/chunks/CXZFu-FS.js"];
export const stylesheets = [];
export const fonts = [];
