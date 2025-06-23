## Brave Web Search API – Response Object Specs (Markdown)

### WebSearchApiResponse

| Field            | Type      | Required | Description                                                             |
|------------------|-----------|----------|-------------------------------------------------------------------------|
| type             | "search"  | Yes      | The type of web search API result (always "search").                    |
| discussions      | Discussions         | No       | Discussion clusters from forums relevant to the query.                   |
| faq              | FAQ                | No       | FAQs relevant to the search query.                                      |
| infobox          | GraphInfobox       | No       | Aggregated entity info for an infobox.                                  |
| locations        | Locations          | No       | Places of interest for location-sensitive queries.                      |
| mixed            | MixedResponse      | No       | Preferred ranked order of search results.                               |
| news             | News               | No       | News results relevant to the query.                                     |
| query            | Query              | No       | Original and modified search query info.                                |
| videos           | Videos             | No       | Videos relevant to the query.                                           |
| web              | Search             | No       | Web search results relevant to the query.                               |
| summarizer       | Summarizer         | No       | Summary key for summaries of the query.                                 |
| rich             | RichCallbackInfo   | No       | Callback info for rich results.                                         |

---

### LocalPoiSearchApiResponse

| Field   | Type                        | Required | Description                                      |
|---------|-----------------------------|----------|--------------------------------------------------|
| type    | "local_pois"                | Yes      | API result type (always "local_pois").           |
| results | list [LocationResult]       | No       | Location results matching the requested IDs.      |

---

### LocalDescriptionsSearchApiResponse

| Field   | Type                              | Required | Description                                    |
|---------|-----------------------------------|----------|------------------------------------------------|
| type    | "local_descriptions"              | Yes      | API result type (always "local_descriptions"). |
| results | list [LocationDescription]        | No       | Generated descriptions for requested locations.|

---

### Query

| Field                  | Type      | Required | Description                                    |
|------------------------|-----------|----------|------------------------------------------------|
| original               | string    | Yes      | The original query string.                      |
| show_strict_warning    | bool      | No       | True if response restricted by safesearch.      |
| altered                | string    | No       | Altered query used for search.                  |
| safesearch             | bool      | No       | Whether safesearch was enabled.                 |
| is_navigational        | bool      | No       | Query is navigational to a domain.              |
| is_geolocal            | bool      | No       | Query has location relevance.                   |
| local_decision         | string    | No       | Marked as location sensitive.                   |
| local_locations_idx    | int       | No       | Index of the location.                          |
| is_trending            | bool      | No       | Query is currently trending.                    |
| is_news_breaking       | bool      | No       | Query has breaking news.                        |
| ask_for_location       | bool      | No       | Query needs location for better results.        |
| language               | Language  | No       | Language info of the query.                     |
| spellcheck_off         | bool      | No       | Spellchecker was off.                           |
| country                | string    | No       | Country used for the query.                     |
| bad_results            | bool      | No       | Query yields bad results.                       |
| should_fallback        | bool      | No       | Should use a fallback for the query.            |
| lat, long              | string    | No       | Latitude/longitude for location.                |
| postal_code            | string    | No       | Postal code of the query location.              |
| city, state            | string    | No       | City/state associated with the query.           |
| header_country         | string    | No       | Country where the request originated.           |
| more_results_available | bool      | No       | More results exist for the query.               |
| custom_location_label  | string    | No       | Custom location labels.                         |
| reddit_cluster         | string    | No       | Associated Reddit cluster.                      |

---

### Discussions

| Field           | Type                    | Required | Description                                    |
|-----------------|-------------------------|----------|------------------------------------------------|
| type            | "search"                | Yes      | Type identifier ("search").                    |
| results         | list [DiscussionResult] | Yes      | List of discussions.                           |
| mutated_by_goggles | bool                 | Yes      | If results are changed by a Goggle (default: false). |

---

### FAQ

| Field   | Type        | Required | Description                       |
|---------|-------------|----------|-----------------------------------|
| type    | "faq"       | Yes      | "faq" type identifier.            |
| results | list [QA]   | Yes      | Aggregated Q&A results.           |

---

### Search

| Field          | Type                 | Required | Description                                        |
|----------------|----------------------|----------|----------------------------------------------------|
| type           | "search"             | Yes      | "search" type identifier.                          |
| results        | list [SearchResult]  | Yes      | List of web search results.                        |
| family_friendly| bool                 | Yes      | Whether the results are family friendly.           |

---

### SearchResult

| Field         | Type                  | Required | Description                                                   |
|---------------|-----------------------|----------|---------------------------------------------------------------|
| type          | "search_result"       | Yes      | Identifier for search result (always "search_result").         |
| subtype       | "generic"             | Yes      | Sub type identifier.                                         |
| is_live       | bool                  | Yes      | Result is currently live.                                    |
| deep_results  | DeepResult            | No       | Aggregated info for this result.                             |
| schemas       | list [list]           | No       | Structured data (schema.org style) extracted from the page.  |
| meta_url      | MetaUrl               | No       | Info about the result's URL.                                 |
| thumbnail     | Thumbnail             | No       | Thumbnail for the result.                                    |
| age           | string                | No       | Age of the result.                                           |
| language      | string                | Yes      | Main language on the result.                                 |
| location      | LocationResult        | No       | Location details for location queries.                       |
| ...           | ...                   | ...      | (See full spec for additional fields.)                       |

---

### Locations

| Field   | Type                    | Required | Description                              |
|---------|-------------------------|----------|------------------------------------------|
| type    | "locations"             | Yes      | Type identifier ("locations").           |
| results | list [LocationResult]   | Yes      | Aggregated list of location results.     |

---

### MixedResponse

| Field | Type                  | Required | Description                  |
|-------|-----------------------|----------|------------------------------|
| type  | "mixed"               | Yes      | Type identifier ("mixed").   |
| main  | list [ResultReference]| No       | Ranking for main section.    |
| top   | list [ResultReference]| No       | Ranking for top section.     |
| side  | list [ResultReference]| No       | Ranking for side section.    |

---

### News

| Field   | Type                | Required | Description                          |
|---------|---------------------|----------|--------------------------------------|
| type    | "news"              | Yes      | Type identifier ("news").            |
| results | list [NewsResult]   | Yes      | List of news results.                |
| mutated_by_goggles | bool     | No       | If results changed by a Goggle.      |

---

### Videos

| Field   | Type                  | Required | Description                          |
|---------|-----------------------|----------|--------------------------------------|
| type    | "videos"              | Yes      | Type identifier ("videos").          |
| results | list [VideoResult]    | Yes      | List of video results.               |
| mutated_by_goggles | bool       | No       | If results changed by a Goggle.      |

---

**Note:**  
- For more details, see each submodel (`Result`, `MetaUrl`, `LocationResult`, `Thumbnail`, etc.) as needed in the full schema.
- Table formatting in Markdown uses pipes and hyphens for column separation and headers[1][2][3][4].
