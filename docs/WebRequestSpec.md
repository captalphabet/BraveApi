```typescript
interface BraveWebSearchRequest {
  q: string;                       // Required: User's search query (max 400 chars, 50 words)
  country?: string;                // Optional: 2-letter country code (default: "US")
  search_lang?: string;            // Optional: Language code for search results (default: "en")
  ui_lang?: string;                // Optional: UI language, format "<lang>-<country>" (default: "en-US")
  count?: number;                  // Optional: Number of web results (max 20, default: 20)
  offset?: number;                 // Optional: Zero-based page offset for pagination (max 9, default: 0)
  safesearch?: "off" | "moderate" | "strict";  // Optional: Adult content filter (default: "moderate")
  freshness?: string;              // Optional: Filter by date discovered e.g. "pd", "pw", "pm", "py", or "YYYY-MM-DDtoYYYY-MM-DD"
  text_decorations?: boolean;     // Optional: Whether to include text decorations in snippets (default: true)
  spellcheck?: boolean;            // Optional: Whether to spellcheck query (default: true)
  result_filter?: string;          // Optional: Comma-separated result types to include (e.g. "web,news,videos")
  goggles?: string[];              // Optional: List of goggles URLs or definitions for custom re-ranking
  units?: "metric" | "imperial";  // Optional: Measurement units (default from country)
  extra_snippets?: boolean;        // Optional: Include up to 5 extra snippets (default: false)
  summary?: boolean;               // Optional: Enable summary generation (default: false)
}
```
