import { w as writable } from "./index.js";
const { subscribe, update } = writable([]);
let nextId = 0;
function add(type, message, duration = 4e3) {
  const id = nextId++;
  update((all) => [...all, { id, type, message }]);
  if (duration > 0) {
    setTimeout(() => dismiss(id), duration);
  }
}
function dismiss(id) {
  update((all) => all.filter((t) => t.id !== id));
}
const toasts = {
  subscribe,
  success: (msg) => add("success", msg),
  error: (msg) => add("error", msg, 6e3),
  info: (msg) => add("info", msg),
  dismiss
};
export {
  toasts as t
};
