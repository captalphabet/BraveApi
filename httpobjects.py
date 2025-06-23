
"""Objects to easily validate and pass parameters to specific Endpoints"""



from typing import List, Optional, Literal
from pydantic import BaseModel


# Web Search Request Object (res/v1/web/search)
class WebSearchRequest(BaseModel):
    q: str
    country: str = "US"
    count: Optional[int] = 20
    extra_snippets: Optional[bool] = False
    freshness: Optional[str] = None
    goggles: Optional[List[str]] = None
    offset: Optional[int] = 0
    result_filter: Optional[str] = None
    safesearch: Optional[str] = "moderate"
    search_lang: str = "en"
    spellcheck: Optional[bool] = True
    summary: Optional[bool] = None
    text_decorations: Optional[bool] = True
    ui_lang: str = "en-US"
    units: Optional[str] = None


# ----- Response object stubs and models based on docs/WebResponseSpec.md -----

# Submodel stubs (full schema definitions to be added later)
class DiscussionResult(BaseModel):
    pass

class QA(BaseModel):
    pass

class GraphInfobox(BaseModel):
    pass

class LocationResult(BaseModel):
    pass

class LocationDescription(BaseModel):
    pass

class DeepResult(BaseModel):
    pass

class MetaUrl(BaseModel):
    pass

class Thumbnail(BaseModel):
    pass

class Language(BaseModel):
    pass

class ResultReference(BaseModel):
    pass

class NewsResult(BaseModel):
    pass

class VideoResult(BaseModel):
    pass

class Summarizer(BaseModel):
    pass

class RichCallbackInfo(BaseModel):
    pass

# Top-level response models
class WebSearchApiResponse(BaseModel):
    type: Literal["search"]
    discussions: Optional["Discussions"] = None
    faq: Optional["FAQ"] = None
    infobox: Optional[GraphInfobox] = None
    locations: Optional["Locations"] = None
    mixed: Optional["MixedResponse"] = None
    news: Optional["News"] = None
    query: Optional["Query"] = None
    videos: Optional["Videos"] = None
    web: Optional["Search"] = None
    summarizer: Optional[Summarizer] = None
    rich: Optional[RichCallbackInfo] = None

class LocalPoiSearchApiResponse(BaseModel):
    type: Literal["local_pois"]
    results: Optional[List[LocationResult]] = None

class LocalDescriptionsSearchApiResponse(BaseModel):
    type: Literal["local_descriptions"]
    results: Optional[List[LocationDescription]] = None

class Query(BaseModel):
    original: str
    show_strict_warning: Optional[bool] = None
    altered: Optional[str] = None
    safesearch: Optional[bool] = None
    is_navigational: Optional[bool] = None
    is_geolocal: Optional[bool] = None
    local_decision: Optional[str] = None
    local_locations_idx: Optional[int] = None
    is_trending: Optional[bool] = None
    is_news_breaking: Optional[bool] = None
    ask_for_location: Optional[bool] = None
    language: Optional[Language] = None
    spellcheck_off: Optional[bool] = None
    country: Optional[str] = None
    bad_results: Optional[bool] = None
    should_fallback: Optional[bool] = None
    lat: Optional[str] = None
    long: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    header_country: Optional[str] = None
    more_results_available: Optional[bool] = None
    custom_location_label: Optional[str] = None
    reddit_cluster: Optional[str] = None

class Discussions(BaseModel):
    type: Literal["search"]
    results: List[DiscussionResult]
    mutated_by_goggles: bool = False

class FAQ(BaseModel):
    type: Literal["faq"]
    results: List[QA]

class Search(BaseModel):
    type: Literal["search"]
    results: List["SearchResult"]
    family_friendly: bool

class SearchResult(BaseModel):
    type: Literal["search_result"]
    subtype: Literal["generic"]
    is_live: bool
    deep_results: Optional[DeepResult] = None
    schemas: Optional[List[List]] = None
    meta_url: Optional[MetaUrl] = None
    thumbnail: Optional[Thumbnail] = None
    age: Optional[str] = None
    language: str
    location: Optional[LocationResult] = None

class Locations(BaseModel):
    type: Literal["locations"]
    results: List[LocationResult]

class MixedResponse(BaseModel):
    type: Literal["mixed"]
    main: Optional[List[ResultReference]] = None
    top: Optional[List[ResultReference]] = None
    side: Optional[List[ResultReference]] = None

class News(BaseModel):
    type: Literal["news"]
    results: List[NewsResult]
    mutated_by_goggles: Optional[bool] = None

class Videos(BaseModel):
    type: Literal["videos"]
    results: List[VideoResult]
    mutated_by_goggles: Optional[bool] = None

# allow forward references
WebSearchApiResponse.update_forward_refs()
Search.update_forward_refs()




