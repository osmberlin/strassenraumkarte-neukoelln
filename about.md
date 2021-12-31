---
title: Über das Projekt Straßenraumkarte Neukölln
layout: page
menu_highlight: about
noindex: true
---

<div class="notice mb-12">

# Über das Projekt

{: class='!mb-3' }

Die Straßenraumkarten Neukölln sowie die Parkraumanalyse sind ein Projekt von Alex Seidel (OSM: [Supaplex030](https://www.openstreetmap.org/user/Supaplex030/)) und der OpenStreetMap Community Berlin.

Sie wird gepflegt im Rahmen der ehrenamtlichen Aktivitäten der [Berliner OSM-Verkehrswendegruppe](https://wiki.openstreetmap.org/wiki/Berlin/Verkehrswende).

- [Kontakt]({{ 'contact' | relative_url }})
- [Code: GitHub](https://github.com/SupaplexOSM/strassenraumkarte-neukoelln/)
  {: class='!mb-0' }

</div>

# Blogpost-Liste

{: #blogposts class='!mb-3' }

Eine Liste aller Artikel und Blogposts über das Projekt.

| Datum | Artikel | Autor |
| ----- | ------- | ----- |
{% for post in site.posts -%}
| <span class='text-gray-400 whitespace-nowrap'>{{ post.date | date: site.minima.date_format }}</span> | [{{ post.title }}]({{ post.url | relative_url }}) | {{ post.author }} |
{% endfor -%}
| <span class='text-gray-400 whitespace-nowrap'>2021-03-11</span> | [Methoden- und Ergebnisbericht Parkraumanalyse für den Berliner Ortsteil Neukölln](parkraumkarte/report) | Alex Seidel @Supaplex030 |
{: class='table' }
