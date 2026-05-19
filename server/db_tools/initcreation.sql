CREATE TABLE IF NOT EXISTS users (
    userid integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    upassword text NOT NULL
);

CREATE TABLE IF NOT EXISTS aimodels (
    modelid integer PRIMARY KEY AUTOINCREMENT,
    modeltitle text NOT NULL,
    modeldescription text NOT NULL,
    modeltype text NOT NULL
);

CREATE TABLE IF NOT EXISTS historyitems (
    hid integer PRIMARY KEY AUTOINCREMENT,
    outeruserid integer,
    outermodelid integer,
    imagebin blob,
    textout text NOT NULL,
    FOREIGN KEY (outeruserid) REFERENCES users (userid),
    FOREIGN KEY (outermodelid) REFERENCES aimodels (modelid)
);

