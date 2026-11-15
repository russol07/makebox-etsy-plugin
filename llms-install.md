# Installing MakeBox for Etsy (MCP)

MakeBox for Etsy is a **hosted remote MCP server**. There is nothing to clone, build or run locally and no API key.

- Server URL: `https://mcp.makebox.ai/mcp`
- Transport: Streamable HTTP
- Authentication: OAuth 2.1 with dynamic client registration (the client opens a browser; the user signs in to MakeBox and presses **Connect**)

## Cline

Add this entry to `cline_mcp_settings.json` (Cline → MCP Servers → Configure MCP Servers):

```json
{
  "mcpServers": {
    "makebox": {
      "type": "streamableHttp",
      "url": "https://mcp.makebox.ai/mcp"
    }
  }
}
```

Then start the server in Cline and complete the MakeBox sign-in in the browser window that opens.

## Other clients

- Claude Code: `claude mcp add --transport http makebox https://mcp.makebox.ai/mcp`, then `/mcp` → Authenticate.
- Codex CLI: `codex mcp add makebox --url https://mcp.makebox.ai/mcp`, then `codex mcp login makebox`.
- Cursor / VS Code / Windsurf: add a remote MCP server with the URL above.
- ChatGPT, Claude, Gemini, Grok, Perplexity, Mistral: step-by-step guides at https://app.makebox.ai/connector

## First request

Ask: "Use MakeBox to check my plan, then research keywords for ceramic mugs. Do not change anything."
Keyword, niche and public competitor research works without an Etsy shop. Reading private shop data and changing listings requires the user's own Etsy connection and their explicit confirmation for every write.
