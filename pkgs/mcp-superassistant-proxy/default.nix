{
  buildNpmPackage,
  fetchurl,
  lib,
}:
buildNpmPackage rec {
  pname = "mcp-superassistant-proxy";
  version = "";

  src = fetchurl {
    url = "https://registry.npmjs.org/@srbhptl39/mcp-superassistant-proxy/-/mcp-superassistant-proxy-${version}.tgz";
    hash = "";
  };

  npmDepsHash = "";

  postPatch = ''
    npm install --package-lock-only
  '';

  NODE_OPTIONS = "--openssl-legacy-provider";

  passthru.updateScript = ''
    		
    	'';

  meta = {
    description = "MCP Proxy Server software to run SSE and stdio based servers";
    mainProgram = "@srbhptl39/mcp-superassistant-proxy";
    homepage = "https://www.npmjs.com/package/@srbhptl39/mcp-superassistant-proxy";
    licence = lib.licenses.unfree;
    maintainers = with lib.maintainers; [ eveeifyeve ];
  };
}
