# Data dictionary

## Trees CSV (`betulog_trees.csv`)
| Column | Meaning |
|---|---|
| id | Tree ID: plot ID + `-T` + running number |
| plot, site, stand, age | Plot ID, site or stand name, `Young plantation` or `Older stand`, stand age in years |
| date, obs | Assessment date, observer |
| x, y | Position in the plot, metres (blank if not recorded) |
| dbh | Diameter at breast height, cm |
| defol | Defoliation / crown transparency, % (0-100) |
| dieb | Crown dieback, % |
| disc | Foliage discolouration, % |
| class | ICP Forests class: 0 (0-10%), 1 (11-25%), 2 (26-60%), 3 (61-99%), 4 dead or 100% |
| canker, bleed, fruit, crack, insect, browse, root, dead | `true` or `false` symptom flags |
| notes | Free text, including any GPS note |

## Isolates CSV (`betulog_isolates.csv`)
| Column | Meaning |
|---|---|
| id | Isolate ID (your own scheme) |
| tree | Tree ID the isolate came from |
| tissue | Leaf, twig, bark lesion margin, inner bark, xylem, root, fruiting body or soil |
| date, medium, morph | Isolation date, medium, morphotype description |
| seq | Sequence marker or accession (for example ITS, GenBank number) |
| status | Plated, pure culture, DNA extracted, sequenced, identified or contaminated |

Join isolates to trees on `isolates.tree = trees.id`.
