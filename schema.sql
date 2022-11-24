CREATE TABLE "ListDataHistorical" (
	"ID"	INTEGER NOT NULL,
	"Title"	TEXT NOT NULL,
	"TitleRomaji"	TEXT,
	"MediaType"	REAL NOT NULL,
	"Format"	TEXT NOT NULL,
	"Score"	INTEGER,
	"Status"	TEXT,
	"Progress"	INTEGER,
	"Episodes"	INTEGER,
	"Repeat"	INTEGER,
	"StartedAt"	TEXT,
	"CompletedAt"	TEXT,
	"UpdatedAt"	TEXT NOT NULL,
	"Notes"	TEXT,
	"HiddenFromStatusList"	INTEGER NOT NULL,
	PRIMARY KEY("ID","UpdatedAt")
)

CREATE TABLE "CustomListMembershipHistorical" (

	"ID"	INTEGER NOT NULL,

	"UpdatedAt"	TEXT NOT NULL,

	"CustomList"	TEXT NOT NULL,

	"IsMember"	INTEGER NOT NULL,

	FOREIGN KEY("ID","UpdatedAt") REFERENCES "ListDataHistorical" ("ID", "UpdatedAt")

	PRIMARY KEY("ID","UpdatedAt","CustomList")

)

CREATE INDEX "UpdatedAtIndex" ON "ListDataHistorical" (
	"UpdatedAt"
)

CREATE VIEW [ListDataMostRecent] AS

SELECT ListDataHistorical.*

FROM ListDataHistorical

	INNER JOIN (

		SELECT ID, max(UpdatedAt) AS LastUpdated FROM ListDataHistorical GROUP BY id

	 ) recent on ListDataHistorical.ID = recent.ID AND UpdatedAt = lastupdated

