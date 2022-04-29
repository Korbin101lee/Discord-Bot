CREATE TABLE IF NOT EXISTS music_player(
    Num integer PRIMARY KEY,
    Server_ID integer,
    Server_Name text,
    Voice_ID integer,
    Voice_Name text,
    User_Name text,
    Next_Queue integer,
    Queue_Name text,
    Song_Name text,
    Track_Thumbnail text,
    Track_Url text
);
