import "@dfinity/auth-client";
import { w as writable } from "./index.js";
const isAuthenticated = writable(false);
const principal = writable("");
export {
  isAuthenticated as i,
  principal as p
};
