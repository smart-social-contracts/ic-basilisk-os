export const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set([]),
	mimeTypes: {},
	_: {
		client: {start:"_app/immutable/entry/start.Bw1OJVEg.js",app:"_app/immutable/entry/app.R6LxQtre.js",imports:["_app/immutable/entry/start.Bw1OJVEg.js","_app/immutable/chunks/CXZFu-FS.js","_app/immutable/chunks/BRWXwaBk.js","_app/immutable/entry/app.R6LxQtre.js","_app/immutable/chunks/DWYQT3AE.js","_app/immutable/chunks/BRWXwaBk.js","_app/immutable/chunks/Dg3Y8UVu.js","_app/immutable/chunks/mJvOm6gK.js"],stylesheets:[],fonts:[],uses_env_dynamic_public:false},
		nodes: [
			__memo(() => import('./nodes/0.js')),
			__memo(() => import('./nodes/1.js')),
			__memo(() => import('./nodes/2.js')),
			__memo(() => import('./nodes/3.js')),
			__memo(() => import('./nodes/4.js'))
		],
		remotes: {
			
		},
		routes: [
			{
				id: "/",
				pattern: /^\/$/,
				params: [],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			},
			{
				id: "/[namespace]",
				pattern: /^\/([^/]+?)\/?$/,
				params: [{"name":"namespace","optional":false,"rest":false,"chained":false}],
				page: { layouts: [0,], errors: [1,], leaf: 3 },
				endpoint: null
			},
			{
				id: "/[namespace]/[...path]",
				pattern: /^\/([^/]+?)(?:\/([^]*))?\/?$/,
				params: [{"name":"namespace","optional":false,"rest":false,"chained":false},{"name":"path","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 4 },
				endpoint: null
			}
		],
		prerendered_routes: new Set([]),
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();
