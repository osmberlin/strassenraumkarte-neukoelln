---
title: "Call for help from the data science community: Evaluate tradeoffs in data quality for mapping parking data in OSM"
date: 2021-12-13 06:00:00 +0100
author: Tobias Jordans @tordans
layout: post
# menu_highlight: none
# canonical_url:
language: "en"
---

![_Screenshot of the parking map with debugging circles to show different cutoff areas.](../images/posts/strassenraumkarte/parkstreifen-generieren.jpg){: class='img-thumbnail' }

The volunteer project "[Parkraumkarte](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=parkingmap#17/52.47379/13.44164)" shows that OSM data can be used to calculate the available roadside parking space with very high accuracy.

Our controlgroup counts showed that the accuracy of the data for Neukölln is **only ~0,4 % of.** [See this table of our control counts](https://supaplexosm.github.io/strassenraumkarte-neukoelln/parkraumkarte/report#anhang-b-vergleich-interpolierter-und-gez%C3%A4hlter-stellpl%C3%A4tze-stra%C3%9Fenparken).

**However, this accuracy comes at a cost:** It requires a very high level of detail of mapped data. Not only parking lane attributes, but also driveways, pedestrian crossings, curb data and other map data of objects that prevent cars from parking at a place. This high level of detail is not available in other districts of Berlin or most other cities. Which is why we want to evaluate which level of detailed mapping is actually required to produce accurate parking data.

Please [watch Alex’ presentation](https://supaplexosm.github.io/strassenraumkarte-neukoelln/posts/2021-06-08-vortrag-fossgis) and [read his report](https://supaplexosm.github.io/strassenraumkarte-neukoelln/parkraumkarte/report) to learn more about the process used to calculate the parking data.

## The question is…

**What are the tradeoffs if we remove some accuracy from this process? We want to find the way of mapping with the least effort but the highest accuracy. Or in other words: We want to see how much accuracy every additional step of the mapping and processing process adds.**

This will likely be different for different parking styles. For example, parking perpendicular requires a higher level of mapped details since more cars will be added/removed per meter, so the error rate will be higher.

## The current process

(Again, please check out the video and report for details about how the data is generated and processed.)

- **Step 0:** The highway lanes are already present in OSM and with it street junction (which represent non-parking space in this analysis)
- **Step 1:** We add parking:lane tags to the lanes. Note, that we only cut the lanes when absolutely necessary. We rely on subtracting space by tagging it, rather than cutting lanes in small pieces.

Now we add data, that we use to accurately subtract non-parking space:

- **Step 2:** We add all driveway, especially private ones, that have a lowered curb or disallow parking by signage or other means.
- **Step 3.1:** We map pedestrian crossings as node on the way
- **Step 3.2:** We enright the pedestrian crossings nodes with information about the type of markings or protection (eg. curb extensions)
- **Step 4:** We map parking bays – street side parking spaces that have a curb – separately, which allows us to more accurately model the curb extensions with trees or just grass in between the parking bays.
- **Step 5:** We add trees, traffic signs, street lights, street cabinets where those objects will prevent a car from using the parking space.
- **Step 6:** Validate that traffic signals on junctions are mapped on their stop position, rather than on the intersection of the streets ([learn more](https://wiki.openstreetmap.org/wiki/DE:Tag:highway%3Dtraffic_signals)); improve the data if missing.
- **Step 7:** Validate that all bus stops (`public_transport=stop_position`) have a node representing the stop area (`highway=bus_stop`) on each side; add them if missing.
- **Step 8:** We add parking spaces for bikes or motorcycles that are located on the roadway/lane.
- **Step 9:** We add width-attributes to those driveway if they have a special width in order to accurately represent their impact on parking (we assume a default impact on parking of 4m).
- Step **10:** In a separate processing step, we move the parking lane per side from the center of the road to the curb, which slightly changes the geometry and length.

### Those are the cutoffs that we use for the analysis

Those values are taken from [this table in the report](https://supaplexosm.github.io/strassenraumkarte-neukoelln/parkraumkarte/report#24-datenverarbeitung-zur-modellierung-des-stra%C3%9Fenparkens). Please learn more overthere.

- **Crossing:** 5m from (virtual) kerb line intersection, depending on road width
- **Pedestrian Crossing:**
  - 4m default crossing
  - 6m with “buffer markings” or curb extensions ([Example for both](https://supaplexosm.github.io/strassenraumkarte-neukoelln/?map=micromap#20/52.48057/13.43204))
  - 5m before zebra crossings on each side
  - 10m before traffic signals
- **Driveways:** 4m if no other width is specified as a tag on the driveway
- **Bus stops: 15m before and after the bus stop sign (`highway=bus_stop`)

The values depend on local traffic law; those are values that work well for Berlin.

![_Screenshot of the parking map with debugging circles to show different cutoff areas.](../images/posts/strassenraumkarte/parkstreifen-generieren.jpg){: class='img-thumbnail' }

_Screenshot of the parking map with debugging circles to show different cutoff areas._

## Possible report structure and questions to be analysed

This chapter is meant to provide insight into the questions we would like to have answered how we think those answered might be structured.

| Mapping precision step                           | Number of parked cars | Difference to baseline     | Added precision to previous step |
| ------------------------------------------------ | --------------------- | -------------------------- | -------------------------------- |
| Baseline (eg. manual count or Alex precise data) | 789 cars              | \-                         | \-                               |
| Step 1a:, Add \`parking:lane\` data >50m         | 1.000 cars            | x% difference to baseline  | \-                               |
| Step 1b: Add \`parking:lane\`data <50m           | 950 cars              | x2% difference to baseline | Step adds x3% precision          |
| Step 2: Add driveways and remove cuttof          | 900 cars              | x4% difference to baseline | Step adds x5% precision          |
| …                                                |                       |                            |                                  |
{: class='border-b' }

**About Step 1a and 1b:** It would be ideal to split the mapping of Step 1 during analysis to get an even better idea about the error rate of roughly mapped areas.

**Report step 1.a:** Add attributes that describe the direction of parking (or no parking) for a whole street (crossing to crossing / start to end).

This can be done by using a tool like [zlant.github.io/parking-lanes/](https://zlant.github.io/parking-lanes/#17/52.47906/13.42876) or by adding the tags manually using the iD Editor on osm.org or JOSM. (Side note: Building an easy to use editor will be a key effort in scaling this process.)

We only cut a road where an obvious change in the direction of parking >50m happens.

This is the roughest we can get and meant to simulate the mapping precision of a novice user who uses aerial imagery as a source of information.

**Report step 1.b:** Add changes in parking (especially no parking) <50m. For example at the beginning of roads where the parking direction might change to parallel or no parking. This step requires splitting the roads more accurately in places where automated cut offs (crossings, …) are not feasible.

To do this, a mapper needs to pay close attention or collect “ground truth” (survey the streets vs. mapping from aerial imagery).

### Report area

It might be possible to do this report based on just a few selected streets.

It might even be possible to do it based on a fictitious street.

Another approach would be to use an existing area in Berlin. It should have a good spread of different parking directions and pedestrian crossing forms. It should also have a few parking bays.

However, not too much of one of those.
- A lot of `diagonal` or `perpendicular` would increase the error rate since small mapping errors have a bigger impact.
- Reichenberger Kiez in Kreuzberg has a lot of parking bays, which means only Step 4 will become especially important for a high precision.

**Possible areas:**

- **Schillerkiez** – has a lot of different parking situations which are mapped in high precision. There are also a few manual counts for comparison. However, there is a lot of `diagonal` and `perpendicular` parking, so the error rate issue mentioned above needs to be considered.
- **Richardkiez** or maybe only the South part of Richardkiez below Richardplatzes. Also a high level of mapping and different parking situations.

## Why is this report important

Right now, the project “Parkraumkarte” cannot be applied to other districts due to missing mapping details. Adding all this data is a time consuming and complex process which requires quite a lot of domain knowledge on how to map in OSM.

With this report, we can improve the documentation of the project and make it easier for other communities to create parking data for their district or city.

In addition, we have contact with representatives from city administration offices that are interested in this data. The accuracy we can provide in their district is a key question. With this report, we can start the conversation and describe the quality of data with high confidence.

Please also consider giving a presentation about your report at the FOSSGIS or “State Of The Map” conference.

## Let's connect

We are using the [DSSG Dathon 2021 Slack to connect](https://dssgdatathon2021.slack.com/archives/C02KRJGTFGF). Please reach out at [t@tobiasjordans.de](mailto:t@tobiasjordans.de) to join.
