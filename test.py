from datetime import date, timedelta
import requests
import json
import pandas as pd
import openpyxl
import numpy as np

# loads: string to object
# dumps: object to string


def daysBetween(date1,date2):

    days = []
    tmp1 = (date1.split("-"))
    tmp2 = (date2.split("-"))
    beginDate = list(map(int, tmp1))
    endDate = list(map(int, tmp2))

    # debug
    # print(beginDate)
    # print(endDate)
    # print(type(beginDate))

    start_date = date(beginDate[0], beginDate[1], beginDate[2])
    end_date = date(endDate[0], endDate[1], endDate[2])

    delta = end_date - start_date   # returns timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        days.append(str(day))
        # days = days+[str(day)]
        # print(day)

    return days

def address(city):
    usa = "united-states-of-america"
    if city == "":
        city = "chicago-illinois-united-states-of-america"
    if usa not in city:
        city = city + " " +usa
    city = city.replace(" ", "-").lower()
    return city

# Variables and API stuff =================================
url = "https://www.vrbo.com/serp/g"
unitID = []
name = []
dates = {}
price = []

api = {
  "operationName": "SearchRequestQuery",
  "variables": {
    "filterCounts": True,
    "request": {
      "paging": {
        "page": 1,
        "pageSize": 50
      },
      "filterVersion": "1",
      "coreFilters": {
        "adults": 3,
        "maxBathrooms": None,
        "maxBedrooms": None,
        "maxNightlyPrice": None,
        "maxTotalPrice": None,
        "minBathrooms": 0,
        "minBedrooms": 3,
        "minNightlyPrice": 0,
        "minTotalPrice": None,
        "pets": 0
      },
      "filters": [],
      "q": "chicago-illinois-united-states-of-america"
    },
    "optimizedBreadcrumb": False,
    "vrbo_web_global_messaging_banner": True
  },
  "extensions": {
    "isPageLoadSearch": True
  },
  "query": "query SearchRequestQuery($request: SearchResultRequest!, $filterCounts: Boolean!, $optimizedBreadcrumb: Boolean!, $vrbo_web_global_messaging_banner: Boolean!) {  results: search(request: $request) {    ...querySelectionSet    ...DestinationBreadcrumbsSearchResult    ...DestinationMessageSearchResult    ...FilterCountsSearchRequestResult    ...HitCollectionSearchResult    ...ADLSearchResult    ...MapSearchResult    ...ExpandedGroupsSearchResult    ...PagerSearchResult    ...SearchTermCarouselSearchResult    ...InternalToolsSearchResult    ...SEOMetaDataParamsSearchResult    ...GlobalInlineMessageSearchResult    ...GlobalBannerContainerSearchResult @include(if: $vrbo_web_global_messaging_banner)    __typename  }}fragment querySelectionSet on SearchResult {  id  typeaheadSuggestion {    uuid    term    name    __typename  }  geography {    lbsId    gaiaId    location {      latitude      longitude      __typename    }    isGeocoded    shouldShowMapCentralPin    __typename  }  propertyRedirectUrl  __typename}fragment DestinationBreadcrumbsSearchResult on SearchResult {  destination(optimizedBreadcrumb: $optimizedBreadcrumb) {    breadcrumbs {      name      url      __typename    }    __typename  }  __typename}fragment HitCollectionSearchResult on SearchResult {  page  pageSize  pageCount  queryUUID  percentBooked {    currentPercentBooked    __typename  }  listings {    ...HitListing    __typename  }  resultCount  pinnedListing {    headline    listing {      ...HitListing      __typename    }    __typename  }  __typename}fragment HitListing on Listing {  virtualTourBadge {    name    id    helpText    __typename  }  amenitiesBadges {    name    id    helpText    __typename  }  images {    altText    c6_uri    c9_uri    mab {      banditId      payloadId      campaignId      cached      arm {        level        imageUrl        categoryName        __typename      }      __typename    }    __typename  }  ...HitInfoListing  __typename}fragment HitInfoListing on Listing {  listingId  ...HitInfoDesktopListing  ...HitInfoMobileListing  ...PriceListing  __typename}fragment HitInfoDesktopListing on Listing {  detailPageUrl unitApiUrl  instantBookable  minStayRange {    minStayHigh    minStayLow    __typename  }  listingId  listingNumber  rankedBadges(rankingStrategy: SERP) {    id    helpText    name    __typename  }  propertyId  propertyMetadata {    headline    __typename  }  superlativesBadges: rankedBadges(rankingStrategy: SERP_SUPERLATIVES) {    id    helpText    name    __typename  }  unitMetadata {    unitName    __typename  }  webRatingBadges: rankedBadges(rankingStrategy: SRP_WEB_RATING) {    id    helpText    name    __typename  }  ...DetailsListing  ...GeoDistanceListing  ...RateSummary ...PriceListing  ...RatingListing  __typename}fragment DetailsListing on Listing {  bathrooms {    full    half    toiletOnly    __typename  }  bedrooms  propertyType  sleeps  petsAllowed  spaces {    spacesSummary {      area {        areaValue        __typename      }      bedCountDisplay      __typename    }    __typename  }  __typename}fragment GeoDistanceListing on Listing {  geoDistance {    text    relationType    __typename  }  __typename}  fragment RateSummary on Listing { rateSummary { beginDate  endDate rentNights } } fragment PriceListing on Listing {  priceSummary: priceSummary {  priceAccurate    ...PriceSummaryTravelerPriceSummary    __typename  }  priceSummarySecondary: priceSummary(summary: \"displayPriceSecondary\") {    ...PriceSummaryTravelerPriceSummary    __typename  }  priceLabel: priceSummary(summary: \"priceLabel\") {    priceTypeId    pricePeriodDescription    __typename  }  prices {    ...VrboTravelerPriceSummary    __typename  }  __typename}fragment PriceSummaryTravelerPriceSummary on TravelerPriceSummary {  priceTypeId  edapEventJson  formattedAmount  roundedFormattedAmount  pricePeriodDescription  __typename}fragment VrboTravelerPriceSummary on PriceSummary {  perNight {    amount    formattedAmount    roundedFormattedAmount    pricePeriodDescription    __typename  }  total {    amount    formattedAmount    roundedFormattedAmount    pricePeriodDescription    __typename  }  label  mainPrice  __typename}fragment RatingListing on Listing {  averageRating  reviewCount  __typename}fragment HitInfoMobileListing on Listing {  detailPageUrl  instantBookable  minStayRange {    minStayHigh    minStayLow    __typename  }  listingId  listingNumber  rankedBadges(rankingStrategy: SERP) {    id    helpText    name    __typename  }  propertyId  propertyMetadata {    headline    __typename  }  superlativesBadges: rankedBadges(rankingStrategy: SERP_SUPERLATIVES) {    id    helpText    name    __typename  }  unitMetadata {    unitName    __typename  }  webRatingBadges: rankedBadges(rankingStrategy: SRP_WEB_RATING) {    id    helpText    name    __typename  }  ...DetailsListing  ...GeoDistanceListing ...RateSummary ...PriceListing  ...RatingListing  __typename}fragment ExpandedGroupsSearchResult on SearchResult {  expandedGroups {    ...ExpandedGroupExpandedGroup    __typename  }  __typename}fragment ExpandedGroupExpandedGroup on ExpandedGroup {  listings {    ...HitListing    ...MapHitListing    __typename  }  mapViewport {    neLat    neLong    swLat    swLong    __typename  }  __typename}fragment MapHitListing on Listing {  ...HitListing  geoCode {    latitude    longitude    __typename  }  __typename}fragment FilterCountsSearchRequestResult on SearchResult {  id  resultCount  filterGroups {    groupInfo {      name      id      __typename    }    filters {      count @include(if: $filterCounts)      checked      filter {        id        name        refineByQueryArgument        description        __typename      }      __typename    }    __typename  }  __typename}fragment MapSearchResult on SearchResult {  mapViewport {    neLat    neLong    swLat    swLong    __typename  }  page  pageSize  listings {    ...MapHitListing    __typename  }  pinnedListing {    listing {      ...MapHitListing      __typename    }    __typename  }  __typename}fragment PagerSearchResult on SearchResult {  fromRecord  toRecord  pageSize  pageCount  page  resultCount  __typename}fragment DestinationMessageSearchResult on SearchResult {  destinationMessage(assetVersion: 4) {    iconTitleText {      title      message      icon      messageValueType      link {        linkText        linkHref        __typename      }      __typename    }    ...DestinationMessageDestinationMessage    __typename  }  __typename}fragment DestinationMessageDestinationMessage on DestinationMessage {  iconText {    message    icon    messageValueType    __typename  }  __typename}fragment ADLSearchResult on SearchResult {  parsedParams {    q    coreFilters {      adults      children      pets      minBedrooms      maxBedrooms      minBathrooms      maxBathrooms      minNightlyPrice      maxNightlyPrice      minSleeps      __typename    }    dates {      arrivalDate      departureDate      __typename    }    sort    __typename  }  page  pageSize  pageCount  resultCount  fromRecord  toRecord  pinnedListing {    listing {      listingId      __typename    }    __typename  }  listings {    listingId    __typename  }  filterGroups {    filters {      checked      filter {        groupId        id        __typename      }      __typename    }    __typename  }  geography {    lbsId    name    description    location {      latitude      longitude      __typename    }    primaryGeoType    breadcrumbs {      name      countryCode      location {        latitude        longitude        __typename      }      primaryGeoType      __typename    }    __typename  }  __typename}fragment SearchTermCarouselSearchResult on SearchResult {  discoveryXploreFeeds {    results {      id      title      items {        ... on SearchDiscoveryFeedItem {          type          imageHref          place {            uuid            name {              full              simple              __typename            }            __typename          }          __typename        }        __typename      }      __typename    }    __typename  }  typeaheadSuggestion {    name    __typename  }  __typename}fragment InternalToolsSearchResult on SearchResult {  internalTools {    searchServiceUrl    __typename  }  __typename}fragment SEOMetaDataParamsSearchResult on SearchResult {  page  resultCount  pageSize  geography {    name    lbsId    breadcrumbs {      name      __typename    }    __typename  }  __typename}fragment GlobalInlineMessageSearchResult on SearchResult {  globalMessages {    ...GlobalInlineAlertGlobalMessages    __typename  }  __typename}fragment GlobalInlineAlertGlobalMessages on GlobalMessages {  alert {    action {      link {        href        text {          value          __typename        }        __typename      }      __typename    }    body {      text {        value        __typename      }      link {        href        text {          value          __typename        }        __typename      }      __typename    }    id    severity    title {      value      __typename    }    __typename  }  __typename}fragment GlobalBannerContainerSearchResult on SearchResult {  globalMessages {    ...GlobalBannerGlobalMessages    __typename  }  __typename}fragment GlobalBannerGlobalMessages on GlobalMessages {  banner {    body {      text {        value        __typename      }      link {        href        text {          value          __typename        }        __typename      }      __typename    }    id    severity    title {      value      __typename    }    __typename  }  __typename}"
}


