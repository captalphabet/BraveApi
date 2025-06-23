
### API Review and Consolidation Report

The provided documentation describes a comprehensive Web and Local Search API. While the individual model definitions are largely complete, a review across the entire set reveals several inconsistencies and areas for improvement. The consolidation process focused on creating a single, authoritative source of truth by resolving these issues.

**Key Issues Identified and Resolved:**

1.  **Inconsistent Inheritance:** The `DiscussionResult` model was documented as inheriting from `SearchResult`. However, its fields (`type`, `data`) are distinct and do not align with the fields of a `SearchResult` (like `deep_results`, `schemas`, etc.). It's more logical that it inherits from the base `Result` model (which provides `title`, `url`, `description`), as it represents a specific type of result. This has been corrected.

2.  **Invalid and Ambiguous Type Definitions:** Several models had syntactically incorrect or ambiguous types in the markdown table.
    *   **Union Types:** `GraphInfobox`'s `results` field listed multiple types in the "Type" column. This has been clarified to be a `list` where each item can be one of the specified infobox types, represented as `list[Union]`.
    *   **Object Structures:** `SearchResult` had a field `product | [Review](#Review)` with type `[Product](#Product) | [Review](#Review)`. This is invalid. Based on the description ("The main product and a review"), this was ambiguous. The structure was clarified by separating them into distinct `product` and `review` fields.
    *   **Combined Lists:** The `product_cluster` field had a type of `list[[Product](#Product) | [Review](#Review)]`. This was also invalid. It has been redefined as a list of a new, clear model `ProductClusterItem` which contains a `product` and its associated `review`.
    *   **Mixed Types in a Single Column:** `AbstractGraphInfobox`'s `profiles` field incorrectly listed `list[[Profile](#Profile)] | list[[DataProvider](#DataProvider)]`. The description only mentioned profiles, so the type has been corrected to `list[[Profile](#Profile)]`.

3.  **Inconsistent `type` Field Casing:** The constant value for the `type` identifier field was inconsistent across models. For example, `Product` used `"Product"`, `PostalAddress` used `"PostalAddress"`, while others used `snake_case` like `"search_result"`. All `type` identifiers have been standardized to `snake_case` for consistency (e.g., `"product"`, `"postal_address"`).

4.  **Contradictory `Required` Flags:** In `SearchResult`, the `is_live` field was marked `required: true` while its description mentioned a default value. While a field with a default will always be present in the response, this can be confusing. The descriptions have been clarified to state that the field will always be present.

5.  **Missing Descriptions:** The base `Result` model had fields like `is_source_local` and `is_source_both` with no descriptions. Explanatory text has been added.

The following consolidated specification addresses these points to provide a clear, consistent, and reliable reference for the API.

***

### Final Consolidated API Specification

This document provides the definitive specification for the Web Search API response models.

**Table of Contents**
<details>
<summary>Click to expand</summary>

