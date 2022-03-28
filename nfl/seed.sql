DELETE FROM user;
DELETE FROM team;
DELETE FROM league;
DELETE FROM game;
DELETE FROM pick;


INSERT INTO user VALUES (0, 'admin', 'test', 'Administrator');
INSERT INTO user VALUES (1, 'ron', 'test', 'Grandpa');
INSERT INTO user VALUES (2, 'michele', 'test', 'Michele');
INSERT INTO user VALUES (3, 'ryan', 'test', 'Ryan');
INSERT INTO user VALUES (4, 'kerry', 'test', 'Kerry');
INSERT INTO user VALUES (5, 'keira', 'test', 'Keira');
INSERT INTO user VALUES (6, 'tegan', 'test', 'Tegan');
INSERT INTO user VALUES (7, 'justin', 'pbkdf2:sha256:260000$ccMfIsnDNYMKiyhd$17967bdcbe6e622016cc8cfee74841aab40e967c1ae84d27e16d970b4634136b', 'Justin');
INSERT INTO user VALUES (8, 'regina', 'test', 'Regina');

INSERT INTO team VALUES(0, 'nfl', 0);
INSERT INTO team VALUES(1, '49ers', 2);
INSERT INTO team VALUES(2, 'bengals', 1);
INSERT INTO team VALUES(3, 'bills', 1);
INSERT INTO team VALUES(4, 'bucs', 2);
INSERT INTO team VALUES(5, 'chiefs', 1);
INSERT INTO team VALUES(6, 'packers', 2);
INSERT INTO team VALUES(7, 'rams', 2);
INSERT INTO team VALUES(8, 'titans', 1);

INSERT INTO league VALUES(0, 'NFL');
INSERT INTO league VALUES(1, 'AFC');
INSERT INTO league VALUES(2, 'NFC');

INSERT INTO game VALUES(1, 'AFC Divisional Round, Game 1', 1, "Division", 5, 3, 5);
INSERT INTO game VALUES(2, 'AFC Divisional Round, Game 2', 1, "Division", 8, 2, 2);
INSERT INTO game VALUES(3, 'NFC Divisional Round, Game 1', 2, "Division", 6, 1, 1);
INSERT INTO game VALUES(4, 'NFC Divisional Round, Game 2', 2, "Division", 4, 7, 7);
INSERT INTO game VALUES(5, 'AFC Championship', 1, "Conference", 5, 2, 2);
INSERT INTO game VALUES(6, 'NFC Championship', 2, "Conference", 7, 1, 7);
INSERT INTO game VALUES(7, 'Super Bowl', 0, "Super Bowl", 7, 2, 7);

-- Justin's picks
INSERT INTO pick VALUES(1, 7, 1, 5);
INSERT INTO pick VALUES(2, 7, 2, 1);
INSERT INTO pick VALUES(3, 7, 3, 6);
INSERT INTO pick VALUES(4, 7, 4, 4);
INSERT INTO pick VALUES(5, 7, 5, 2);
INSERT INTO pick VALUES(6, 7, 6, 1);
INSERT INTO pick VALUES(7, 7, 7, 2);
-- Dad's picks
INSERT INTO pick VALUES(8, 1, 1, 3);
INSERT INTO pick VALUES(9, 1, 2, 8);
INSERT INTO pick VALUES(10, 1, 3, 6);
INSERT INTO pick VALUES(11, 1, 4, 4);
INSERT INTO pick VALUES(12, 1, 5, 5);
INSERT INTO pick VALUES(13, 1, 6, 1);
INSERT INTO pick VALUES(14, 1, 7, 2);