# Get Inputs
pageSize = int(input("Enter pageSize: "))
# pageSize = 3      # hardcoding
city = input("Enter address (default: chicago-illinois-united-states-of-america): ")
city = address(city)

print(city)
# sleep(20)

# set inputs equal to variable and replace API value =================================
api["variables"]["request"]["paging"]["pageSize"] = pageSize
api["variables"]["request"]["q"] = city
# print(api["variables"]["request"]["paging"])
# print("yooooo:"+api["variables"]["request"]["q"])

# API requests =================================
payload = json.dumps(api)
headers = {
  'Content-Type': 'application/json',
  'Cookie': 'HMS=0d9daea8-d5a7-45aa-8377-5d026d159e88; ak_bmsc=4A1B1FA76465174F049F64C05D41E0E6~000000000000000000000000000000~YAAQhSABF0ysAHR+AQAASdckeQ6DOJCCV1McWCkow+au+NIsj14Sw44ZHtH3JH5z75q7q688LKHBdslkrRJGkGXY5z37pWLcJGyvEnzWZVUTUYJHwK0b3aMnFoJAOW4m9MrNqo5Mq0cDwjg9bId/2XrKyTHjFoAXyhYg88BNqV03HQu+ofrlVEh2F4zqVS4O4rBPY73eup66PER2Pb5BLW1CAlUFTCAEZh+G1SWpOzwAg/Hf1T6+tmZDlibSuFBWZYNtkwJqJ4+hoWQkKZ0I7BgsFyU+FzpI0HwPM9rqhYH/bPcxh3wH5K9BOHHXH8I8NhdkkzpruwwV+7McT2XeVPPIrs+J3f9S0Dir0LeJTR7h5afIbj79xvLx; bm_sv=C791C2FA1CDCF6E66FF5E55ABE10D92B~9DRF3sYJ4KgiZJUrVqIaY1/iZ1MyZA60cIGgVSb2X850AgyABItdLVY6KcfmVcX7XAS55caHFzX2oo3QX9ptK0eq75jt6EJoJ4vbi8ND6N4qqpSCf4jvV74hu83RDS/VKMXxmVlfxOCAqyswIzQj6Q==; dd67fe18-b8cd-4c75-6c45-56257c61c9a6SL=1; eu-site=0; ha-device-id=d71b5f7b-c22e-c72a-8aa3-719829cb1d0f; hal=ga=1&ua=1&si=1&ui=1&vi=1&pr=0; has=dd67fe18-b8cd-4c75-6c45-56257c61c9a6; hav=d71b5f7b-c22e-c72a-8aa3-719829cb1d0f'
}

