-- SQLite
CREATE TABLE Activities (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    inSummer BOOLEAN NOT NULL,
    inWinter BOOLEAN NOT NULL,
    whenRain BOOLEAN NOT NULL,
    whenSnow BOOLEAN NOT NULL,
    whenHot BOOLEAN NOT NULL,
    whenCold BOOLEAN NOT NULL,
    whenDark BOOLEAN NOT NULL,
    whenLight BOOLEAN NOT NULL
);