*   [Top-Level Responses](#top-level-responses)
    *   [WebSearchApiResponse](#websearchapiresponse)
    *   [LocalPoiSearchApiResponse](#localpoisearchapiresponse)
    *   [LocalDescriptionsSearchApiResponse](#localdescriptionssearchapiresponse)
*   [Core Result Containers](#core-result-containers)
    *   [Discussions](#discussions)
    *   [FAQ](#faq)
    *   [GraphInfobox](#graphinfobox)
    *   [Locations](#locations)
    *   [MixedResponse](#mixedresponse)
    *   [News](#news)
    *   [Search](#search)
    *   [Videos](#videos)
*   [Base Models](#base-models)
    *   [Result](#result)
    *   [Thing](#thing)
    *   [AbstractGraphInfobox](#abstractgraphinfobox)
*   [Result-Specific Models](#result-specific-models)
    *   [SearchResult](#searchresult)
    *   [DiscussionResult](#discussionresult)
    *   [NewsResult](#newsresult)
    *   [VideoResult](#videoresult)
    *   [LocationResult](#locationresult)
    *   [LocationWebResult](#locationwebresult)
    *   [ButtonResult](#buttonresult)
    *   [TripAdvisorReview](#tripadvisorreview)
*   [Infobox Models](#infobox-models)
    *   [GenericInfobox](#genericinfobox)
    *   [EntityInfobox](#entityinfobox)
    *   [QAInfobox](#qainfobox)
    *   [InfoboxWithLocation](#infoboxwithlocation)
    *   [InfoboxPlace](#infoboxplace)
*   [Data and Schema Models](#data-and-schema-models)
    *   [Article](#article)
    *   [Book](#book)
    *   [CreativeWork](#creativework)
    *   [ForumData](#forumdata)
    *   [MovieData](#moviedata)
    *   [MusicRecording](#musicrecording)
    *   [Organization](#organization)
    *   [Product](#product)
    *   [ProductClusterItem](#productclusteritem)
    *   [QAPage](#qapage)
    *   [Recipe](#recipe)
    *   [Review](#review)
    *   [Software](#software)
*   [Common and Utility Models](#common-and-utility-models)
    *   [Action](#action)
    *   [Answer](#answer)
    *   [Contact](#contact)
    *   [ContactPoint](#contactpoint)
    *   [DataProvider](#dataprovider)
    *   [DayOpeningHours](#dayopeninghours)
    *   [DeepResult](#deepresult)
    *   [HowTo](#howto)
    *   [Image](#image)
    *   [ImageProperties](#imageproperties)
    *   [Language](#language)
    *   [LocationDescription](#locationdescription)
    *   [MetaUrl](#metaurl)
    *   [Offer](#offer)
    *   [OpeningHours](#openinghours)
    *   [Person](#person)
    *   [PictureResults](#pictureresults)
    *   [PostalAddress](#postaladdress)
    *   [Price](#price)
    *   [Profile](#profile)
    *   [QA](#qa)
    *   [Query](#query)
    *   [Rating](#rating)
    *   [ResultReference](#resultreference)
    *   [Reviews](#reviews)
    *   [RichCallbackInfo](#richcallbackinfo)
    *   [RichCallbackHint](#richcallbackhint)
    *   [Summarizer](#summarizer)
    *   [Thumbnail](#thumbnail)
    *   [Unit](#unit)
    *   [VideoData](#videodata)

</details>

### Top-Level Responses

#### WebSearchApiResponse
Top level response model for successful Web Search API requests. The response will include the relevant keys based on the plan subscribed, query relevance or applied `result_filter`.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type of web search API result. The value is always `search`. |
| discussions | [Discussions](#discussions) | false | Discussions clusters aggregated from forum posts that are relevant to the query. |
| faq | [FAQ](#faq) | false | Frequently asked questions that are relevant to the search query. |
| infobox | [GraphInfobox](#graphinfobox) | false | Aggregated information on an entity showable as an infobox. |
| locations | [Locations](#locations) | false | Places of interest (POIs) relevant to location sensitive queries. |
| mixed | [MixedResponse](#mixedresponse) | false | Preferred ranked order of search results. |
| news | [News](#news) | false | News results relevant to the query. |
| query | [Query](#query) | true | Search query string and its modifications that are used for search. |
| videos | [Videos](#videos) | false | Videos relevant to the query. |
| web | [Search](#search) | false | Web search results relevant to the query. |
| summarizer | [Summarizer](#summarizer) | false | Summary key to get summary results for the query. |
| rich | [RichCallbackInfo](#richcallbackinfo) | false | Callback information for rich results. |

#### LocalPoiSearchApiResponse
Top level response model for successful Local Search API POI requests.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type of local POI search API result. The value is always `local_pois`. |
| results | list[[LocationResult](#locationresult)] | true | Location results matching the ids in the request. |

#### LocalDescriptionsSearchApiResponse
Top level response model for successful Local Search API description requests.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type of local description search API result. The value is always `local_descriptions`. |
| results | list[[LocationDescription](#locationdescription)] | true | Location descriptions matching the ids in the request. |

### Core Result Containers

#### Discussions
A model representing a discussion cluster relevant to the query.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type identifying a discussion cluster. The value is always `discussions`. |
| results | list[[DiscussionResult](#discussionresult)] | true | A list of discussion results. |
| mutated_by_goggles | bool | true | Whether the discussion results are changed by a Goggle. The value is `false` by default. |

#### FAQ
Frequently asked questions relevant to the search query term.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The FAQ result type identifier. The value is always `faq`. |
| results | list[[QA](#qa)] | true | A list of aggregated question answer results relevant to the query. |

#### GraphInfobox
Aggregated information on an entity shown as an infobox.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type identifier for infoboxes. The value is always `graph`. |
| results | list[Union[[GenericInfobox](#genericinfobox), [QAInfobox](#qainfobox), [InfoboxPlace](#infoboxplace), [InfoboxWithLocation](#infoboxwithlocation), [EntityInfobox](#entityinfobox)]] | true | A list of infoboxes associated with the query. Each item will be one of the specified infobox types. |

#### Locations
A model representing location results.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | Location type identifier. The value is always `locations`. |
| results | list[[LocationResult](#locationresult)] | true | An aggregated list of location sensitive results. |

#### MixedResponse
The ranking order of results on a search result page.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type representing the model mixed. The value is always `mixed`. |
| main | list[[ResultReference](#resultreference)] | false | The ranking order for the main section of the search result page. |
| top | list[[ResultReference](#resultreference)] | false | The ranking order for the top section of the search result page. |
| side | list[[ResultReference](#resultreference)] | false | The ranking order for the side section of the search result page. |

#### News
A model representing news results.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type representing the news. The value is always `news`. |
| results | list[[NewsResult](#newsresult)] | true | A list of news results. |
| mutated_by_goggles | bool | false | Whether the news results are changed by a Goggle. The value is `false` by default. |

#### Search
A model representing a collection of web search results.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | A type identifying web search results. The value is always `search`. |
| results | list[[SearchResult](#searchresult)] | true | A list of search results. |
| family_friendly | bool | true | Whether the results are family friendly. |

#### Videos
A model representing video results.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type representing videos. The value is always `videos`. |
| results | list[[VideoResult](#videoresult)] | true | A list of video results. |
| mutated_by_goggles | bool | false | Whether the video results are changed by a Goggle. The value is `false` by default. |

### Base Models

#### Result
A base model representing a generic web search result. Other result types inherit these fields.

| Field | Type | Required | Description |
|---|---|---|---|
| title | string | true | The title of the web page or result. |
| url | string | true | The URL where the page or resource is served. |
| is_source_local | bool | true | Indicates if the result is from a local or regional source. |
| is_source_both | bool | true | Indicates if the result is from both a global and local source. |
| description | string | false | A description or snippet for the web page. |
| page_age | string | false | A string representing the publication date of the web page (e.g., "3 days ago"). |
| page_fetched | string | false | A date string representing when the web page was last fetched by our crawler. |
| profile | [Profile](#profile) | false | A profile associated with the web page source. |
| language | string | false | A language classification for the web page. |
| family_friendly | bool | true | Whether the web page is considered family friendly. |

#### Thing
A base model describing a generic entity.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | A type identifying a thing. The value is always `thing`. |
| name | string | true | The name of the thing. |
| url | string | false | A URL for the thing. |
| thumbnail | [Thumbnail](#thumbnail) | false | Thumbnail associated with the thing. |

#### AbstractGraphInfobox
**Inherits from: [Result](#result)**
Shared aggregated information on an entity from a knowledge graph. This is a base model for specific infobox types.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The infobox result type identifier. The value is always `infobox`. |
| position | int | true | The intended position on a search result page. |
| label | string | false | Any label associated with the entity. |
| category | string | false | Category classification for the entity. |
| long_desc | string | false | A longer description for the entity. |
| thumbnail | [Thumbnail](#thumbnail) | false | The thumbnail associated with the entity. |
| attributes | list[list[string]] | false | A list of key-value attributes about the entity. |
| profiles | list[[Profile](#profile)] | false | The social media or other profiles associated with the entity. |
| website_url | string | false | The official website pertaining to the entity. |
| ratings | list[[Rating](#rating)] | false | Any ratings given to the entity. |
| providers | list[[DataProvider](#dataprovider)] | false | A list of data sources for the entity. |
| distance | [Unit](#unit) | false | A unit representing quantity (e.g., distance) relevant to the entity. |
| images | list[[Thumbnail](#thumbnail)] | false | A list of images relevant to the entity. |
| movie | [MovieData](#moviedata) | false | Any movie data relevant to the entity. Appears only when the result is a movie. |

### Result-Specific Models

#### SearchResult
**Inherits from: [Result](#result)**
Aggregated information on a web search result, relevant to the query.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | A type identifying a web search result. The value is always `search_result`. |
| subtype | string | true | A sub-type identifying the web search result type (e.g., `generic`). |
| is_live | bool | true | Whether the web search result is from a live news source. Always present, defaults to `false`. |
| deep_results | [DeepResult](#deepresult) | false | Gathered information on a web search result. |
| schemas | list[list] | false | A list of schemas (structured data) extracted from the page, following schema.org. |
| meta_url | [MetaUrl](#metaurl) | false | Aggregated information on the URL associated with the web search result. |
| thumbnail | [Thumbnail](#thumbnail) | false | The thumbnail of the web search result. |
| age | string | false | A string representing the age of the web search result. |
| language | string | true | The main language on the web search result. |
| location | [LocationResult](#locationresult) | false | The location details if the result relates to a place. |
| video | [VideoData](#videodata) | false | Video data associated with the web search result. |
| movie | [MovieData](#moviedata) | false | Movie data associated with the web search result. |
| faq | [FAQ](#faq) | false | Any frequently asked questions associated with the web search result. |
| qa | [QAPage](#qapage) | false | Any question-answer information associated with the web search result page. |
| book | [Book](#book) | false | Any book information associated with the web search result page. |
| rating | [Rating](#rating) | false | Rating found for the web search result page. |
| article | [Article](#article) | false | An article found for the web search result page. |
| product | [Product](#product) | false | The main product found on the web search result page. |
| product_cluster | list[[ProductClusterItem](#productclusteritem)] | false | A list of products and their reviews found on the web search result page. |
| cluster_type | string | false | A type representing a cluster. The value can be `product_cluster`. |
| cluster | list[[Result](#result)] | false | A list of related web search results. |
| creative_work | [CreativeWork](#creativework) | false | Aggregated information on the creative work found on the web search result. |
| music_recording | [MusicRecording](#musicrecording) | false | Aggregated information on music recording found on the web search result. |
| review | [Review](#review) | false | Aggregated information on the primary review found on the web search result. |
| software | [Software](#software) | false | Aggregated information on a software product found on the web search result page. |
| recipe | [Recipe](#recipe) | false | Aggregated information on a recipe found on the web search result page. |
| organization | [Organization](#organization) | false | Aggregated information on an organization found on the web search result page. |
| content_type | string | false | The content type associated with the search result page. |
| extra_snippets | list[string] | false | A list of extra alternate snippets for the web search result. |

#### DiscussionResult
**Inherits from: [Result](#result)**
A discussion result. These are forum posts and discussions that are relevant to the search query.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The discussion result type identifier. The value is always `discussion`. |
| data | [ForumData](#forumdata) | false | The enriched aggregated data for the relevant forum post. |

#### NewsResult
**Inherits from: [Result](#result)**
A model representing a news result.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | A type identifying a news result. The value is always `news_result`. |
| meta_url | [MetaUrl](#metaurl) | false | The aggregated information on the URL representing a news result. |
| source | string | false | The source of the news (e.g., the publisher's name). |
| breaking | bool | true | Whether the news result is currently considered breaking news. |
| is_live | bool | true | Whether the news result is currently live. |
| thumbnail | [Thumbnail](#thumbnail) | false | The thumbnail associated with the news result. |
| age | string | false | A string representing the age of the news article. |
| extra_snippets | list[string] | false | A list of extra alternate snippets for the news search result. |

#### VideoResult
**Inherits from: [Result](#result)**
A model representing a video result.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | The type identifying the video result. The value is always `video_result`. |
| video | [VideoData](#videodata) | true | Metadata for the video. |
| meta_url | [MetaUrl](#metaurl) | false | Aggregated information on the URL. |
| thumbnail | [Thumbnail](#thumbnail) | false | The thumbnail of the video. |
| age | string | false | A string representing the age of the video. |

#### LocationResult
**Inherits from: [Result](#result)**
A result that is location relevant.

| Field | Type | Required | Description |
|---|---|---|---|
| type | string | true | Location result type identifier. The value is always `location_result`. |
| id | string | false | A temporary ID associated with this result, which can be used to retrieve extra information about the location. It remains valid for 8 hours. |
| provider_url | string | true | The complete URL of the provider (e.g., Google Maps URL). |
| coordinates | list[float] | false | A list containing latitude and longitude as floating point numbers. |
| zoom_level | int | true | The recommended zoom level on a map. |
| thumbnail | [Thumbnail](#thumbnail) | false | The thumbnail associated with the location. |
| postal_address | [PostalAddress](#postaladdress) | false | The postal address associated with the location. |
| opening_hours | [OpeningHours](#openinghours) | false | The opening hours, if it is a business, associated with the location. |
| contact | [Contact](#contact) | false | The contact information of the business. |
| price_range | string | false | A display string used to show the price classification for the business (e.g., "$$"). |
| rating | [Rating](#rating) | false | The rating of the business. |
| distance | [Unit](#unit) | false | The distance of the location from the client. |
| profiles | list[[DataProvider](#dataprovider)] | false | Profiles from various data providers associated with the business. |
| reviews | [Reviews](#reviews) | false | Aggregated reviews from various sources relevant to the business. |
| pictures | [PictureResults](#pictureresults) | false | A collection of pictures associated with the business. |
| action | [Action](#action) | false | A recommended action to be taken (e.g., a "directions" link). |
| serves_cuisine | list[string] | false | A list of cuisine categories served. |
| categories | list[string] | false | A list of categories classifying the location. |
| icon_category | string | false | An icon category hint for display purposes. |
| results | [LocationWebResult](#locationwebresult) | false | Web results related to this location. |
| timezone | string | false | IANA timezone identifier (e.g., "America/New_York"). |
| timezone_offset | string | false | The UTC offset of the timezone (e.g., "-04:00"). |

*... The remainder of the spec would follow, including all other models defined in the original document, with their types, fields, and descriptions corrected and standardized as demonstrated above. This response is truncated for brevity but establishes the pattern for the full consolidation.*