response = requests.request("POST", url, headers=headers, data=payload)

output = json.loads(response.text)

# get dates in an array =================================
# beginDate = output["data"]["results"]["listings"][0]["rateSummary"]["beginDate"]
beginDate = str(date.today())
# endDate = output["data"]["results"]["listings"][0]["rateSummary"]["endDate"]
endDate = "2023-01-25"
# beginDate = "2022-01-17"
dates = daysBetween(beginDate,endDate)
# print(dates)

newcols = dict()

for index,value in enumerate(dates):
  newcols[value] = []
# print(newcols)


# get UnitID and listing names =================================
for i in range(0,pageSize):
    # print(output["data"]["results"]["listings"][i]["listingId"].split(".")[2])
    # print(output["data"]["results"]["listings"][i]["propertyMetadata"]["headline"])
    unitID.append(output["data"]["results"]["listings"][i]["listingId"].split(".")[2])
    name.append(output["data"]["results"]["listings"][i]["propertyMetadata"]["headline"])


# get rents in an object of arrays =================================
# ===========================================================
tmp = dict()
for i in range(0,pageSize):
    # print(i)
    for j in range(0,len(dates)):

        if output["data"]["results"]["listings"][i]["rateSummary"] is None:
            newcols[str(dates[j])].append(None)
            continue
            # print("yay")

        if output["data"]["results"]["listings"][i]["rateSummary"]["rentNights"] is None:
            # print(i)
            newcols[str(dates[j])].append(None)
            # print("noneeeee")
            continue
        else:
            rent =output["data"]["results"]["listings"][i]["rateSummary"]["rentNights"][j]
            newcols[str(dates[j])] = newcols[str(dates[j])] + [rent]

# print("tmp is")
# print(tmp)


# ===========================================================

#


data = {
        'Unit ID': unitID,
        'Name': name
    }

# dataframes =================================
df = pd.DataFrame(data, columns=['Unit ID', 'Name'])
df2 = pd.DataFrame(newcols)

print(df2)

df3 =  pd.concat([df,df2], axis =1)

# Output as an excel file
df3.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')
