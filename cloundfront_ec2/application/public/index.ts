import { proxy } from "https://deno.land/x/oak_http_proxy@2.1.0/mod.ts";
import { Application, Router } from "https://deno.land/x/oak@v10.1.0/mod.ts";
import staticFiles from "https://deno.land/x/static_files@1.1.6/mod.ts";

const app = new Application();

app.use(async (ctx, next) => {
  await next();
  console.log(`${ctx.request.method} ${ctx.request.url}`);
});

app.addEventListener("error", (event) => {
  console.log("ERROR", event.error);
});

app.use(staticFiles("public"));

const router = new Router();
router.get("/", proxy("https://teste-de-widgets.bonde.org", {
    srcResHeaderDecorator(headers, req, res, proxyReq, proxyRes) {
	console.log('headers');
	console.log(headers.delete("cache-control"));
      // delete headers[headers.indexOf("cache-control")]
      return headers;
    },
}));
app.use(router.allowedMethods());
app.use(router.routes());
await app.listen({ hostname: "0.0.0.0", port: 80 });